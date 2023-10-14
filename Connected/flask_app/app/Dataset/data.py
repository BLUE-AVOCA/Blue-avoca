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

        # csv_data = read_csv('/Users/tranvo1233/VSCode/MyShecodes/Connected/flask_app/app/Dataset/products.csv')

        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        path_data = os.path.join(SITE_ROOT, "products.csv")
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

       
        company_1 = Company(
            company_name="Your life",
            logo="https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            background_img="https://hoadecor.vn/wp-content/uploads/2021/08/cua-hang-hoa-17.jpg",
            telephone="0869848290"
        )
        db.session.add_all([company_1])
        db.session.commit()
         # Retrieve the added data
        added_products = Product.query.all()
        companies = Company.query.all()
        
        # Print the added products (for demonstration purposes)
        for product in added_products:
            print(f"Added product: {product.product_name} (ID: {product.product_id})")
        for company in companies:
            print("Company: {}".format(company.company_name) )