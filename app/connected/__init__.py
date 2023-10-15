from flask import Blueprint
import os

bp = Blueprint('connected', __name__)

from app.connected import routes
