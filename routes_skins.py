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

    @app.route('/cs2skins')
    @login_required
    def display_cs2skins():
        user_id = session['user_id']
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Fetch all skins from the CS2 skin database
                cursor.execute("SELECT * FROM cs2skins")
                cs2skins = cursor.fetchall()

                # Fetch the user's balance to display
                cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
                balance = cursor.fetchone()

        finally:
            connection.close()

        # Render the template with CS2 skins and user balance
        return render_template('cs2skins.html', cs2skins=cs2skins, balance=balance['balance'])


    @app.route('/buy_skin', methods=['POST'])
    @login_required
    def buy_skin():
        skin_id = request.form['skin_id']
        game = request.form['game']
        user_id = session['user_id']

        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Check if the user already owns the skin
                cursor.execute("SELECT * FROM user_inventory WHERE user_id = %s AND skin_id = %s AND game = %s",
                               (user_id, skin_id, game))
                existing_skin = cursor.fetchone()

                if existing_skin:
                    flash("You already own this skin.", "error")
                    return redirect(url_for('marketplace'))

                # Get the skin price based on the game (Valorant or CS2)
                if game == 'Valorant':
                    cursor.execute("SELECT cost FROM valskins WHERE id = %s", (skin_id,))
                else:
                    cursor.execute("SELECT cost FROM cs2skins WHERE id = %s", (skin_id,))

                skin = cursor.fetchone()

                if skin:
                    skin_cost = skin['cost']

                    # Get the user's current balance
                    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
                    user = cursor.fetchone()

                    if float(user['balance']) >= float(skin['cost']):
                        # Update user's balance
                        new_balance = float(user['balance']) - float(skin['cost'])
                        cursor.execute("UPDATE users SET balance = %s WHERE user_id = %s", (new_balance, user_id))

                        # Add the skin to the user's inventory
                        cursor.execute("INSERT INTO user_inventory (user_id, skin_id, game) VALUES (%s, %s, %s)",
                                       (user_id, skin_id, game))

                        connection.commit()
                        flash("Skin purchased successfully!", "success")
                    else:
                        flash("Insufficient balance.", "error")
                else:
                    flash("Skin not found.", "error")

        finally:
            connection.close()

        return redirect(url_for('marketplace'))


    @app.route('/view_skins/<game>', methods=['GET'])
    @login_required
    def view_skins(game):
        user_id = session['user_id']
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Get the user's balance
                cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()

                if game == 'Valorant':
                    cursor.execute("SELECT * FROM valskins")
                    skins = cursor.fetchall()
                elif game == 'CS2':
                    cursor.execute("SELECT * FROM cs2skins")
                    skins = cursor.fetchall()

        finally:
            connection.close()

        return render_template(f'{game.lower()}_skins.html', skins=skins, balance=user['balance'])


    @app.route('/trade', methods=['GET', 'POST'])
    @login_required
    def trade():
        user_id = session['user_id']
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Fetch the user's skins from their inventory for offering
                cursor.execute("""
                    SELECT ui.inventory_id, ui.skin_id, ui.game, v.Name AS val_skin_name, cs.Name AS cs2_skin_name
                    FROM user_inventory ui
                    LEFT JOIN valskins v ON ui.skin_id = v.id AND ui.game = 'Valorant'
                    LEFT JOIN cs2skins cs ON ui.skin_id = cs.id AND ui.game = 'CS2'
                    WHERE ui.user_id = %s
                """, (user_id,))
                user_inventory = cursor.fetchall()

                # Fetch all available skins that are owned by other users (exclude the current user)
                cursor.execute("""
                    SELECT ui.user_id AS user_id_from, ui.skin_id, v.Name AS val_skin_name, cs.Name AS cs2_skin_name, ui.game
                    FROM user_inventory ui
                    LEFT JOIN valskins v ON ui.skin_id = v.id AND ui.game = 'Valorant'
                    LEFT JOIN cs2skins cs ON ui.skin_id = cs.id AND ui.game = 'CS2'
                    WHERE ui.user_id != %s 
                """, (user_id))
                available_skins = cursor.fetchall()

            # Handle form submission for trade offer creation
            if request.method == 'POST':
                skin_id_offered = request.form['skin_id_offered']
                skin_id_requested = request.form['skin_id_requested']
               

                with connection.cursor() as cursor:
                    # Insert the trade offer into the database
                    cursor.execute("""
                        INSERT INTO trade_offers (user_id_from, skin_id_from, skin_id_to, status)
                        VALUES (%s, %s, %s, 'pending')
                    """, (user_id, skin_id_offered,  skin_id_requested))
                    connection.commit()

                flash('Trade offer created successfully!', 'success')
                return redirect(url_for('trade'))

        finally:
            connection.close()

        return render_template('trade.html', user_inventory=user_inventory, available_skins=available_skins)


    @app.route('/view_trade_offers', methods=['GET', 'POST'])
    @login_required
    def view_trade_offers():
        user_id = session['user_id']
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Fetch trade offers where the user is the one receiving the skin (user_id_to) or offering the skin (user_id_from)
                cursor.execute("""
                    SELECT trade_offers.offer_id, 
                        users.username AS offer_user,
                        valskins.Name AS offered_skin_name, 
                        valskins.picture AS offered_skin_picture, 
                        cs2skins.Name AS requested_skin_name, 
                        cs2skins.picture AS requested_skin_picture
                    FROM trade_offers
                    JOIN users ON trade_offers.user_id_from = users.user_id
                    LEFT JOIN valskins ON trade_offers.skin_id_from = valskins.id
                    LEFT JOIN cs2skins ON trade_offers.skin_id_to = cs2skins.id
                    WHERE (trade_offers.user_id_to IS NULL OR trade_offers.user_id_to = %s) 
                    AND trade_offers.status = 'pending'
                """, (user_id))

                trade_offers = cursor.fetchall()

            # Handle accepting the trade offer
            if request.method == 'POST':
                offer_id = request.form['offer_id']
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM trade_offers WHERE offer_id = %s", (offer_id,))
                    offer = cursor.fetchone()

                    if offer:
                        # Handle the trade acceptance here (swapping skins)
                        cursor.execute("UPDATE trade_offers SET status = 'accepted' WHERE offer_id = %s", (offer_id,))
                        cursor.execute("""
                            UPDATE user_inventory 
                            SET user_id = %s 
                            WHERE user_id = %s AND skin_id = %s
                        """, (user_id, offer['user_id_from'], offer['skin_id_from']))

                        cursor.execute("""
                            UPDATE user_inventory 
                            SET user_id = %s 
                            WHERE user_id = %s AND skin_id = %s
                        """, (offer['user_id_from'], user_id, offer['skin_id_to']))

                        connection.commit()
                        flash("Trade offer accepted and skins swapped!", "success")
                        return redirect(url_for('view_trade_offers'))

        finally:
            connection.close()

        return render_template('view_trade_offers.html', trade_offers=trade_offers)


    @app.route('/accept_trade/<int:trade_id>', methods=['POST'])
    @login_required
    def accept_trade(trade_id):
        user_id = session['user_id']
        connection = get_db_connection()

        try:
            with connection.cursor() as cursor:
                # Get the trade offer details
                cursor.execute("""
                    SELECT * FROM trade_offers WHERE offer_id = %s
                """, (trade_id,))
                offer = cursor.fetchone()

                if offer:
                    # Ensure the user is not accepting a trade for a skin they already have
                    cursor.execute("""
                        SELECT * FROM user_inventory WHERE user_id = %s AND skin_id = %s
                    """, (user_id, offer['skin_id_to']))
                    existing_skin = cursor.fetchone()

                    if existing_skin:
                        flash("You already own the requested skin!", "error")
                        return redirect(url_for('view_trade_offers'))

                    # Swap skins between the users
                    cursor.execute("""
                        UPDATE user_inventory SET user_id = %s WHERE user_id = %s AND skin_id = %s
                    """, (user_id, offer['user_id_from'], offer['skin_id_from']))

                    cursor.execute("""
                        UPDATE user_inventory SET user_id = %s WHERE user_id = %s AND skin_id = %s
                    """, (offer['user_id_from'], user_id, offer['skin_id_to']))

                    # Mark the trade offer as accepted
                    cursor.execute("""
                        UPDATE trade_offers SET status = 'accepted' WHERE offer_id = %s
                    """, (trade_id,))
                    connection.commit()

                    flash("Trade accepted! Skins swapped.", "success")
                    return redirect(url_for('view_trade_offers'))

        finally:
            connection.close()

        return redirect(url_for('view_trade_offers'))


    @app.route('/profile')
    @login_required
    def profile():
        if 'user_id' not in session:
            return redirect(url_for('login'))

        user_id = session['user_id']
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT valskins.id, valskins.picture, valskins.cost, valskins.release_date, valskins.description, valskins.Name
                    FROM valskins
                    JOIN user_inventory ON user_inventory.skin_id = valskins.id
                    WHERE user_inventory.user_id = %s AND user_inventory.game = 'Valorant'
                """, (user_id,))
                valorant_skins = cursor.fetchall()

                cursor.execute("""
                    SELECT cs2skins.id, cs2skins.picture, cs2skins.cost, cs2skins.release_date, cs2skins.description, cs2skins.Name
                    FROM cs2skins
                    JOIN user_inventory ON user_inventory.skin_id = cs2skins.id
                    WHERE user_inventory.user_id = %s AND user_inventory.game = 'CS2'
                """, (user_id,))
                cs2_skins = cursor.fetchall()

        return render_template('profile.html', username=session['username'], valorant_skins=valorant_skins,
                               cs2_skins=cs2_skins)

