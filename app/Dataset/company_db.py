
def create_company_data(app):
    with app.app_context():
        from app import db
        from app.models.test2 import Company
        db.drop_all()
        db.create_all()   
        company_1 = Company(
            company_name="Your life",
            logo="https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            background_img="https://hoadecor.vn/wp-content/uploads/2021/08/cua-hang-hoa-17.jpg",
            telephone="0869848290"
        )
        db.session.add_all([company_1])
        db.session.commit()

        companies = Company.query.all()
        for company in companies:
            print("Company: {}".format(company.company_name) )