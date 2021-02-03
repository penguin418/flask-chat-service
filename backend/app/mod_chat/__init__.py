from flask import Blueprint

mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

from .controller import RoomsListAPI, RoomsAPI
chats_list_api = RoomsListAPI
chats_api = RoomsAPI
