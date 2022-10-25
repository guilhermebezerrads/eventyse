import uuid
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class User:
    id: str
    name: str
    username: str
    password_hash: str
    password_salt: str
    followers_counter: int
    following_counter: int

def user_factory(name: str, username: str, password_hash: bytes, password_salt: bytes, followers_counter: int = 0, following_counter: int = 0) -> User:
    return User(
        id=str(uuid.uuid4()),
        name=name,
        username=username,
        password_hash=password_hash.decode(),
        password_salt=password_salt.decode(),
        followers_counter=followers_counter,
        following_counter=following_counter
    )
