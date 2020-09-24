from flask import Blueprint

mod_chat = Blueprint('chat', __name__, url_prefix='/chat')

from . import controller