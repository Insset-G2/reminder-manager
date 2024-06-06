from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime, timedelta
import uuid
import mysql.connector
import os
from dotenv import load_dotenv
import mariadb


app = Flask(__name__)
load_dotenv()

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)

def get_db_connection():
    try:
        conn = mariadb.connect(
            host=os.getenv('MARIADB_HOST'),
            port=int(os.getenv('MARIADB_PORT')),
            user=os.getenv('MARIADB_USER'),
            password=os.getenv('MARIADB_PASSWORD'),
            database=os.getenv('MARIADB_DB')

            # host='172.21.0.3',
            # port=3306,
            # user='reminder',
            # password='reminder',
            # database='reminder-manager'
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None
    
###########################################################################

@app.route('/api/users', methods=['GET'])
def get_all_users():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            conn.close()
            # Convertir les résultats en un format JSON
            users_list = []
            for user in users:
                user_dict = {
                    'id': user[0],
                    'username': user[1],
                }
                users_list.append(user_dict)
            print(jsonify(users_list))
            return jsonify(users_list), 200
        except mariadb.Error as e:
            print(f"Error retrieving users: {e}")
            return jsonify({"error": "Failed to retrieve users"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500
    
@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.form
    username = data.get('username')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username) VALUES (?)",
            (username,)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'id': user_id}), 201
    else:
        return jsonify({'error': 'Failed to connect to the database'}), 500
    
    

#################################################################################

@app.route('/reminders/current', methods=['GET'])
def get_current_reminders():
    print("Executing function...")
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            # Sélectionnez les rappels dont l'heure de déclenchement est égale à l'heure actuelle
            
            # current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_time = datetime.now() + timedelta(hours=2)
            
            lower_bound = (current_time - timedelta(seconds=0)).strftime('%Y-%m-%d %H:%M:%S')
            upper_bound = (current_time + timedelta(seconds=60)).strftime('%Y-%m-%d %H:%M:%S')
            
            cur.execute("SELECT * FROM reminders WHERE trigger_time BETWEEN ? AND ?", (lower_bound, upper_bound))
            due_reminders = cur.fetchall()

            reminders_list = []
            for reminder in due_reminders:
                reminders_dict = {
                    'id': reminder[0],
                    'user_id': reminder[1],
                    'title': reminder[2],
                    'description': reminder[3],
                    'trigger_time': reminder[4].strftime("%Y-%m-%d %H:%M:%S"),
                }
                reminders_list.append(reminders_dict)
                
            return jsonify(reminders_list)
        except mariadb.Error as e:
            print(f"Error retrieving due reminders: {e}")
        finally:
            conn.close()


# Route pour récupérer tous les rappels
@app.route('/reminders/list', methods=['GET'])
def get_all_reminders():
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM reminders")
            reminders = cur.fetchall()

            conn.close()
            # Convertir les résultats en un format JSON
            reminders_list = []
            for reminder in reminders:
                reminder_dict = {
                    'id': reminder[0],
                    'user_id': reminder[1],
                    'title': reminder[2],
                    'description': reminder[3],
                    'trigger_time': reminder[4].strftime("%Y-%m-%d %H:%M:%S"),
                }
                reminders_list.append(reminder_dict)
            print(jsonify(reminders_list))
            return jsonify(reminders_list), 200
        except mariadb.Error as e:
            print(f"Error retrieving reminders: {e}")
            return jsonify({"error": "Failed to retrieve reminders"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500


@app.route('/')
def home():
    current_date_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
    return render_template('create-reminder.html', current_date_time=current_date_time)

@app.route('/update/<string:id>')
def updateReminder(id):
    reminder_data = get(id)

    current_date_time = datetime.now().strftime('%Y-%m-%dT%H:%M')
    
    if reminder_data:
        # Créer un dictionnaire contenant les données du rappel
        reminder = {
            'id': id,
            'title': reminder_data['title'],
            'description': reminder_data['description'],
            'trigger_time': reminder_data['trigger_time']
        }
        
        # Formater la date avant de passer à la vue
        reminder['trigger_time'] = datetime.strptime(reminder['trigger_time'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%dT%H:%M')
        
        return render_template('update-reminder.html', reminder=reminder, current_date_time=current_date_time)
    else:
        return jsonify({"error": "Reminder not found"}), 404

@app.route('/get/<string:id>')
def getReminder(id):
    reminder = get(id)
    if reminder:
        return render_template('reminder.html', reminder=reminder)
    else:
        return jsonify({"error": "Reminder not found"}), 404


# Route pour créer un rappel
@app.route('/reminder/create', methods=['POST'])
def create_reminder():
    data = request.form
    user_id = data.get('user_id')
    title = data.get('title')
    description = data.get('description')
    trigger_time = data.get('trigger_time')

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO reminders (user_id, title, description, trigger_time) VALUES (?, ?, ?, ?)", (user_id, title, description, trigger_time))
            conn.commit()
            conn.close()
            return jsonify({"message": "Reminder created successfully"}), 201
        except mariadb.Error as e:
            print(f"Error creating reminder: {e}")
            return jsonify({"error": "Failed to create reminder"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500
    
# Route pour mettre à jour un rappel
@app.route('/reminder/update/<string:id>', methods=['POST'])
def update_reminder(id):
    data = request.form
    description = data.get('description')
    trigger_time = data.get('trigger_time')
    title = data.get('title')

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE reminders SET description=?, trigger_time=?, title=? WHERE id=?", (description, trigger_time, title, id))
            conn.commit()
            conn.close()
            return jsonify({"message": "Reminder updated successfully"}), 200
        except mariadb.Error as e:
            print(f"Error updating reminder: {e}")
            return jsonify({"error": "Failed to update reminder"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route pour supprimer un rappel
@app.route('/reminder/delete/<string:id>', methods=['POST'])
def delete_reminder(id):
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM reminders WHERE id=?", (id,))
            conn.commit()
            conn.close()
            return jsonify({"message": "Reminder deleted successfully"}), 200
        except mariadb.Error as e:
            print(f"Error deleting reminder: {e}")
            return jsonify({"error": "Failed to delete reminder"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500
    

@app.route('/reminder/get/<string:id>', methods=['GET'])
def get(id):
    # Récupérer les données du rappel correspondant dans la base de données
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, title, description, trigger_time FROM reminders WHERE id=?", (id,))
            reminder = cur.fetchone()
            conn.close()
            if reminder:
                return {
                    'id': reminder[0],
                    'title': reminder[1],
                    'description': reminder[2],
                    'trigger_time': reminder[3].strftime("%Y-%m-%dT%H:%M:%S")
                }
        except mariadb.Error as e:
            print(f"Erreur lors de la récupération du rappel : {e}")
            return None
    return None

if __name__ == '__main__':
    print("Starting the application...")

    app.run(host='0.0.0.0', port=5000, debug=True)

