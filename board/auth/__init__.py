from flask import Blueprint
auth_view = Blueprint('auth_view', __name__)
from board.auth import views, forms
