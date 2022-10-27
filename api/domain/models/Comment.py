import uuid
from datetime import datetime
from dataclasses_json import dataclass_json, LetterCase
from dataclasses import dataclass

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Comment:
    id: str
    author_username: str
    roadmap_id: str
    text: str
    created_date: datetime

def comment_factory(author_username: str, roadmap_id: str, text: str, created: datetime = None) -> Comment:
    created_date = created or datetime.now()
    return Comment(
        id=str(uuid.uuid4()),
        author_username=author_username,
        roadmap_id=roadmap_id,
        text=text,
        created_date=created_date,
    )
