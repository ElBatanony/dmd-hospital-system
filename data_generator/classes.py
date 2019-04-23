from firebase_admin import firestore
from data_generator.utils import fake, get_fake_datetime
from data_generator.abstracts import Entity
from datetime import timedelta, datetime
from random import randint
from random import choice

timeSlots = ["10:00-10:30", "10:30-11:00", "11:00-11:30", "11:30-12:00", "12:00-12:30", "12:30-13:00", "13:00-13:30",
             "13:30-14:00", "14:00-14:30", "14:30-15:00"]
statusSlots = ["pending", "approved", "declined"]
empRole = ["laboratorist", "nurse", "accountant", "pharmacist"]
medNamed = ["Aspirin", "Viagra", "Trimoll", "Citramon", "Nosh-pa", "Abakavir", "Azinoks", "Azaran",
            "Avaril", "Apap", "Zantak", "Zivox", "Zinerit", "Zitrek", "Zodak", "Imidil",
            "Imuran", "Indap", "Itrazol", "Kagocel", "Kanizon", "Ketoph", "Klemastin"]
medPrice = {"Aspirin": 1000, "Viagra": 250, "Trimoll": 350, "Citramon": 20, "Nosh-pa": 320, "Abakavir": 1500, "Azinoks": 800, "Azaran": 440,
            "Avaril": 880, "Apap": 35, "Zantak": 175, "Zivox": 220, "Zinerit": 270, "Zitrek": 950, "Zodak": 720, "Imidil": 910,
            "Imuran": 1000, "Indap": 1200, "Itrazol": 40, "Kagocel": 2000, "Kanizon": 255, "Ketoph": 90, "Klemastin": 140}
cashed_collections = {}


def get_collection(db: firestore, collection):
    if collection in cashed_collections:
        return cashed_collections[collection]
    docs = db.collection(collection).stream()
    arr = []
    for doc in docs:
        arr.append(doc)  # doc.id  doc.to_dict()['role']
    cashed_collections[collection] = arr
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
        self.medList = []

    def to_dict(self):
        return {
            u'name': self.name,
            u'address': self.address,
            u'contactNumber': self.contactNumber,
            u'gender': self.gender,
            u'email': self.email,
            u'medList': self.medList,
        }


class Medicine(Entity):
    def __init__(self, db):
        super().__init__(db=db, collection=u'medicines')

        self.expDate = get_fake_datetime(datetime.now(), datetime.now() + timedelta(days=120))
        self.sold = False
        self.name = choice(medNamed)
        self.price = medPrice[self.name]
        self.quantity = randint(10, 100)

    def to_dict(self):
        return {
            u'expDate': self.expDate,
            u'sold': self.sold,
            u'name': self.name,
            u'price': self.price,
            u'quantity': self.quantity
        }


class Employee(Entity):
    def __init__(self, db, role="others"):
        super().__init__(db=db, collection=u'employees')

        profile = fake.simple_profile()
        self.name = profile['name']
        self.contactNumber = fake.phone_number()
        self.gender = profile['sex']
        self.address = profile['address']
        self.salary = randint(1200, 3600) * 10
        if role == "doctor":
            self.role = role
        elif role == "others":
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

        colPat = get_collection(db, "patients")
        # arr = []
        # for doc in col:
        #     arr.append(doc)
        patient = choice(colPat)
        self.patient = patient.reference
        colDoc = get_collection(db, "employees")
        arr = get_by_condition(colDoc, "role", "doctor")
        doctor = choice(arr)
        self.doctor = doctor.reference
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
        colNur = get_collection(db, "employees")
        arr = get_by_condition(colNur, "role", "nurse")
        nurse = choice(arr)
        self.nurse = nurse.reference
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
        self.date = get_fake_datetime()
        self.testResult = choice(["positive", "negative"])
        self.testType = "Urin"
        colLab = get_collection(db, "employees")
        arr = get_by_condition(colLab, "role", "laboratorist")
        lab = choice(arr)
        self.laboratorist = lab.reference
        colPat = get_collection(db, "patients")
        patient = choice(colPat)
        self.patient = patient.reference
        colNur = get_collection(db, "employees")
        arr = get_by_condition(colNur, "role", "nurse")
        nurse = choice(arr)
        self.nurse = nurse.reference

    def to_dict(self):
        return {
            u'date': self.date,
            u'testResult': self.testResult,
            u'testType': self.testType,
            u'laboratorist': self.laboratorist,
            u'patient': self.patient,
            u'requester': self.nurse,
        }


class Prescription(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'prescriptions')
        self.date = get_fake_datetime()
        self.description = "some test here"
        colDoc = get_collection(db, "employees")
        arr = get_by_condition(colDoc, "role", "doctor")
        doctor = choice(arr)
        self.doctor = doctor.reference
        colPat = get_collection(db, "patients")
        patient = choice(colPat)
        self.patient = patient.reference
        arrBill = []
        medList = []
        for i in range(1, randint(1, 5)):
            colMed = get_collection(db, "medicines")
            med = choice(colMed).to_dict()
            obj = {
                'name': med['name'],
                'price': med['price'],
                'quantity': randint(1, 10),
            }
            medList.append(obj)
        colBill = get_collection(db, "bills")
        for i in range(0, len(medList)):
            arrBill.append(choice(colBill).reference)

        # for unit in medList:
        #     obj = {
        #         'buyer': unit.get('name'),
        #         'date': get_fake_datetime(),
        #         'medList': medList,
        #     }
        #     arrBill.append(obj)
        self.bills = arrBill
        self.medList = medList

    def to_dict(self):
        return {
            u'date': self.date,
            u'description': self.description,
            u'doctor': self.doctor,
            u'patient': self.patient,
            u'bills': self.bills,
            u'medList': self.medList
        }


class RoomAssign(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'room_assignment')
        self.dateAddmitted = get_fake_datetime()
        self.dateDischarged = self.dateAddmitted + timedelta(days=randint(1, 5))
        colPat = get_collection(db, "patients")
        patient = choice(colPat)
        self.patient = patient.reference
        colRoom = get_collection(db, "rooms")
        room = choice(colRoom)
        self.room = room.reference

    def to_dict(self):
        return {
            u'date_admitted': self.dateAddmitted,
            u'date_discharged': self.dateDischarged,
            u'patient': self.patient,
            u'room': self.room
        }


class Bill(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'bills')
        self.date = get_fake_datetime()
        colPat = get_collection(db, "patients")
        patient = choice(colPat)
        self.buyer = patient.reference
        colRoom = get_collection(db, "medicines")
        meds = []
        for i in range(0, randint(1, 10)):
            meds.append(choice(colRoom).reference)
        self.medList = meds

    def to_dict(self):
        return {
            u'date': self.date,
            u'buyer': self.buyer,
            u'medList': self.medList,
        }


class Chat(Entity):
    def __init__(self, db: firestore):
        super().__init__(db=db, collection=u'chats')
        col = get_collection(db, "patients")
        patient = choice(col)
        self.patient = patient.reference
        col = get_collection(db, "employees")
        arr = get_by_condition(col, "role", "doctor")
        doctor = choice(arr)
        self.doctor = doctor.reference
        msg = []
        for i in range(1, randint(1, 15)):
            obj = {
                'data': get_fake_datetime(),
                'test': "oneyne ame",
                'sender': choice(["doctor", "patient"]),
            }
            msg.append(obj)
        self.messages = msg

    def to_dict(self):
        return {
            u'patient': self.patient,
            u'doctor': self.doctor,
            u'messages': self.messages,
        }
