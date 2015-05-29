""" Every Breath of the Way """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Attack, AttackSymptom, Symptom, AttackTrigger, PossibleTrigger

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

app.secret_key = "wheeze89798ew7hjyas98798798sdhui7987s987bhghjg987r"


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
    password = request.form["password"]
    age = int(request.form["age"])

    if User.query.filter_by(email=email).first():
        flash("You are already a user. Sign in.")
        return redirect("/login")

    else:
        new_user = User(email=email, first_name=first_name, last_name=last_name, password=password, age=age)

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

    if not user:
        flash("Password not found. Please Register.")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("%s, you are logged in." % user.first_name)
    return redirect("/user/%s" % user.user_id)


@app.route("/user/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    attacks = Attack.query.filter_by(user_id=session.get("user_id")).order_by(Attack.attack_date).all()
    return render_template("user_detail.html", user=user, attacks=attacks)


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
    attack_location = request.form["location"]
    user_info = User.query.get(session["user_id"])
    user_id = user_info.user_id

    attack = Attack(attack_date=attack_date, attack_location=attack_location, user_id=user_id)

    db.session.add(attack)
    db.session.flush()

    print attack.attack_id
    attack_id = attack.attack_id

    print request.form.getlist("trigger")
    print request.form.getlist("symptom")
    print attack_location
    print attack_date

    symptoms = request.form.getlist("symptom")

    for symptom in symptoms:
        symptom_id = int(symptom)
        attack_symptom = AttackSymptom(attack_id=attack_id, symptom_id=symptom_id)
        db.session.add(attack_symptom)

    triggers = request.form.getlist("trigger")

    for trigger in triggers:
        possible_trigger_id = int(trigger)
        attack_trigger = AttackTrigger(attack_id=attack_id, possible_trigger_id=possible_trigger_id)
        db.session.add(attack_trigger)

    db.session.commit()

    # attack_month = attack_date[5:7]
    # print "this is the" + attack_month
    # print attack_month

    attacks = Attack.query.filter_by(user_id=session.get("user_id")).all()

    attack_count = [0]*12
    for attack in attacks:
        attack_month = int(attack.attack_date[5:7])
        attack_count[attack_month-1] += 1
    print attack_count


    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

    flash("Your attack has been added.")
    return render_template("attack_info.html", user_id=user_id)


@app.route("/attack/edit", methods="POST")
def edit_attack(attack_id):
    """ Edit and existing attack"""

    return


@app.route("/info/<int:attack_id>")
def show_info_about_attack(attack_id):
    """Showing information about a specific attack"""

    attack = Attack.query.get(attack_id)
    user_info = User.query.get(session["user_id"])
    user_id = user_info.user_id
    return render_template("attack_detail.html", attack=attack, user_id=user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("You have successfully logged out.")
    return redirect("/")


if __name__ == "__main__":
    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()
