from typing import List
from typing import Literal

from pydantic import BaseModel
from pydantic.types import StrictInt
from pydantic.types import StrictStr
from pydantic.types import constr


class SuccessResponseTemplate(BaseModel):
    id: constr(regex=r"[a-z]{3,5}-[0-9]{3,5}-[0-9]{3,5}-[a-z]{3,5}")
    method: Literal[""]
    status: Literal["success"]


class AddResponse(SuccessResponseTemplate):
    method: Literal["add"]


class DeleteResponse(SuccessResponseTemplate):
    method: Literal["delete"]


class UpdateResponse(SuccessResponseTemplate):
    method: Literal["update"]


class UpdateResponseFailure(UpdateResponse):
    status: Literal['failure']


class User(BaseModel):
    name: StrictStr
    surname: StrictStr
    age: StrictInt
    phone: StrictStr


class SelectResponseSuccess(SuccessResponseTemplate):
    method: Literal["select"]
    users: List[User]


class SelectResponseFailure(SelectResponseSuccess):
    status: Literal["failure"]


class FailureResponse(BaseModel):
    id: constr(regex=r"[a-z]{3,5}-[0-9]{3,5}-[0-9]{3,5}-[a-z]{3,5}")
    status: Literal["failure"]
    reason: StrictStr
