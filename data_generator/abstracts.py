from abc import ABC, abstractmethod
from firebase_admin import firestore


class Entity(ABC):

    def __init__(self, collection=None):
        self.id = None
        self.collection = collection

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def post_action(self):
        pass

    def save(self, db: firestore):
        doc = db.collection(self.collection).document()
        self.id = doc.id
        doc.set(self.to_dict())
        self.post_action()
