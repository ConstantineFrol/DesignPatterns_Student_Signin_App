import unittest
from unittest.mock import Mock

from Utilities.WebcamManager import WebcamManager


class TestWebcamManagerSingleton(unittest.TestCase):
    def setUp(self):
        # Reset the singleton instance before each test
        WebcamManager._instance = None

    def test_singleton_instance(self):
        # Ensure that creating multiple instances returns the same instance (singleton)
        instance1 = WebcamManager()
        instance2 = WebcamManager()
        self.assertIs(instance1, instance2)


if __name__ == '__main__':
    unittest.main()
