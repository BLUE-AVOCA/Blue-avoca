from flask import render_template
from app.connected import bp
from app.models.test2 import Company

@bp.route('/')
def index():
    companies = Company.query.all()
    return render_template('connected/base.html', companies = companies)
