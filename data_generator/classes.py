from firebase_admin import firestore
from data_generator.utils import fake, get_fake_datetime
from data_generator.abstracts import Entity
from datetime import timedelta
from random import randint


class Patient(Entity):
    def __init__(self):
        super().__init__(collection=u'patients')

        profile = fake.simple_profile()
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
            u'name': self.name,
            u'address': self.address,
            u'contactNumber': self.contactNumber,
            u'gender': self.gender,
            u'Pdetails': self.get_pdetails(),
            u'email': self.email
        }


class Medicine(Entity):
    def __init__(self):
        super().__init__(collection=u'medicines')

        self.code = fake.pystr(min_chars=10, max_chars=10)
        self.price = randint(10, 1000)
        self.quantity = randint(10, 100)

    def to_dict(self):
        return {
            u'code': self.code,
            u'price': self.price,
            u'quantity': self.quantity
        }

