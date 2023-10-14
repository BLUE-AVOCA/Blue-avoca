from flask import render_template
from app.company import bp
from app.models.test2 import Company

@bp.route('/')
def index():
    companys = Company.query.all()
    print(companys)
    return render_template('company/home.html', title = "Company", companys = companys)

@bp.route('/detail/<int:id>')
def detail(id):
    company = Company.query.get(id)
    print(company)
    return render_template('company/detail.html',company = company)

