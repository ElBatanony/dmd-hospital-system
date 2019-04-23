from abc import ABC, abstractmethod
from firebase_admin import firestore


class Entity(ABC):

    def __init__(self, db=None, collection=None):
        self.id = None
        self.db = db
        self.collection = collection

    @abstractmethod
    def to_dict(self):
        pass

    def post_action(self):
        pass

    def save(self, db: firestore, batch):
        doc = db.collection(self.collection).document()
        self.id = doc.id
        # doc.set(self.to_dict())
        batch.set(doc, self.to_dict())
        self.post_action()
