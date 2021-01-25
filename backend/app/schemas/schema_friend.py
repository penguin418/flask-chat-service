from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError



friend_schema = {
    "type": "object",
    "properties": {
        "requester": {
            "type": "object",
            "propoerties": {
                "username": {"type": "string"},
                "nickname": {"type:" "string"}
            }},
        "subject": {
            "type": "object",
            "propoerties": {
                "username": {"type": "string"},
                "nickname": {"type:" "string"}
            }},
        "status": {
            "type": "number",
            "enums": [
                0,  # reference
                1   # are friend
            ]
        }
    },
    "required": ["requester", "subject"],
    "additionalProperties": False
}

new_friend_schema = {
    "type": "object",
    "properties": {
        "requester": {
            "type": "object",
            "propoerties": {
                "username": {"type": "string"},
                "nickname": {"type:" "string"}
            }},
        "subject": {
            "type": "object",
            "propoerties": {
                "username": {"type": "string"},
                "nickname": {"type:" "string"}
            }}
    },
    "required": ["requester", "subject"],
    "additionalProperties": False
}


def validate_new_friend(data):
    try:
        validate(data, new_friend_schema)
    except ValidationError as e:
        return False, e
    except SchemaError as e:
        return False, e
    return True, data
