""" Every Breath of the Way """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Attack, Attack_Symptom, Symptom, Attack_Trigger, Possible_Trigger, Trigger_Type

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

	email = request.form["email"]
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

	email = request.form["email"]
	password = request.form["password"]

	user = User.query.filter_by(email=email).first()

	print user

	if not user:
	    flash("No such user, please register")
	    return redirect("/login")

	if user.password != password:
	    flash("Incorrect password")
	    return redirect("/login")

	session["user_id"] = user.user_id

	flash("Logged in")
	return redirect("/users/%s" % user.user_id)


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





