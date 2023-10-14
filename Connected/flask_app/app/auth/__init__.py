from flask import Blueprint
import os

bp = Blueprint('auth', __name__)

from app.auth import routes
