from flask import render_template,request
from app.company import bp
from app.models.test2 import Company, Product

@bp.route('/')
def index():
    companies = Company.query.all()
    return render_template('company/base.html', title = "Company", companies = companies)

@bp.route('/detail/<int:id>')
def detail(id):
    company = Company.query.filter(Company.company_id == id).first()
    products = Product.query.filter(Product.company_id == id)
    return render_template('company/detail.html',company = company, products = products)

@bp.route('/search', methods=('GET', 'POST'))
def search():
    search_value = "Please search the items"
    products = []
    if request.method == 'POST':
        search_value = request.form['search_product']
        companies = Company.query.filter(Company.company_name.contains(search_value)).all()
        return render_template('company/base.html',companies = companies )
    return search_value

@bp.route('/filter', methods=('GET', 'POST'))
def filter():
    category = "NO"
    if request.method == 'POST':
        category = request.form.get('category')
        companies = Company.query.filter(Company.category == category).all()
        return render_template('company/base.html',companies = companies )
    return category