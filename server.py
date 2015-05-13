""" Every Breath of the Way """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Attack, Attack_Symptom, Symptom, Attack_Trigger, Possible_Trigger, Trigger_Type

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined


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
	"""Process Registration"""

	email = request.form["email"]
	first_name = request.form["first"]
	last_name = request.form["last"]
	password = request.form["password"]
	age = int(request.form["age"])
	
	new_user = User(email=email, first_name=fname, last_name=lname, password=password, age=age)

	db.session.add(new_user)
	db.session.commit()

	flash("User Profile %s added." % email)
	return redirect("/")















if __name__ == "__main__":
	app.debug = True

	connect_to_db(app)

	DebugToolbarExtension(app)

	app.run()





