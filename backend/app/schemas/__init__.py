from . import schema_user
from . import schema_friend
from . import schema_chat

validate_register = schema_user.validate_user

validate_login = schema_user.validate_login

validate_new_friend = schema_friend.validate_new_friend

validate_flag_read_msg = schema_chat.validate_flag_read_msg