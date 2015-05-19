""" Every Breath of the Way """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Attack, AttackSymptom, Symptom, AttackTrigger, PossibleTrigger

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

app.secret_key = "wheezer"

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

	new_user = User(email=email, first_name=first_name, last_name=last_name, password=password, age=age)

	db.session.add(new_user)
	db.session.commit()

	flash("User Profile %s added." % email)
	return redirect("/")

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

	print "testing"

	if not user:
	    flash("Password not found. Please Register.")
	    return redirect("/login")

	if user.password != password:
	    flash("Incorrect password")
	    return redirect("/login")

	session["user_id"] = user.user_id

	flash("Logged in")
	return redirect("/user/%s" % user.user_id)

@app.route("/user/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""
    user = User.query.get(user_id)
    return render_template("user_detail.html", user=user)

# I need to create an attack before I can see a list of attacks for the user

@app.route("/attack", methods=['POST'])
def attack_creation():
	"""Attack incident creation"""
	print request.form.getlist("trigger_name")
	print request.form.getlist("symptom")
	date = request.form["date"]
	location = request.form["location"]	
	attack_possible_triggers = request.form.getlist("trigger_name")
	symptom_type_name = request.form.getlist("symptom")
	new_attack = Attack(date=date, location=location, attack_possible_triggers= attack_possible_triggers)
	new_attack_symptoms = Symptom(symptom=symptom_name)
	new_attack_triggers = PossibleTrigger(trigger_name=possible_trigger_name)

	print new_attack_triggers
	print new_attack_symptoms
	print new_attack

	db.session.add(new_attack)
	db.session.add(new_attack_symptom)
	db.session.add(new_attack_triggers)
	db.session.commit()

	flash("Attack added.")
	return render_template("attack_submission.html")



@app.route('/list')
def attack_list():
	"""Show list of Asthma Attacks."""

	attack = Attack.query.orderby("attack_id").all()
	return render_template("list_user_attacks.html", attacks=attacks)

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


if __name__ == "__main__":
	app.debug = False

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run()
