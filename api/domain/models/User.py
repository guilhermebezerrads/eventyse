import uuid
from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

from domain.models.Post import Post

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class User:
    name: str
    username: str
    password_hash: str
    password_salt: str
    posts: List[Post]
    followers: int = 0
    following: int = 0
    id: str = str(uuid.uuid4())
