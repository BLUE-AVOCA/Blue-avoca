from flask import Blueprint
import os

bp = Blueprint('main', __name__)

from app.main import routes
