from firebase_admin import firestore
from data_generator.utils import fake, get_fake_datetime
from data_generator.abstracts import Entity
from datetime import timedelta, datetime
from random import randint
from random import choice

timeSlots = ["10:00-10:30", "10:30-11:00", "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-13:00", "13:00-13:30",
             "13:30-14:00", "14:00-14:30", "14:30-15:00"]
statusSlots = ["pending", "approved", "declined"]
empRole = ["doctor", "laboratorist", "nurse", "accountant", "pharmacist"]
medNamed = ["Aspirin", "Viagra"]


def get_collection(db: firestore, collection):
    docs = db.collection(collection).stream()
    arr = []
    for doc in docs:
        arr.append(doc)  # doc.id  doc.to_dict()['role']
    return arr


def get_by_condition(arr, key, value):
    return [doc for doc in arr if doc.to_dict()[key] == value]


class Patient(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'patients')

        profile = fake.simple_profile()
        self.name = profile['name']
        self.contactNumber = fake.phone_number()
        self.email = profile['mail']
        self.gender = profile['sex']
        self.address = profile['address']
        # self.dateAdmitted = get_fake_datetime()
        # self.dateDischarged = get_fake_datetime(start=self.dateAdmitted, end=self.dateAdmitted + timedelta(days=7))

    # def get_pdetails(self):
    #     return {
    #         'dateAdmitted': self.dateAdmitted,
    #         'dateDischarged': self.dateDischarged
    #     }

    def to_dict(self):
        return {
            u'name': self.name,
            u'address': self.address,
            u'contactNumber': self.contactNumber,
            u'gender': self.gender,
            # u'Pdetails': self.get_pdetails(),
            u'email': self.email
        }


class Medicine(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'medicines')

        self.expDate = get_fake_datetime(datetime.now(), datetime.now() + timedelta(days=120))
        self.name = choice(medNamed)
        self.price = randint(1, 100) * 10
        self.quantity = randint(10, 100)

    def to_dict(self):
        return {
            u'expDate': self.expDate,
            u'name': self.name,
            u'price': self.price,
            u'quantity': self.quantity
        }


class Employee(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'employees')

        profile = fake.simple_profile()
        self.name = profile['name']
        self.contactNumber = fake.phone_number()
        self.gender = profile['sex']
        self.address = profile['address']
        self.salary = randint(12, 36) * 1000
        self.role = choice(empRole)
        if self.role == "doctor":
            self.status = "permanent"

    def to_dict(self):
        result = {
            u'name': self.name,
            u'address': self.address,
            u'contactNumber': self.contactNumber,
            u'gender': self.gender,
            u'salary': self.salary,
            u'role': self.role,
        }
        if self.role == "doctor":
            result[u'status'] = self.status
        return result


class Record(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'records')

        col = get_collection(db, "patients")
        arr = []
        for doc in col:
            arr.append(doc)
        patient = choice(arr)
        col = get_collection(db, "employees")
        arr = get_by_condition(col, "role", "doctor")
        doctor = choice(arr)
        self.patient = db.collection('patients').document(patient.id)
        self.doctor = db.collection('employees').document(doctor.id)
        self.description = "imagine some text here"
        self.date = get_fake_datetime()
        self.status = choice(statusSlots)
        self.timeSlot = choice(timeSlots)

    def to_dict(self):
        return {
            u'patient': self.patient,
            u'doctor': self.doctor,
            u'description': self.description,
            u'date': self.date,
            u'status': self.status,
            u'timeSlot': self.timeSlot
        }


class Room(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'rooms')

        self.free = True
        self.roomType = choice(["basic", "luxury", "economic"])
        col = get_collection(db, "employees")
        arr = get_by_condition(col, "role", "nurse")
        nurse = choice(arr)
        self.nurse = db.collection('employees').document(nurse.id)
        self.roomNumber = randint(1, 1000)

    def to_dict(self):
        return {
            u'free': self.free,
            u'roomType': self.roomType,
            u'nurse': self.nurse,
            u'roomNumber': self.roomNumber
        }


class Report(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'reports')
        self.testResult = choice(["positive", "negative"])
        self.testType = "Urin"
        col = get_collection(db, "employees")
        arr = get_by_condition(col, "role", "laboratorist")
        lab = choice(arr)
        self.laboratorist = db.collection('employees').document(lab.id)
        col = get_collection(db, "patients")
        patient = choice(col)
        self.patient = db.collection('patients').document(patient.id)

    def to_dict(self):
        return {
            u'testResult': self.testResult,
            u'testType': self.testType,
            u'laboratorist': self.laboratorist,
            u'patient': self.patient
        }
