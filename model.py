""" Models and database function for Every Breath of the Way Project"""


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
	""" User of Every Breath of the Way website."""

	__tablename__ = "user"

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(64), nullable=False)
	password = db.Column(db.String(64), nullable=False)
	first_name = db.Column(db.String(64), nullable=False)
	last_name = db.Column(db.String(64), nullable=False)
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

	user = db.relationship("User",
							backref=db.backref("attack", order_by=attack_id))


	def __repr__(self):
		"""Providing some helpful representation when printed for asthma attacks."""

		return "<Attack attack_id=%s attack_location=%s attack_possible_triggers=%s  user_id=%s>" % (
			self.attack_id, self.attack_location, self.attack_possible_triggers, self.user_id)

class Attack_Symptom(db.Model):
	""" The Asthma Attack and the list of symptoms associated with the attack."""

	__tablename__ = "attack_symptom"

	attack_symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	attack_id = db.Column(db.Integer, db.ForeignKey('attack.attack_id'))
	symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.symptom_id'))

	attack = db.relationship("Attack",
								backref=db.backref("attack_symptom", order_by=attack_symptom_id))

	symptom = db.relationship("Symptom",
								backref=db.backref("attack_symptom", order_by=attack_symptom_id))

	def __repr__(self):
		""" Providing some helpful representation when printed for attacks and related 
		symptom."""

		return "<Attack_Symptom attack_symptom_id=%s attack_id=%s symptom_id=%s>" % (
			self.attack_symptom_id, self.attack_id, self.symptom_id)

class Symptom(db.Model):
	"""A symptom associated with an attack by type. """

	__tablename__  = "symptom"

	symptom_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	symptom_type_name = db.Column(db.String(64))
	attack_id = db.Column(db.Integer, db.ForeignKey('attack.attack_id'))

	attack = db.relationship("Attack",
								backref=db.backref("symptom", order_by=symptom_id))

	def __repr__(self):
		""" Providing some helpful representation when printed for symptom type name,
		 and attack"""

		return "<Symptom symptom_id=%s symptom_type_name=%s attack_id=%s>" % (
			self.symptom_id, self.symptom_type_name, self.attack_id)

			
class Attack_Trigger(db.Model):
	""" The Asthma attack and the list of id's of possible triggers associated with the attack."""

	__tablename__ = "attack_trigger"

	attack_triggger_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	attack_id = db.Column(db.Integer, db.ForeignKey('attack.attack_id'))
	possible_trigger_id = db.Column(db.Integer, db.ForeignKey('possible_trigger.possible_trigger_id'))

	attack = db.relationship("Attack", 
									backref=db.backref("attack_trigger", order_by=attack_triggger_id))

	possible_trigger = db.relationship("Possible_Trigger", 
										backref=db.backref("attack_trigger", order_by=attack_triggger_id))

	def __repr__(self):
		"""Providing some helpful representation when printed for attacks and related list of
		 possible triggers."""

		return "<Attack_Trigger attack_triggger_id=%s attack_id=%s trigger_id=%s>" % (
			self.attack_triggger_id, self.attack_id, self.trigger_id)

		

class Possible_Trigger(db.Model):
	""" Possible trigger associated with the Asthma attack by name."""

	__tablename__ = "possible_trigger"

	possible_trigger_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	possible_trigger_name = db.Column(db.String(64))
	possible_trigger_type_id = db.Column(db.Integer, db.ForeignKey('trigger_type.trigger_type_id'))

	trigger_type = db.relationship("Trigger_Type", 
											backref=db.backref("possible_trigger", order_by=possible_trigger_id))


	def __repr__(self):
		"""Providing some helpful representation when printed for attacks and the names of triggers."""

		return "<Possible_Trigger possible_trigger_id=%s  possible_trigger_name=%s possible_trigger_type_id=%s>" % (
			self.possible_trigger_id, self.possible_trigger_name, self.possible_trigger_type_id)
		

class Trigger_Type(db.Model):	
	""" The name of the types of possible triggers"""

	__tablename__ = "trigger_type"

	trigger_type_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	trigger_type_name = db.Column(db.String(64))

	def _repr__(self):
		""" Possible trigger associated with the Asthma attack by  trigger name. """

		return "<Trigger_Type trigger_type_id=%s  trigger_type_name=%s>" % (
			self.trigger_type_id, self.trigger_type_name)



####################################################################
def connect_to_db(app):
    """Connect the database to my Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///breathe.db' #have to put my db name
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
   

	from server import app
	connect_to_db(app)
	print "Connected to DB."




