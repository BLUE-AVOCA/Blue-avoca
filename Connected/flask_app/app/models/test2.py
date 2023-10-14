from app import db

from flask_login import UserMixin


class Customers(UserMixin,db.Model):
    __tablename__ = 'customers'
    __table_args__ = {'extend_existing': True}
    customer_id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    # customer_id = db.Column(db.Integer, db.ForeignKey('products.customer_id'))

class Product(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(255))
    description = product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer())
    price = db.Column(db.Float())
    #Relationship with users
    customer_id = db.Column(db.Float())
    country = db.Column(db.String(255), nullable=False)
    #Relationship with companies
    company_id = db.Column(db.Integer())
    category = db.Column(db.String(255), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    product_img = db.Column(db.String(255), nullable=False)
   
class Company(db.Model):
    __tablename__ = 'companies'
    __table_args__ = {'extend_existing': True}
    company_id = db.Column(db.Integer(), primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    logo =  db.Column(db.String(255), nullable=False)
    background_img = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(255), nullable=False)