"""
Unit tests for the Core class in dataeng_toolbox.
"""

import unittest
from dataeng_toolbox.core import Core


class TestCore(unittest.TestCase):
    """Test cases for the Core class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.core = Core()

    def test_initialization(self) -> None:
        """Test that Core class initializes correctly."""
        self.assertEqual(self.core.name, "DataEng Toolbox")
        self.assertEqual(self.core.version, "0.1.0")

    def test_hello_world(self) -> None:
        """Test the hello_world method."""
        expected_message = "Hello World from DataEng Toolbox v0.1.0!"
        actual_message = self.core.hello_world()
        self.assertEqual(actual_message, expected_message)

    def test_hello_world_return_type(self) -> None:
        """Test that hello_world returns a string."""
        result = self.core.hello_world()
        self.assertIsInstance(result, str)

    def test_get_info(self) -> None:
        """Test the get_info method."""
        info = self.core.get_info()

        self.assertIsInstance(info, dict)
        self.assertIn("name", info)
        self.assertIn("version", info)
        self.assertIn("description", info)

        self.assertEqual(info["name"], "DataEng Toolbox")
        self.assertEqual(info["version"], "0.1.0")
        self.assertEqual(info["description"], "A comprehensive data engineering toolbox for Python")


if __name__ == "__main__":
    unittest.main()
