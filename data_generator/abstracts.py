from abc import ABC, abstractmethod
from firebase_admin import firestore


class Entity(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def save(self, db: firestore):
        pass
