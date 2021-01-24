from . import schema_user
from . import schema_friend

validate_register = schema_user.validate_user

validate_login = schema_user.validate_login

validate_new_friend = schema_friend.validate_new_friend