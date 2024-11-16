from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
db = SQLAlchemy(app)

from models.user import User
@app.route('/')
@app.route('/home')
def home():
    return render_template('base.html', title="Home")


@app.route('/profile', methods=['GET'])
def profile():
    return render_template('base.html', title="profile")


@app.route('/logout', methods=['GET'])
def logout():
    return render_template('base.html', title="Logout")


@app.route('/register', methods=['GET'])
def register():
    return render_template('base.html', title="Register")

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/trade', methods=['GET'])
def trade():
    return render_template('base.html', title="Trade")


@app.route('/sell', methods=['GET'])
def sell():
    return render_template('base.html', title="Sell")


@app.route('/buy', methods=['GET'])
def buy():
    return render_template('base.html', title="Buy")


@app.route('/faq', methods=['GET'])
def faq():
    return render_template('base.html', title="FAQ")


@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template('base.html', title="About Us")



@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    return render_template('base.html', title="Contact Us")


@app.route('/user_profile', methods=['GET'])
def user_profile():
    return render_template('base.html', title="User Profile")


@app.route('/marketplace', methods=['GET'])
def marketplace():
    return render_template('base.html', title="Marketplace")


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

