from jsonschema import validate, ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "fullname": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "role": {
            "type": "string",
            "enum": ["NEW", "STANDARD", "ADMIN", "BANNED"]
        }
    },
    "required": ["email", "password"]
}

# def validate_user(data):
#     try:
#         validate(data, user_schema)
#     except ValidationError as e:
#         return False, e
#     return True, None
