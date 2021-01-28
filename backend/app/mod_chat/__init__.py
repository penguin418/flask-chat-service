from flask import Blueprint

mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

from .controller import ChatsListAPI, ChatsAPI
chats_list_api = ChatsListAPI
chats_api = ChatsAPI
