""" Utility file to seed breathe database"""

import datetime
 
from model import User, Attack, AttackSymptom, Symptom, AttackTrigger, PossibleTrigger, TriggerType, connect_to_db, db
from server import app

def load_triggers():
	"""Load triggers from u.triggers into database."""

	triggers_file = open("seed_data/u.triggers")

	for row in triggers_file:
		possible_trigger_name, possible_trigger_type = row.split("|")

		trigger = PossibleTrigger(possible_trigger_name=possible_trigger_name
									possible_trigger_type=possible_trigger_type)
		db.session.add(trigger)
	db.session.commit()		

			

def load_symptoms():
	"""Load symptoms from u.symptoms into database."""

	symptoms_file = open("seed_data/u.symptoms")

	for row in symptoms_file:
		symptom_name =row.rstrip()

		symptom = Symptom(symptom_name=symptom_name)
		db.session.add(symptom)
	db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_triggers()
    load_symptoms()
	



