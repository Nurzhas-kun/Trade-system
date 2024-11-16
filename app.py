
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(name)
app.secret_key = 'your_secret_key'  # Replace with your secret key for session management

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',  # Replace with your database password
    'database': 'skinsdb'
}
from models.user import User


def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        cursorclass=pymysql.cursors.DictCursor
    )


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function





# Home route
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')






# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                               (username, email, password))
                connection.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
        except pymysql.MySQLError:
            flash('User already exists or database error', 'error')
        finally:
            connection.close()

    return render_template('register.html')





# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                if user and check_password_hash(user['password'], password):
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid credentials', 'error')
        finally:
            connection.close()

    return render_template('login.html')


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

