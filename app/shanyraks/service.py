from app.config import database
from .repository.repository import ShanyrakRepository

class Service:
    def __init__(self):
        self.repository = ShanyrakRepository(database)


def get_service():
    svc = Service()
    return svc

