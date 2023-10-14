from flask import render_template
from app.company import bp
from app.models.test2 import Company, Product

@bp.route('/')
def index():
    companys = Company.query.all()
    return render_template('company/home.html', title = "Company", companys = companys)

@bp.route('/detail/<int:id>')
def detail(id):
    company = Company.query.filter(Company.company_id == id).first()
    products = Product.query.filter(Product.company_id == id)
    return render_template('company/detail.html',company = company, products = products)
