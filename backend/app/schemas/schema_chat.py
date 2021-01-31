from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

chat_room_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "members": {
            "type": "array",
            "items": {"$ref": "#/definitions/user"}
        }
    },
    "required": ["title", "members"],
    "additionalProperties": False,
    "definitions": {
        "user": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "nickname": {"type": "string"}  # original name
            }
        }
    }
}
msg_schema = {
    "type": "object",
    "properties": {
        "room_id": {"type": "string"},
        "msg": {"type": "string"},
        "sender": {"type": "string"},
        "members": {
            "type": "array",
            "items": {"type": "string"}
        },
        "timestamp": {"type": "string", "format": "utc-millisec"}
    },
    "required": ["room_id", "msg", "sender", "members"],
    "additionalProperties": False
}

def validate_new_room(data):
    try:
        validate(data, chat_room_schema)
    except ValidationError as e:
        return False, e
    except SchemaError as e:
        return False, e
    return True, data

def validate_new_msg(data):
    try:
        validate(data, msg_schema)
    except ValidationError as e:
        return False, e
    except SchemaError as e:
        return False, e
    return True, data