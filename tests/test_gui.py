import unittest
import string

from baseconvgui import OnValidateGiven


class OnValidateGivenTest(unittest.TestCase):

    def test_valid(self):
        self.assertTrue(OnValidateGiven(string.digits[0], string.digits))

    def test_invalid(self):
        self.assertFalse(OnValidateGiven('*', string.digits))


if __name__ == "__main__":
    unittest.main()
