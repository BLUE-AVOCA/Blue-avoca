from flask import Blueprint

bp = Blueprint('pay', __name__)

from app.pay import routes
