from flask import Flask, request, jsonify, render_template, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)

reminders = []

class Reminder:
    def __init__(self, title, description, trigger_time):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.trigger_time = trigger_time


@app.route('/')
def home():
    return render_template('create-reminder.html')

@app.route('/create-reminder')
def create_reminder_page():
    return render_template('create-reminder.html')




@app.route('/show', methods=['GET'])
def show():
    return jsonify([reminder.__dict__ for reminder in reminders])

@app.route('/create', methods=['POST'])
def create():
    description = request.form['description']
    print(request.form)
    # data = request.json
    # title = 'Rappel n°' + str(len(reminders) + 1)
    # description = data.get('description', 'TEST')
    # trigger_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # reminder = Reminder(title, description, trigger_time)
    # reminders.append(reminder)
    # return jsonify(reminder.__dict__)
    return redirect('/create-reminder')

@app.route('/edit/<string:id>', methods=['PUT'])
def edit(id):
    data = request.json
    for reminder in reminders:
        if reminder.id == id:
            reminder.description = data.get('description', 'TEST EDITED')
            reminder.trigger_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return jsonify(reminder.__dict__)
    return jsonify({"error": "Reminder not found"}), 404

@app.route('/delete/<string:id>', methods=['DELETE'])
def delete(id):
    global reminders
    reminders = [reminder for reminder in reminders if reminder.id != id]
    return jsonify({"message": "Your reminder has been deleted successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
