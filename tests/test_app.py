# Import des librairies de test
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template, redirect, url_for

# Import de l'application Flask à tester
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Initialisation de l'application Flask pour les tests
        app.testing = True
        self.app = app.test_client()
        

    @patch('app.get_db_connection')
    def test_get_current_reminders(self, mock_get_db_connection):
        # Mocking the database connection and cursor
        mock_conn = mock_get_db_connection.return_value
        mock_cursor = mock_conn.cursor.return_value
        
        # Sample data to be returned by the mock cursor
        mock_cursor.fetchall.return_value = [
            (12, 4, "Test", "description du test", datetime(2024, 6, 6, 10, 21, 0))
        ]

        response = self.app.get('/reminders/current')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test', response.get_data(as_text=True))

    @patch('app.get_db_connection')
    def test_get_all_reminders(self, mock_get_db_connection):
        # Mocking the database connection and cursor
        mock_conn = mock_get_db_connection.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Sample data to be returned by the mock cursor
        mock_cursor.fetchall.return_value = [
            (12, 4, "Test", "description du test", datetime(2024, 6, 6, 10, 21, 0)),
            (13, 5, "Another Test", "another description", datetime(2024, 6, 7, 11, 22, 0))
        ]

        response = self.app.get('/reminders/list')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test', response.get_data(as_text=True))
        self.assertIn('Another Test', response.get_data(as_text=True))

    @patch('app.get_db_connection')
    def test_create_reminder(self, mock_get_db_connection):
        # Mocking the database connection and cursor
        mock_conn = mock_get_db_connection.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Sample data to be returned by the mock cursor
        mock_cursor.lastrowid = 1

        data = {
            'user_id': 4,
            'title': 'Test Reminder',
            'description': 'Test Description',
            'trigger_time': '2024-06-06 10:21:00'
        }
        response = self.app.post('/reminder/create', data=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Reminder created successfully', response.get_data(as_text=True))

    @patch('app.get_db_connection')
    def test_update_reminder(self, mock_get_db_connection):
        # Mocking the database connection and cursor
        mock_conn = mock_get_db_connection.return_value
        mock_cursor = mock_conn.cursor.return_value

        data = {
            'description': 'Updated Description',
            'trigger_time': '2024-06-07 11:22:00'
        }
        response = self.app.post('/reminder/update/12', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Reminder updated successfully', response.get_data(as_text=True))

    @patch('app.get_db_connection')
    def test_delete_reminder(self, mock_get_db_connection):
        # Mocking the database connection and cursor
        mock_conn = mock_get_db_connection.return_value
        mock_cursor = mock_conn.cursor.return_value

        response = self.app.post('/reminder/delete/12')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Reminder deleted successfully', response.get_data(as_text=True))

    @patch('app.get_db_connection')
    def test_show_reminder(self, mock_get_db_connection):
        # Mocking the database connection and cursor
        mock_conn = mock_get_db_connection.return_value
        mock_cursor = mock_conn.cursor.return_value

        # Sample data to be returned by the mock cursor
        mock_cursor.fetchone.return_value = (12, "Test", "description du test", datetime(2024, 6, 6, 10, 21, 0))

        response = self.app.get('/reminder/get/12')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()