from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_show_boggle_board(self):
        """make sure info in HTML is displayed, and info is in session"""

        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'Score:', res.data)
            self.assertIn(b'Time Left:', res.data)


    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        res = self.client.get('/word-check?word=cat')
        self.assertEqual(res.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        res = self.client.get('/word-check?word=impossible')
        self.assertEqual(res.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is a real word"""

        self.client.get('/')
        res = self.client.get(
            '/word-check?word=mftfffjdtmcgtj')
        self.assertEqual(res.json['result'], 'not-word')



