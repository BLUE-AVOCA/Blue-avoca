from flask import render_template
from app.main import bp

@bp.route('/')
def index():
    return render_template('home/home.html', title = "Home")

@bp.route('/about/')
def about():
    return render_template('home/about.html',title = "About")

