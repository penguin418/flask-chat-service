from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

from backend.app.schemas.validator import validate_schema

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

full_msg_schema = {
    "type": "object",
    "properties": {
        "room_id": {"type": "string"},
        "msg": {"type": "string"},
        "sender": {"type": "string"},
        "members": {
            "type": "array",
            "items": {"$ref": "#/definitions/receiver"}
        },
        "timestamp": {"type": "string", "format": "utc-millisec"}
    },
    "required": ["room_id", "msg", "sender", "members"],
    "additionalProperties": False,
    "definitions": {
        "receiver": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "read": {"type": "boolean"}
            }
        }
    }
}

new_msg_schema = {
    "type": "object",
    "properties": {
        "room_id": {"type": "string"},
        "msg": {"type": "string"},
        "sender": {"type": "string"},
        "members": {
            "type": "array",
            "items": {"$ref": "#/definitions/receiver"}
        }
    },
    "required": ["room_id", "msg", "sender", "members"],
    "additionalProperties": False,
    "definitions": {
        "receiver": {
            "type": "object",
            "properties": {
                "username": {"type": "string"}
            }
        }
    }
}

flag_read_schema = {
    "type": "object",
    "properties": {
        "room_id": {"type": "string"},
        "reader": {"type": "string"}
    },
    "required": ["room_id", "reader"],
    "additionalProperties": False
}


def validate_new_room(data):
    return validate_schema(data, chat_room_schema)

def validate_new_msg(data):
    return validate_schema(data, new_msg_schema)

def validate_flag_read_msg(data):
    return validate_schema(data, flag_read_schema)