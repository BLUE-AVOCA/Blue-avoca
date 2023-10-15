import os
import pandas as pd


def create_data(app):
    with app.app_context():
        from app import db
        from app.models.test2 import Product
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
        path_data = os.path.join(SITE_ROOT, "products2.csv")
        csv_data = read_csv(path_data)

        for item in csv_data:
            product = Product(
                product_id=item['Product_id'], 
                description=item['Description'],
                quantity=item['Quantity'], 
                price=item['Price'], 
                customer_id=item['Customer ID'], 
                country=item['Country'], 
                company_id=item['Company_id'], 
                category=item['Category'], 
                product_name=item['Name'], 
                product_img = item['Product_img']
                )
            db.session.add(product)
            db.session.commit()

       
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        path_data = os.path.join(SITE_ROOT, "companies2.csv")
        csv_data = read_csv(path_data)

        for company in csv_data:
            product = Company(
                company_id = company["Company ID"],
                company_name = company["Company Name"],
                logo = company["Logo"],
                background_img = company["Background_img"],
                telephone = company["Telephone"],
                category = company["Category"]
                )
            db.session.add(product)
            db.session.commit()
            
         # Retrieve the added data
        added_products = Product.query.all()
        companies = Company.query.all()
        
        # Print the added products (for demonstration purposes)
        for product in added_products:
            print(f"Added product: {product.product_name} (ID: {product.product_id})")
        for company in companies:
            print("Company: {}".format(company.category) )
