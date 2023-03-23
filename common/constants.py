ADD_UPDATE_REQUIRED_PARAMS = ["id", "method", "name", "surname", "phone", "age"]

DELETE_REQUIRED_PARAMS = ["id", "method", "phone"]

SELECT_REQUIRED_PARAMS = ["id", "method", "phone", "name", "surname"]

STRING_ADD_UPDATE_PARAMS = ["id", "method", "name", "surname", "phone"]

STRING_DELETE_PARAMS = ["id", "method", "phone"]

INT_PARAMS = ["age"]

WRONG_DATA_TYPES = ["string", 123, 12.01, True, None, []]

STRING_INCORRECT_DATA_TYPES = [True, 10, 124.13, {"foo": "bar"}, ["foo", "bar"], None]

INT_INCORRECT_DATA_TYPES = [True, 124.13, "foo", {"foo": "bar"}, ["foo", "bar"], None]
