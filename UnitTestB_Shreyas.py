import unittest
from run import app

class TestCalculateCapacity(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_valid_input(self):
        # Test with valid input
        data = {
            "days": 10,
            "details": [
                {"max_hours": 8, "min_hours": 6, "pto_days": 1, "ceremony_days": 1},
                {"max_hours": 9, "min_hours": 7, "pto_days": 2, "ceremony_days": 2}
            ]
        }
        response = self.app.post('/calculate_capacity', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_hours_per_person', response.json)
        self.assertIn('total_hours', response.json)

    def test_missing_days(self):
        # Test with missing days
        data = {
            "details": [
                {"max_hours": 8, "min_hours": 6, "pto_days": 1, "ceremony_days": 1},
                {"max_hours": 9, "min_hours": 7, "pto_days": 2, "ceremony_days": 2}
            ]
        }
        response = self.app.post('/calculate_capacity', json=data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_days(self):
        # Test with invalid days (non-integer value)
        data = {
            "days": "ten",
            "details": [
                {"max_hours": 8, "min_hours": 6, "pto_days": 1, "ceremony_days": 1},
                {"max_hours": 9, "min_hours": 7, "pto_days": 2, "ceremony_days": 2}
            ]
        }
        response = self.app.post('/calculate_capacity', json=data)
        self.assertEqual(response.status_code, 400)

    def test_empty_details(self):
        # Test with empty details
        data = {
            "days": 10,
            "details": []
        }
        response = self.app.post('/calculate_capacity', json=data)
        self.assertEqual(response.status_code, 400)

    def test_missing_details_fields(self):
        # Test with missing fields in details
        data = {
            "days": 10,
            "details": [
                {"max_hours": 8, "min_hours": 6},
                {"max_hours": 9, "min_hours": 7, "pto_days": 2, "ceremony_days": 2}
            ]
        }
        response = self.app.post('/calculate_capacity', json=data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
