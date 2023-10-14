from flask import Blueprint
import os

bp = Blueprint('company', __name__)

from app.company import routes
