from werkzeug.exceptions import HTTPException
from flask import make_response
import json
#  created new classes for specific error codes and messages 
class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('',status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {
            'Error Code' : error_code,
            'Message' : error_message
        }
        self.response = make_response(json.dumps(message),status_code)
