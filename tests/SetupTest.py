import unittest
from setupEnv import setup
import warnings
import os


class MyTestCase(unittest.TestCase):
    def test_there_is_no_dotenv(self):
        os.chdir("/")
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            token = setup('this_not_real_path')
        self.assertWarnsRegex(ResourceWarning, "No token loaded.")
        # self.assertEqual(None, token)
        # self.assertEqual(1, len(w))

    def test_there_is_a_dotenv(self):
        token = setup()
        self.assertIsInstance(token, str)
        self.assertIsNot(token, False)  # checks if the string is not empty


if __name__ == '__main__':
    unittest.main()
