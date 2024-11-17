from flask import render_template, request, redirect, url_for, session, flash
from functools import wraps
from database import get_db_connection
from werkzeug.security import check_password_hash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def register_skins_routes(app):
    @app.route('/valskins')
    @login_required
    def display_valskins():
        user_id = session['user_id']
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Fetch all skins from the Valorant skin database
                cursor.execute("SELECT * FROM valskins")
                valskins = cursor.fetchall()

                # Fetch the user's balance to display
                cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
                balance = cursor.fetchone()

        finally:
            connection.close()

        # Render the template with Valorant skins and user balance
        return render_template('valskins.html', valskins=valskins, balance=balance['balance'])