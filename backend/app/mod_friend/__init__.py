from flask import Blueprint
from .controller import FriendsAPI
# mod_friend = Blueprint('friend', __name__, url_prefix='/friends')
api_friends = FriendsAPI

# from . import controller