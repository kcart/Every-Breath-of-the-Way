""" Every Breath of the Way """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session


app = Flask(__name__)

app.secret_key = "Wheezy"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
	"""Site Homepage."""

	return render_template("homepage.html")


 # Running into  template rendering issue for the registration form 
@app.route('/register', methods=['GET'])
def register_form():
	"""Show form for profile creation."""

	return render_template("register_form.html")

@app.route('/register', methods=['POST'])
def register_process():
	"""Process Registration"""

	email = request.form["email"]
	fname = request.form["first"]
	lname = request.form["last"]
	password = request.form["password"]
	age = int(request.form["age"])
	
	new_user = User(email=email, 
					fname=fname,
					lname=lname,
					password=password,
					age=age)

	db.session.add(new_user)
	db.session.commit()

	flash("User Profile %s added." % email)
	return redirect("/")


















if __name__ == "__main__":
	app.run(debug=True)