from typing import Dict
from typing import List
from typing import Union

from pydantic import BaseModel
from pydantic.types import StrictBool
from pydantic.types import StrictFloat
from pydantic.types import StrictInt
from pydantic.types import StrictStr
from pydantic_factories import ModelFactory


class IncorrectBodyTemplate(BaseModel):
    id: Union[StrictBool, StrictInt, StrictFloat, Dict, List, None]
    method: Union[StrictBool, StrictInt, StrictFloat, Dict, List, None]
    phone: Union[StrictBool, StrictInt, StrictFloat, Dict, List, None]


class IncorrectBodySecondFields(IncorrectBodyTemplate):
    name: Union[StrictBool, StrictInt, StrictFloat, Dict, List, None]
    surname: Union[StrictBool, StrictInt, StrictFloat, Dict, List, None]
    age: Union[StrictBool, StrictStr, StrictFloat, Dict, List, None]


class GeneratedWrongAddBody(ModelFactory):
    __model__ = IncorrectBodySecondFields


class GeneratedWrongDeleteBody(ModelFactory):
    __model__ = IncorrectBodyTemplate


class GeneratedWrongUpdateBody(ModelFactory):
    __model__ = IncorrectBodySecondFields


class GeneratedWrongSelectBody(ModelFactory):
    __model__ = IncorrectBodySecondFields
