from abc import ABC
from sqlalchemy.orm import Session

class IDatabase(ABC):
    session: Session
