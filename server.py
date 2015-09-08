""" Every Breath of the Way """

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
# from model import connect_to_db, db, User, Attack, AttackSymptom, AttackTrigger
from collections import Counter
from Crypto.Hash import SHA256
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
import urlparse
import psycopg2  

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/breathepostgres'
# heroku = Heroku(app)
db = SQLAlchemy(app)

app.jinja_env.undefined = StrictUndefined

app.secret_key = os.urandom(24)


##########################################################################

class User(db.Model):
    """ User of Every Breath of the Way website."""

    __tablename__ = "user"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(90), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s password=%s first_name=%s last_name=%s age=%s>" % (
            self.user_id, self.email, self.password, self.first_name,
            self.last_name, self.age)


class Attack(db.Model):
    """ An instance of a User's asthma attack"""

    __tablename__ = "attack"

    attack_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    attack_date = db.Column(db.String(200))
    attack_location = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    user = db.relationship("User",
                           backref=db.backref("attack", order_by=attack_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Attack attack_id=%s attack_location=%s user_id=%s>" % (
            self.attack_id, self.attack_location, self.user_id)


class AttackSymptom(db.Model):
    """Asthma Attack and list of symptoms associated with the attack."""

    __tablename__ = "attack_symptom"

    attack_id = db.Column(db.Integer, db.ForeignKey('attack.attack_id'))
    attack_symptom_id = db.Column(db.Integer, autoincrement=True,
                                                 primary_key=True)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.symptom_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<AttackSymptom attack_symptom_id=%s attack_id=%s symptom_id=%s>" % (
            self.attack_symptom_id, self.attack_id, self.symptom_id)


class Symptom(db.Model):
    """A symptom associated with an attack by type. """

    __tablename__ = "symptom"

    symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symptom_name = db.Column(db.String(200))
    attack = db.relationship("Attack",
                                 backref=db.backref("symptom", order_by=symptom_id),
                                 secondary="attack_symptom")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Symptom symptom_id=%s symptom_type_name=%s>" % (
            self.symptom_id, self.symptom_name)


class AttackTrigger(db.Model):
    """ The Asthma attack and the list of id's of possible triggers."""
    __tablename__ = "attack_trigger"

    attack_triggger_id = db.Column(db.Integer, autoincrement=True,
                                             primary_key=True)
    attack_id = db.Column(db.Integer, db.ForeignKey('attack.attack_id'))
    possible_trigger_id = db.Column(db.Integer, db.ForeignKey('possible_trigger.possible_trigger_id'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<AttackTrigger attack_triggger_id=%s trigger_id=%s>" % (
            self.attack_triggger_id, self.attack_id, self.trigger_id)


class PossibleTrigger(db.Model):
    """ Possible trigger associated with the Asthma attack by name."""

    __tablename__ = "possible_trigger"

    possible_trigger_id = db.Column(db.Integer, autoincrement=True,
                                                 primary_key=True)
    possible_trigger_name = db.Column(db.String(200))
    possible_trigger_type = db.Column(db.String(200))
    attack = db.relationship("Attack",
                                    backref=db.backref("possible_trigger",
                                    order_by=possible_trigger_id),
                                    secondary="attack_trigger")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<PossibleTrigger possible_trigger_id=%s  possible_trigger_name=%s> possible_trigger_type=%s" % (
            self.possible_trigger_id, self.possible_trigger_name,
            self.possible_trigger_type)


#########################################################################

@app.route('/')
def index():
    """Site Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for profile creation."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process Registration."""

    unprocessed_email = request.form["email"]
    email = unprocessed_email.lower()
    first_name = request.form["first"]
    last_name = request.form["last"]
    clear_password = request.form["password"]

    password = SHA256.new(clear_password).hexdigest()

    age = int(request.form["age"])

    if User.query.filter_by(email=email).first():
        flash("You are already a user. Sign in.")
        return redirect("/login")

    else:
        new_user = User(email=email, first_name=first_name, last_name=last_name,
                        password=password, age=age)

        db.session.add(new_user)
        db.session.commit()

        flash("User Profile %s added." % email)
        return redirect("/login")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process the User's login."""

    unprocessed_email = request.form["email"]
    email = unprocessed_email.lower()
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    def check_password(password, hash_password):
        return SHA256.new(password).hexdigest() == hash_password

    if not user:
        flash("Password not found. Please Register.")
        return redirect("/login")

    if check_password(password, user.password) is False:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("%s, you are logged in." % user.first_name)
    return redirect("/user")


@app.route("/user", methods=['GET'])
def user_detail():
    """Show info about user."""

    colors_dict = {"Changes in the Weather": {"color": "#F7464A", "highlight": "#FF5A5E"},
                    "Physical Exertion": {"color": "#46BFBD", "highlight": "#5AD3D1"},
                    "Dust Mites": {"color": "#FDB45C", "highlight": "#FFC870"},
                    "Stress": {"color": "#a3f746", "highlight": "#46f79a"},
                    "Pollen": {"color": "#c28ffa", "highlight": "#9a46f7"},
                    "Smoke": {"color": "#464bf7", "highlight": "#46a3f7"},
                    "Seasonal Cold": {"color": "#000000", "highlight": "#819f70"},
                    "Medication": {"color": "#a7aeb8", "highlight": "#b9cce3"},
                    "Emotional Exertion": {"color": "#a73955", "highlight": "#b44359"},
                    "Strong Odors": {"color": "#b9e9ba", "highlight": "#c5edbb"}
                    }

    if "user_id" in session:

        user = User.query.get(session.get("user_id"))

        attacks = Attack.query.filter_by(user_id=session.get("user_id"))\
                                                        .order_by(Attack.attack_date)\
                                                        .all()

        triggers_list = []
        for attack in attacks:
            triggers_list.extend(attack.possible_trigger)

        triggers = [trigger.possible_trigger_name for trigger in triggers_list]
        triggers_count = Counter(triggers)

        data = []
        for trigger in triggers_count:
            d = {}
            d['value'] = triggers_count[trigger]
            d['highlight'] = colors_dict[trigger]["highlight"]
            d['color'] = colors_dict[trigger]["color"]
            d["label"] = trigger
            data.append(d)

        attacks = Attack.query.filter_by(user_id=session.get("user_id")).all()

        attack_count = [0]*12
        for attack in attacks:
            attack_month = int(attack.attack_date[5:7])
            attack_count[attack_month-1] += 1
        return render_template("user_detail.html", user=user,
                                                 attacks=attacks,
                                                attack_count=attack_count,
                                                data=data)
    else:

        return redirect('/')


@app.route("/attack", methods=["GET"])
def attack_form():
    """ Show attack input form."""

    user_info = User.query.get(session["user_id"])
    user_id = user_info.user_id

    return render_template("attack_submission.html", user_id=user_id)


@app.route("/attack", methods=['POST'])
def attack_process():
    """Process the User's new attack."""

    attack_date = request.form["date"]
    print attack_date
    attack_location = request.form["location"]
    user_info = User.query.get(session["user_id"])
    user_id = user_info.user_id

    attack = Attack(attack_date=attack_date,
                    attack_location=attack_location, user_id=user_id)

    db.session.add(attack)
    db.session.flush()

    attack_id = attack.attack_id

    symptoms = request.form.getlist("symptom")

    for symptom in symptoms:
        symptom_id = int(symptom)
        attack_symptom = AttackSymptom(attack_id=attack_id,
                                     symptom_id=symptom_id)
        db.session.add(attack_symptom)

    triggers = request.form.getlist("trigger")

    for trigger in triggers:
        possible_trigger_id = int(trigger)
        attack_trigger = AttackTrigger(attack_id=attack_id,
                                    possible_trigger_id=possible_trigger_id)
        db.session.add(attack_trigger)

    db.session.commit()

    attacks = Attack.query.filter_by(user_id=session.get("user_id")).all()

    attack_count = [0]*12
    for attack in attacks:
        attack_month = int(attack.attack_date[5:7])
        attack_count[attack_month-1] += 1
    print attack_count

    flash("Your incident has been added to your log.")
    return render_template("attack_info.html", user_id=user_id, attack=attack,
                                            attack_count=attack_count)



@app.route("/info/<int:attack_id>")
def show_info_about_attack(attack_id):
    """Showing information about a specific attack"""

    attack = Attack.query.get(attack_id)
    user_info = User.query.get(session["user_id"])
    user_id = user_info.user_id

    attacks = Attack.query.filter_by(user_id=session.get("user_id")).all()

    attack_count = [0]*12
    for a in attacks:
        attack_month = int(a.attack_date[5:7])
        attack_count[attack_month-1] += 1


    return render_template("attack_detail.html", attack=attack,
                                                 user_id=user_id,
                                                 attack_count=attack_count)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have successfully logged out.")
    return redirect("/")

if __name__ == "__main__":
    app.debug = True
    # connect_to_db(app)
    app.run()
