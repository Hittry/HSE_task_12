from flask import Blueprint
actions_view = Blueprint('actions_view', __name__)
from board.actions import forms, views
