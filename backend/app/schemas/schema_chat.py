from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

chat_schema = {
    "type": "object",
    "properties": {
        "room_key": {"type": "string"},
        "msg": {"type": "string"},
        "sender": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "nickname": {"type": "string"}
            }
        },
        "members": [{
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "read": {"type": "boolean"}
            }
        }],
        "timestamp": {"type": "string", "format": "date-time"}
    },
    "required": ["requester", "subject"],
    "additionalProperties": False
}
chat_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "members": [{
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "nickname": {"type": "string"},
                "unread": {"type": "number"}
            }
        }]
    },
    "required": ["title", "members"],
    "additionalProperties": False
}
new_chat_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "room_id": {"type": "string"},  # generated value
        "members": [{
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "nickname": {"type": "string"},
                "unread": {"type": "number"}
            }
        }]
    },
    "required": ["title", "members"],
    "additionalProperties": False
}


def validate_new_chat(data):
    try:
        validate(data, new_chat_schema)
    except ValidationError as e:
        return False, e
    except SchemaError as e:
        return False, e
    return True, data
