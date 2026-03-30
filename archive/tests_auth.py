import unittest
import sys
from unittest.mock import MagicMock

# Mock dependencies to avoid installing heavy sci-libs for auth testing
sys.modules['chatbot'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['sklearn'] = MagicMock()
sys.modules['sklearn.feature_extraction.text'] = MagicMock()
sys.modules['sklearn.metrics.pairwise'] = MagicMock()

# Mock the chatbot class specifically
mock_bot = MagicMock()
sys.modules['chatbot'].SimpleChatbot.return_value = mock_bot

from app import app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.secret_key = 'test_secret'
        self.app = app.test_client()
        
    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Identifiant Acad', response.data)

    def test_valid_login(self):
        # Ensure user exists (relying on seed)
        email = "o.elmessaoudi@uca.ac.ma"
        code = "ENSA-8F3K"
        
        response = self.app.post('/login', data=dict(
            email=email,
            password=code
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Check if navbar shows something indicating login or the redirect happened
        # index page usually has "Accueil"
        self.assertIn(b'Accueil', response.data)
        # verify session persistence indirectly via layout 
        # The user has full name in DB
        self.assertIn(b'Othmane', response.data) 

    def test_invalid_email(self):
        response = self.app.post('/login', data=dict(
            email="fake@gmail.com",
            password="123"
        ), follow_redirects=True)
        self.assertIn(b'Email acad', response.data)

    def test_invalid_code(self):
        # This will fail if the DB seed didn't run or passwords aren't hashed/checked correctly
        response = self.app.post('/login', data=dict(
            email="o.elmessaoudi@uca.ac.ma",
            password="WRONG_CODE"
        ), follow_redirects=True)
        self.assertIn(b'Email ou code incorrect', response.data)

if __name__ == '__main__':
    unittest.main()
