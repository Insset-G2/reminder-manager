# # Import des librairies de test
# import unittest
# from unittest.mock import patch
# from datetime import datetime, timedelta
# from flask import Flask, request, jsonify, render_template, redirect, url_for

# # Import de l'application Flask à tester
# from app import app

# class TestApp(unittest.TestCase):
#     def setUp(self):
#         # Initialisation de l'application Flask pour les tests
#         app.testing = True
#         self.app = app.test_client()
        

#     @patch('app.get_db_connection')
#     def test_get_current_reminders(self, mock_get_db_connection):
#         # Mocking the database connection and cursor
#         mock_conn = mock_get_db_connection.return_value
#         mock_cursor = mock_conn.cursor.return_value
        
#         # Sample data to be returned by the mock cursor
#         mock_cursor.fetchall.return_value = [
#             (12, 4, "Test", "description du test", datetime(2024, 6, 6, 10, 21, 0))
#         ]

#         response = self.app.get('/reminders/current')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Test', response.get_data(as_text=True))

#     @patch('app.get_db_connection')
#     def test_get_all_reminders(self, mock_get_db_connection):
#         # Mocking the database connection and cursor
#         mock_conn = mock_get_db_connection.return_value
#         mock_cursor = mock_conn.cursor.return_value

#         # Sample data to be returned by the mock cursor
#         mock_cursor.fetchall.return_value = [
#             (12, 4, "Test", "description du test", datetime(2024, 6, 6, 10, 21, 0)),
#             (13, 5, "Another Test", "another description", datetime(2024, 6, 7, 11, 22, 0))
#         ]

#         response = self.app.get('/reminders/list')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Test', response.get_data(as_text=True))
#         self.assertIn('Another Test', response.get_data(as_text=True))

#     @patch('app.get_db_connection')
#     def test_create_reminder(self, mock_get_db_connection):
#         # Mocking the database connection and cursor
#         mock_conn = mock_get_db_connection.return_value
#         mock_cursor = mock_conn.cursor.return_value

#         # Sample data to be returned by the mock cursor
#         mock_cursor.lastrowid = 1

#         data = {
#             'user_id': 4,
#             'title': 'Test Reminder',
#             'description': 'Test Description',
#             'trigger_time': '2024-06-06 10:21:00'
#         }
#         response = self.app.post('/reminder/create', data=data)
#         self.assertEqual(response.status_code, 201)
#         self.assertIn('Reminder created successfully', response.get_data(as_text=True))

#     @patch('app.get_db_connection')
#     def test_update_reminder(self, mock_get_db_connection):
#         # Mocking the database connection and cursor
#         mock_conn = mock_get_db_connection.return_value
#         mock_cursor = mock_conn.cursor.return_value

#         data = {
#             'description': 'Updated Description',
#             'trigger_time': '2024-06-07 11:22:00'
#         }
#         response = self.app.put('/reminder/update/12', json=data)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Reminder updated successfully', response.get_data(as_text=True))

#     @patch('app.get_db_connection')
#     def test_delete_reminder(self, mock_get_db_connection):
#         # Mocking the database connection and cursor
#         mock_conn = mock_get_db_connection.return_value
#         mock_cursor = mock_conn.cursor.return_value

#         response = self.app.delete('/reminder/delete/12')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Reminder deleted successfully', response.get_data(as_text=True))

#     @patch('app.get_db_connection')
#     def test_show_reminder(self, mock_get_db_connection):
#         # Mocking the database connection and cursor
#         mock_conn = mock_get_db_connection.return_value
#         mock_cursor = mock_conn.cursor.return_value

#         # Sample data to be returned by the mock cursor
#         mock_cursor.fetchone.return_value = (12, "Test", "description du test", datetime(2024, 6, 6, 10, 21, 0))

#         response = self.app.get('/reminder/get/12')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('Test', response.get_data(as_text=True))


# if __name__ == '__main__':
#     unittest.main()

import unittest
from datetime import datetime, timedelta
import uuid

# Importer l'application Flask
from app import app, reminders

class TestApp(unittest.TestCase):
    
    def setUp(self):
        # Initialiser l'application Flask pour les tests
        app.testing = True
        self.app = app.test_client()
        global reminders

    def tearDown(self):
        # Vider les rappels après chaque test
        reminders.clear()

    def test_create_reminder(self):
        data = {
            'id': str(uuid.uuid4()),
            'user_id': 'user1',
            'title': 'Test Reminder',
            'description': 'Test Description',
            'trigger_time': '2024-06-06 10:21:00'
        }
        response = self.app.post('/reminder/create', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Reminder created successfully', response.get_data(as_text=True))

    def test_get_current_reminders(self):
        # Ajouter un rappel dû dans les 60 prochaines secondes
        reminder_id = str(uuid.uuid4())
        current_time = datetime.now() + timedelta(hours=2)
        trigger_time = (current_time + timedelta(seconds=30)).strftime('%Y-%m-%d %H:%M:%S')
        reminders.append({
            'id': reminder_id,
            'user_id': 'user1',
            'title': 'Test Reminder',
            'description': 'Test Description',
            'trigger_time': trigger_time,
        })

        response = self.app.get('/reminders/current')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Reminder', response.get_data(as_text=True))

    def test_get_all_reminders(self):
        # Ajouter des rappels d'exemple
        reminders.extend([
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user1',
                'title': 'Test Reminder',
                'description': 'Test Description',
                'trigger_time': (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'),
            },
            {
                'id': str(uuid.uuid4()),
                'user_id': 'user2',
                'title': 'Another Test Reminder',
                'description': 'Another Test Description',
                'trigger_time': (datetime.now() + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),
            }
        ])

        response = self.app.get('/reminders/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Reminder', response.get_data(as_text=True))
        self.assertIn('Another Test Reminder', response.get_data(as_text=True))

    def test_update_reminder(self):
        reminder_id = str(uuid.uuid4())
        reminders.append({
            'id': reminder_id,
            'user_id': 'user1',
            'title': 'Test Reminder',
            'description': 'Test Description',
            'trigger_time': '2024-06-06 10:21:00',
        })

        data = {
            'description': 'Updated Description',
            'trigger_time': '2024-06-07 11:22:00',
            'title': 'Updated Title',
        }
        response = self.app.put(f'/reminder/update/{reminder_id}', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Reminder updated successfully', response.get_data(as_text=True))

    def test_delete_reminder(self):
        reminder_id = str(uuid.uuid4())
        reminders.append({
            'id': reminder_id,
            'user_id': 'user1',
            'title': 'Test Reminder',
            'description': 'Test Description',
            'trigger_time': '2024-06-06 10:21:00',
        })

        response = self.app.delete(f'/reminder/delete/{reminder_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Reminder deleted successfully', response.get_data(as_text=True))

    def test_get_reminder(self):
        reminder_id = str(uuid.uuid4())
        reminders.append({
            'id': reminder_id,
            'user_id': 'user1',
            'title': 'Test Reminder',
            'description': 'Test Description',
            'trigger_time': '2024-06-06 10:21:00',
        })

        response = self.app.get(f'/reminder/show/{reminder_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Reminder', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
