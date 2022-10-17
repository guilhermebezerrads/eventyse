import uuid

class User:
    def __init__(self, name: str, username: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.name: str = name
        self.username: str = username
        self.followers: int = 0
        self.following: int = 0
