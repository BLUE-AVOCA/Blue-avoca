from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # app.config.from_object(config_class)
    
    
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.user'
    # app.config['SQLALCHEMY_DATABASE_URI'] = postgresURI
    
    db.init_app(app)


    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # from app.Dataset.data import create_data
    # create_data(app)

    from app.dash_app import create_dash_application
    create_dash_application(app)

    from .models.test2 import Customers

    @login_manager.user_loader
    def load_user(customer_id):
        return Customers.query.get(int(customer_id))

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')
    
    from app.auth import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/auth')

    from app.company import bp as company_bp
    app.register_blueprint(company_bp, url_prefix='/company')

    from app.connected import bp as connect_bp
    app.register_blueprint(connect_bp, url_prefix='/connect')

    from app.pay import bp as pay_bp
    app.register_blueprint(pay_bp, url_prefix='/pay')

    return app

