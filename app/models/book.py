from jsonschema import validate, ValidationError

book_schema = {
    "name": {
        "type": "string",
        "required": True
    },
    "author_name": {
        "type": "string",
        "required": True
    },
    "tag": {
        "type": "string",
        "enum": ["Python", "C++", "JavaScript", "Java"]
    },
    "file": {
        "filename": "string",
        "originalName": "string",
        "contentType": "string",
        "data": "byte"
    }
}

# def validate_book(data):
#     try:
#         validate(data, book_schema)
#     except ValidationError as e:
#         return False, e
#     return True, None
