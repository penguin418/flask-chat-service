from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "password": {
            "type": "string",
            "minLength": 1
        },
        "username":{
            "type": "string",
            "minLength": 1
        }
    },
    "required": ["email", "password", "username"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return False, e
    except SchemaError as e:
        return False, e
    return True, data