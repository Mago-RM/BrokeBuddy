import unittest
import json
import os
import tempfile
from unittest.mock import MagicMock, patch
from logic.storage import save_user_data


class TestStorage(unittest.TestCase):
    def setUp(self):
        # Create a test directory for test file
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_data.json")

        # Create a mock user object
        self.mock_user = MagicMock()
        self.mock_user.user_id = "test_user"
        self.mock_user.to_dict.return_value = {
            "user_id": "test_user",
            "name": "Test User",
            "cards": [],
            "income": [],
            "recurring_expenses": [],
            "transactions": [],
            "budget_categories": {},
            "savings": {"goal": 0, "current": 0},
            "savings_accounts": []
        }

    def tearDown(self):
        # Remove test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists("nonexistent_file.json"):
            os.remove("nonexistent_file.json")
        # Remove test directory
        os.rmdir(self.test_dir)

    def test_save_user_data_new_file(self):
        save_user_data(self.mock_user, self.test_file)

        # Verify file was created and contains correct data
        self.assertTrue(os.path.exists(self.test_file))
        with open(self.test_file, 'r') as f:
            saved_data = json.load(f)

        self.assertIn("users", saved_data)
        self.assertIn("test_user", saved_data["users"])
        self.assertEqual(saved_data["users"]["test_user"]["name"], "Test User")

    def test_save_user_data_existing_file(self):
        # Create initial file with existing data
        initial_data = {
            "users": {
                "existing_user": {"name": "Existing User"}
            }
        }
        with open(self.test_file, 'w') as f:
            json.dump(initial_data, f)

        save_user_data(self.mock_user, self.test_file)

        # Verify both users exist in file
        with open(self.test_file, 'r') as f:
            saved_data = json.load(f)

        self.assertIn("existing_user", saved_data["users"])
        self.assertIn("test_user", saved_data["users"])

    def test_save_user_data_preserve_password(self):
        # Create initial file with user data including password
        initial_data = {
            "users": {
                "test_user": {
                    "user_id": "test_user",
                    "password": "secret_password"
                }
            }
        }
        with open(self.test_file, 'w') as f:
            json.dump(initial_data, f)

        save_user_data(self.mock_user, self.test_file)

        # Verify password was preserved
        with open(self.test_file, 'r') as f:
            saved_data = json.load(f)

        self.assertEqual(saved_data["users"]["test_user"]["password"], "secret_password")


    def test_save_user_data_file_not_found(self):
        save_user_data(self.mock_user, "nonexistent_file.json")

        # Verify file was created and contains correct data
        self.assertTrue(os.path.exists("nonexistent_file.json"))
        with open("nonexistent_file.json", 'r') as f:
            saved_data = json.load(f)

        self.assertIn("users", saved_data)
        self.assertIn("test_user", saved_data["users"])
        self.assertEqual(saved_data["users"]["test_user"]["name"], "Test User")

if __name__ == '__main__':
    unittest.main()