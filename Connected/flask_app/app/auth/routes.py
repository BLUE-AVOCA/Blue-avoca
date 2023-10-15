from flask import render_template, redirect, url_for ,request,flash
from app.models.test2 import Customers
from app.auth import bp
from flask_login import login_user, login_required, current_user
from app.models.test2 import db


@bp.route('/login/')
def login():
    return render_template('form/login.html')

@bp.route('/register/')
def register():
    return render_template('form/register.html')

@bp.route('/profile/')
# @login_required
def profile():
    return render_template('form/profile.html')

@bp.route('/register/', methods=['POST'])
def register_post():
    email = request.form['email']
    password = request.form['password']
    print(email)
    print(password)
    user = Customers.query.filter_by(email=email).first() 
    if user: 
        print('already exists')
        flash('Email address already exists')
        return redirect(url_for('auth.register'))
    
    new_user = Customers(email=email, password=password)
    db.session.add(new_user)
    print(new_user)
    db.session.commit()
    return redirect(url_for('auth.login_post'))

@bp.route('/login/', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    # remember = True if request.form.get('remember') else False
    user = Customers.query.filter_by(email=email).first() 
    print(user)
    checkpass = (user.password == password)
    if not user or not checkpass:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) 
    # login_user(Customers, remember=remember)
    customers  = Customers.query.get(user.customer_id)
    print(customers)
    return redirect(url_for('auth.profile'))
    


