from typing import Literal

from pydantic import BaseModel
from pydantic.types import StrictInt
from pydantic.types import StrictStr
from pydantic.types import constr
from pydantic_factories import ModelFactory


class TemplateBody(BaseModel):
    id: constr(regex=r"[a-z]{3,5}-[0-9]{3,5}-[0-9]{3,5}-[a-z]{3,5}")


class AddBody(TemplateBody):
    method: Literal["add"]
    name: constr(regex=r"[a-z]{1,5}")
    surname: constr(regex=r"[a-z]{1,5}")
    phone: constr(regex=r"\d{8}")
    age: StrictInt


class DeleteBody(TemplateBody):
    method: Literal["delete"]
    phone: constr(regex=r"\d{8}")


class UpdateBody(TemplateBody):
    method: Literal["update"]
    name: StrictStr
    surname: StrictStr
    phone: constr(regex=r"\d{8}")
    age: StrictInt


class SelectBody(TemplateBody):
    method: Literal["select"]
    name: constr(regex=r"[a-z]{1,5}")
    surname: constr(regex=r"[a-z]{1,5}")
    phone: constr(regex=r"\d{8}")


class GeneratedAddBody(ModelFactory):
    __model__ = AddBody


class GeneratedDeleteBody(ModelFactory):
    __model__ = DeleteBody


class GeneratedUpdateBody(ModelFactory):
    __model__ = UpdateBody


class GeneratedSelectBody(ModelFactory):
    __model__ = SelectBody
