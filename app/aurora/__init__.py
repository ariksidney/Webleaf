from flask import Blueprint

aurora = Blueprint('aurora', __name__)

from . import views