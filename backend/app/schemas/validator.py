from jsonschema import validate, ValidationError, SchemaError


def validate_schema(data, schema):
    try:
        validate(data, schema)
    except ValidationError as e:
        return False, e
    except SchemaError as e:
        return False, e
    return True, data