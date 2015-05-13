from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

################################################################################################
 
# User Definitions

class User(db.Model):
	""" User of Every Breath of the Way website."""

	__tablename__ = "user"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(64), nullable=False)
	password = db.Column(db.String(64) nullable=False)
	first_name = db.Column(db.String(64) nullable=False)
	last_name = db.Column(db.String(64) nullable=False)
	age = db.Column(db.String(15), nullable=False)

	def __repr__(self):
		"""Providing some helpful representation when printed for user profile."""

		return "<User user_id=%s email=%s password=%s first_name=%s last_name=%s age=%s>" % (
			self.user_id, self.email, self.password, self.first_name, self.last_name, self.age)

class Attack(db.Model):
	""" An instance of a User's asthma attack"""

	__tablename__ = "attack"

	attack_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	attack_date = db.Column(db.DateTime, nullable=False)
	attack_location = db.Column(db.String(64), nullable=False)
	attack_possible_triggers = db.Column(db.String(64), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

	#must define the relationships ie
	# user = db.relationship("User",
	# 						backref=db.backref("ratings", order_by=rating_id))

 #    # Define relationship to movie
 #    movie = db.relationship("Movie",
 #                            backref=db.backref("ratings", order_by=rating_id))


	def __repr__(self):
		"""Providing some helpful representation when printed for asthma attacks."""

		return "<Attack attack_id=%s attack_location=%s attack_possible_triggers=%s  user_id=%s>" % (
			self.attack_id, self.attack_location, self.attack_possible_triggers, self.user_id)

class Attack_Symptom(db.Model):
		""" This is the bridge between the Asthma Attack and the list of associated systems."""

	__tablename__ = "attack_symptom"

	attack_symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	attack_id = db.Column(db.integer, db.ForeignKey('attack.attack_id'))
	symptom_id = db.Column(db.integer, db.ForeignKey('symptom.symptom_id'))

	# TO DO: define the relationship ###############################################

	def __repr__(self):
		""" Providing some helpful representation when printed for attacks and related symptom."""

		return "<Attack_Symptom attack_symptom_id=%s attack_id=%s symptom_id=%s>" % (
			self.attack_symptom_id, self.attack_id, self.symptom_id)

class Symptom(db.Model):
	"""A symptom associated with an attack. """

	__tablename__  = "symptom"

	symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	symptom_type_name = db.Column(db.String(64))
	attack_id = db.Column(db.Integer, db.ForeignKey('attack.attack_id'))

	def __repr__(self):
		""" Providing some helpful representation when printed for symptom type name, and attack"""

		return "<Symptom symptom_id=%s symptom_type_name=%s attack_id=%s" % (
			self.symptom_id, self.symptom_type_name, self.attack_id)
	#To do- define relationships		



