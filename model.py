""" ORM - Models and database function for Every Breath of the Way Project"""

from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

db = SQLAlchemy()

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


####################################################################
def connect_to_db(app):
    """Connect the database to my Flask app."""

    DATABASE_URL = os.environ.get("DATABASE_URL", )
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
