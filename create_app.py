from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from routes_skins import register_skins_routes  # Function to register skin-related routes
from database import get_db_connection  # Database connection utility

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Replace with your secret key

    # Register skin-related routes
    register_skins_routes(app)

    # Decorator to ensure login is required for certain routes
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    # Index route
    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return render_template('index.html')

    # Registration route
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

    # Logout route
    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    # Home route
    @app.route('/home')
    def home():
        return render_template('home.html')

    # Marketplace route
    @app.route('/marketplace')
    @login_required
    def marketplace():
        user_id = session['user_id']
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Fetch all Valorant skins
                cursor.execute("SELECT * FROM valskins")
                valskins = cursor.fetchall()

                # Fetch all CS2 skins
                cursor.execute("SELECT * FROM cs2skins")
                cs2skins = cursor.fetchall()

                # Fetch the user's balance
                cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()

        finally:
            connection.close()

        return render_template(
            'marketplace.html',
            valskins=valskins,
            cs2skins=cs2skins,
            balance=user['balance']
        )

    # FAQ route
    @app.route('/faq')
    def faq():
        return render_template('faq.html')

    # About Us route
    @app.route('/about_us')
    def about_us():
        return render_template('about_us.html')

    # Contact Us route
    @app.route('/contact_us')
    def contact_us():
        return render_template('contact_us.html')

    return app
