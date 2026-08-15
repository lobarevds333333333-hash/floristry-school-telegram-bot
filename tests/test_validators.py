import unittest
from utils.validators import validate_phone, validate_email

class TestValidators(unittest.TestCase):

    def test_validate_phone_russian_plus7(self):
        is_valid, formatted = validate_phone("+79991234567")
        self.assertTrue(is_valid)
        self.assertEqual(formatted, "+79991234567")

    def test_validate_phone_russian_8(self):
        is_valid, formatted = validate_phone("8 (999) 123-45-67")
        self.assertTrue(is_valid)
        self.assertEqual(formatted, "+79991234567")

    def test_validate_phone_invalid(self):
        is_valid, formatted = validate_phone("12345")
        self.assertFalse(is_valid)
        self.assertIsNone(formatted)

    def test_validate_email_valid(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name+tag@domain.co.uk"))

    def test_validate_email_invalid(self):
        self.assertFalse(validate_email("invalid_email"))
        self.assertFalse(validate_email("user@domain"))
        self.assertFalse(validate_email("@domain.com"))

if __name__ == "__main__":
    unittest.main()
