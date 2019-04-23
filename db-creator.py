import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from data_generator import SampleDatabase


def establish_creds():
    # Use a service account
    cred = credentials.Certificate('cred.json')
    firebase_admin.initialize_app(cred)


def main():
    establish_creds()
    db = firestore.client()
    # db.collection('employees').document('weionerio').set({'name': 'rvbero'})
    # params = {
    #     'patients': 10,
    #     'doctors': 5,
    #     'others': 5,
    #     'medicines': 10,
    #     'records': 20,
    #     'rooms': 20,
    #     'reports': 3,
    #     'prescriptions': 4,
    #     'roomAssings': 7,
    #     'bills': 7,
    #     'chats': 2,
    # }
    # database = SampleDatabase(db=db, **params)
    database = SampleDatabase(db=db)
    database.generate()
    print("The database is generated and saved in Firestore")


if __name__ == "__main__":
    main()
