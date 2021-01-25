from flask import Blueprint
from .controller import FriendsListApi, FriendsAPI
# mod_friend = Blueprint('friend', __name__, url_prefix='/friends')
friends_list_api = FriendsListApi
friends_api = FriendsAPI

# from . import controller