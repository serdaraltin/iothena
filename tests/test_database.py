import unittest
import os

import database
from database import database_connector

class TestDatabase(unittest.TestCase):
    db_connector = None
    def setUp(self):
        self.db_connector = database_connector.Connector()
        self.db_session = self.db_connector.get_session()

    def tearDown(self):
        self.db_connector = None

    def test_config_exists(self):
        self.assertTrue(os.path.exists("config/config.json"))

    def test_connector(self):
        self.assertIsNotNone(self.db_connector)
        self.assertIsInstance(self.db_connector, database_connector.Connector)

    def test_database(self):
        self.assertIsInstance(self.db_connector.check_connection(), bool)
        self.assertTrue(self.db_connector.check_connection())

if __name__ == '__main__':
    unittest.main()

