import unittest
from unittest.mock import MagicMock, patch
from logic.auth import *
from logic.models import User


class TestAuth(unittest.TestCase):
    def setUp(self):
        # Sample test data
        self.test_data = {
            "users": {
                "testuser": {
                    "user_id": "testuser",
                    "password": "testpass",
                    "cards": [],
                    "income": [],
                    "recurring_expenses": [],
                    "budget_categories": [],
                    "transactions": [],
                    "savings_accounts": [],
                    "savings": {"goal": 0, "current": 0}
                },
                "testuser2" : {
                    "user_id": "testuser2",
                    "password": "testpass2",
                    "cards": [],
                    "income": [],
                    "recurring_expenses": [],
                    "budget_categories": [],
                    "transactions": [],
                    "savings_accounts": [],
                    "savings": {"goal": 0, "current": 0}
                }
            }
        }

        # Create mock for json operations
        self.mock_json = MagicMock()
        self.mock_json.load.return_value = self.test_data

        # Create mock for file operations
        self.mock_file = MagicMock()
        self.mock_open = MagicMock(return_value=self.mock_file)

    @patch('builtins.open')
    @patch('json.load')
    def test_load_all_users(self, mock_json_load, mock_open):
        # Test successful load
        mock_json_load.return_value = self.test_data
        result = load_all_users()
        mock_open.assert_called_once_with("data.json", "r")
        self.assertEqual(result, self.test_data)

        # Test loading when file not found
        mock_open.side_effect = FileNotFoundError
        result = load_all_users()
        self.assertEqual(result, {"users": {}})

    @patch('logic.auth.load_all_users')
    def test_get_user(self, mock_load):
        mock_load.return_value = self.test_data

        # Test successful login
        user = get_user("testuser", "testpass")
        user2 = get_user("testuser2", "testpass2")
        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, "testuser")
        self.assertIsNotNone(user2)
        self.assertEqual(user2.user_id, "testuser2")

        # Test wrong password
        user = get_user("testuser", "wrongpass")
        user2 = get_user("testuser2", "wrongpass2")
        self.assertIsNone(user)
        self.assertIsNone(user2)

        # Test nonexistent user
        user = get_user("nonexistent")
        user2 = get_user("nonexistent2")
        self.assertIsNone(user)
        self.assertIsNone(user2)

    @patch('builtins.input')
    @patch('logic.auth.load_all_users')
    @patch('logic.auth.save_all_users')
    def test_create_user(self, mock_save, mock_load, mock_input):
        # Set up mocks
        mock_load.return_value = self.test_data
        mock_input.return_value = "testpass"

        # Test creating new user
        user = create_user("newuser")
        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, "newuser")
        mock_save.assert_called_once()

        # Test creating duplicate user
        user = create_user("testuser")
        self.assertIsNone(user)

    @patch('logic.auth.load_all_users')
    @patch('logic.auth.save_all_users')
    def test_delete_user(self, mock_save, mock_load):
        # Set up mock
        test_data = self.test_data.copy()
        mock_load.return_value = test_data

        # Test deleting existing user
        delete_user("testuser")
        mock_save.assert_called_once()
        self.assertNotIn("testuser", test_data["users"])

        # Test deleting non-existent user
        mock_load.return_value = {"users": {}}
        delete_user("nonexistent")
        mock_save.assert_called_once()
        self.assertNotIn("nonexistent", test_data["users"])

    @patch('logic.auth.load_all_users')
    def test_list_users(self, mock_load):
        mock_load.return_value = self.test_data
        users = list_users()
        self.assertEqual(users, ["testuser", "testuser2"])

    @patch('logic.auth.load_all_users')
    @patch('logic.auth.save_all_users')
    def test_save_single_user(self, mock_save, mock_load):
        mock_load.return_value = self.test_data

        # Create test user
        test_user = User("testuser")

        # Test saving user
        save_single_user(test_user)
        mock_save.assert_called_once()

        # Verify the password was preserved
        saved_data = mock_save.call_args[0][0]
        self.assertEqual(saved_data["users"]["testuser"]["password"], "testpass")

    def test_user_to_dict(self):
        # Test User object serialization
        user = User("testuser")
        user_dict = user.to_dict()

        self.assertEqual(user_dict["user_id"], "testuser")
        self.assertEqual(user_dict["cards"], [])
        self.assertEqual(user_dict["income"], [])
        self.assertEqual(user_dict["recurring_expenses"], [])
        self.assertEqual(user_dict["budget_categories"], [])
        self.assertEqual(user_dict["transactions"], [])
        self.assertEqual(user_dict["savings"], {"goal": 0, "current": 0})
        self.assertEqual(user_dict["savings_accounts"], [])


if __name__ == '__main__':
    unittest.main()