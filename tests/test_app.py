# Import des librairies de test
import unittest
from unittest.mock import patch
from flask import Flask, request, jsonify, render_template, redirect, url_for

# Import de l'application Flask à tester
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        # Initialisation de l'application Flask pour les tests
        app.testing = True
        self.app = app.test_client()

    def test_get_all_reminders(self):
        # Test de la route pour récupérer tous les rappels
        response = self.app.get('/api/test')
        self.assertEqual(response.status_code, 200)

    def test_create_reminder(self):
        # Test de la route pour créer un rappel
        response = self.app.post('/api/create', json={'title': 'Test Reminder', 'description': 'Test Description', 'trigger_time': '2024-04-17 12:00:00'})
        self.assertEqual(response.status_code, 201)

    def test_update_reminder(self):
        # Test de la route pour mettre à jour un rappel
        # Notez que vous devez d'abord créer un rappel pour le mettre à jour
        # response_create = self.app.post('/api/test', json={'title': 'Test Reminder', 'description': 'Test Description', 'trigger_time': '2024-04-17 12:00:00'})
        # self.assertEqual(response_create.status_code, 201)
        # reminder_id = response_create.json['id']

        # Mettre à jour le rappel nouvellement créé
        # response_update = self.app.put(f'/api/test/{reminder_id}', json={'description': 'Updated Description', 'trigger_time': '2024-04-17 13:00:00'})
        response_update = self.app.put(f'/api/test/3', json={'description': 'Updated Description', 'trigger_time': '2024-04-17 13:00:00'})
        self.assertEqual(response_update.status_code, 200)

    def test_delete_reminder(self):
        # Test de la route pour supprimer un rappel
        # Notez que vous devez d'abord créer un rappel pour le supprimer
        # response_create = self.app.post('/api/test', json={'title': 'Test Reminder', 'description': 'Test Description', 'trigger_time': '2024-04-17 12:00:00'})
        # self.assertEqual(response_create.status_code, 201)
        # reminder_id = response_create.json['id']

        # Supprimer le rappel nouvellement créé
        response_delete = self.app.delete(f'/api/test/5')
        self.assertEqual(response_delete.status_code, 200)

if __name__ == '__main__':
    unittest.main()