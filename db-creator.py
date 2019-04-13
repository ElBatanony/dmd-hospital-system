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
    params = {
        'patients': 1,
        'medicines': 1,
    }
    database = SampleDatabase(db=db, **params)
    database.generate()
    print("The database is generated and saved in Firestore")


if __name__ == "__main__":
    main()
