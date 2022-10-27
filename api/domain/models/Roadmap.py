import uuid
from datetime import datetime
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Roadmap:
    id: str
    author_username: str
    title: str
    description: str
    coordinates: list[list[float, float]]
    tags: list[str]
    created_date: datetime
    likes: int
    deslikes: int

def roadmap_factory(
        author_username: str, 
        title: str, description: str, 
        coordinates: list[list[float, float]], 
        tags: list[str], 
        created: datetime = None, 
        likes: int = 0,
        deslikes: int = 0
    ) -> Roadmap:

    created_date = created or datetime.now()
    return Roadmap(
        id=str(uuid.uuid4()),
        author_username=author_username,
        title=title,
        description=description,
        coordinates=coordinates,
        tags=tags,
        created_date=created_date,
        likes=likes,
        deslikes=deslikes
    )
