import os
import pandas as pd


def create_companies(app):
    with app.app_context():
        from app import db
        from app.models.test2 import Company
        db.drop_all()
        db.create_all()      

        import csv

        def read_csv(filename):
            data = []
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            return data

        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        path_data = os.path.join(SITE_ROOT, "companies.csv")
        csv_data = read_csv(path_data)

        for company in csv_data:
            product = Company(
                company_id = company["Company ID"],
                company_name = company["Company Name"],
                logo = company["Logo"],
                background_img = company["Background_img"],
                telephone = company["Telephone"],
                )
            db.session.add(product)
            db.session.commit()
        companies = Company.query.all()
        for company in companies:
            print("Company: {}".format(company.company_name) )
