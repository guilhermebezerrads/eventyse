from dataclasses_json import dataclass_json,LetterCase
from dataclasses import dataclass
import json

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Error:
    message: str