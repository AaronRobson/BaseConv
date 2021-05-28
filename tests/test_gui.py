import unittest
import string

from baseconvgui import on_validate_given


class OnValidateGivenTest(unittest.TestCase):

    def test_valid(self):
        self.assertTrue(on_validate_given(string.digits[0], string.digits))

    def test_invalid(self):
        self.assertFalse(on_validate_given('*', string.digits))


if __name__ == "__main__":
    unittest.main()
