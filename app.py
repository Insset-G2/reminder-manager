from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import uuid
import mysql.connector
import os
import uuid
from dotenv import load_dotenv
import mariadb
import json

app = Flask(__name__)
load_dotenv()

def get_db_connection():
    try:
        conn = mariadb.connect(
            host='172.21.0.2',
            port=3306,
            user='reminder',
            password='reminder',
            database='reminder-manager'
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

# Route pour récupérer tous les rappels
@app.route('/api/test', methods=['GET'])
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
                    'title': reminder[1],
                    'description': reminder[2],
                    'trigger_time': reminder[3].strftime("%Y-%m-%d %H:%M:%S")
                }
                reminders_list.append(reminder_dict)
            return jsonify(reminders_list), 200
        except mariadb.Error as e:
            print(f"Error retrieving reminders: {e}")
            return jsonify({"error": "Failed to retrieve reminders"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500


@app.route('/')
def home():
    return render_template('create-reminder.html')

# Route pour créer un rappel
@app.route('/api/test', methods=['POST'])
def create_reminder():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    trigger_time = data.get('trigger_time')

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO reminders (title, description, trigger_time) VALUES (?, ?, ?)", (title, description, trigger_time))
            conn.commit()
            conn.close()
            return jsonify({"message": "Reminder created successfully"}), 201
        except mariadb.Error as e:
            print(f"Error creating reminder: {e}")
            return jsonify({"error": "Failed to create reminder"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500
    
# Route pour mettre à jour un rappel
@app.route('/api/test/<string:id>', methods=['PUT'])
def update_reminder(id):
    data = request.json
    description = data.get('description')
    trigger_time = data.get('trigger_time')

    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE reminders SET description=?, trigger_time=? WHERE id=?", (description, trigger_time, id))
            conn.commit()
            conn.close()
            return jsonify({"message": "Reminder updated successfully"}), 200
        except mariadb.Error as e:
            print(f"Error updating reminder: {e}")
            return jsonify({"error": "Failed to update reminder"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

# Route pour supprimer un rappel
@app.route('/api/test/<string:id>', methods=['DELETE'])
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
    

@app.route('/api/test/<string:id>', methods=['GET'])
def show(id):
    # Récupérer les données du rappel correspondant dans la base de données
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM reminders WHERE id=?", (id,))
            reminder = cur.fetchone()
            conn.close()

            # Vérifier si le rappel existe
            if reminder:
                reminder_dict = {
                    'id': reminder[0],
                    'title': reminder[1],
                    'description': reminder[2],
                    'trigger_time': reminder[3].strftime("%Y-%m-%d %H:%M:%S")
                }
                return jsonify(reminder_dict), 200
            else:
                return jsonify({"error": "Reminder not found"}), 404
        except mariadb.Error as e:
            print(f"Error retrieving reminder: {e}")
            return jsonify({"error": "Failed to retrieve reminder"}), 500
    else:
        return jsonify({"error": "Failed to connect to database"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
