from flask import Blueprint
from .controller import ChatsListAPI, ChatsAPI

mod_chat = Blueprint('chat', __name__, url_prefix='/chat')
chats_list_api = ChatsListAPI
chats_api = ChatsAPI
