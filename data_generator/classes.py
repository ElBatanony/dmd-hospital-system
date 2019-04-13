from firebase_admin import firestore
from data_generator.utils import fake, get_fake_datetime
from data_generator.abstracts import Entity
from datetime import timedelta
from random import randint


class Patient(Entity):
    def __init__(self):
        profile = fake.simple_profile()
        self.collection = u'patients'
        self.PID = None
        self.name = profile['name']
        self.contactNumber = fake.phone_number()
        self.email = profile['mail']
        self.gender = profile['sex']
        self.address = profile['address']
        self.dateAdmitted = get_fake_datetime()
        self.dateDischarged = get_fake_datetime(start=self.dateAdmitted, end=self.dateAdmitted + timedelta(days=7))

    def get_pdetails(self):
        return {
            'dateAdmitted': self.dateAdmitted,
            'dateDischarged': self.dateDischarged
        }

    def to_dict(self):
        return {
            u'PID': self.PID,
            u'name': self.name,
            u'address': self.address,
            u'contactNumber': self.contactNumber,
            u'gender': self.gender,
            u'Pdetails': self.get_pdetails(),
            u'email': self.email
        }

    def save(self, db: firestore):
        doc = db.collection(self.collection).document()
        self.PID = doc.id
        doc.set(self.to_dict())


class Medicine(Entity):
    def __init__(self):
        self.collection = u'medicines'
        self.code = None
        self.price = randint(10, 1000)
        self.quantity = randint(10, 100)

    def to_dict(self):
        return {
            u'code': self.code,
            u'price': self.price,
            u'quantity': self.quantity
        }

    def save(self, db: firestore):
        doc = db.collection(self.collection).document()
        self.code = doc.id
        doc.set(self.to_dict())

