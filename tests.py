import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        result = self.client.get('/')
        self.assertIn('<h2>Please RSVP</h2>', result.data)
        self.assertNotIn('<h2>Party Details</h2>', result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)

        self.assertIn('<h2>Party Details</h2>', result.data)
        self.assertNotIn('<h2>Please RSVP</h2>', result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        """Runs the test games"""

        result = self.client.get('/games')
        # # this will show the status of the client browser
        # # eg) 200 OK 
        # print result.status
        self.assertIn('madlibs', result.data)
        self.assertIn('fun word game 1', result.data)

        # with self.client as c:
        #     with c.session_transaction() as sess:
        #         # sess is a flask session


if __name__ == "__main__":
    unittest.main()
