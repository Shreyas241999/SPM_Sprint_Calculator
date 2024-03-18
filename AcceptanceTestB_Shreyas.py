import unittest
from run import app

class TestFeatureBAcceptance(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()


    def test_calculate_capacity(self):
        # Happy path: Test calculating team effort-hour capacity with valid input
        valid_input_data = {
            "days": 10,
            "details": [
                {"max_hours": 8, "min_hours": 6, "pto_days": 1, "ceremony_days": 1},
                {"max_hours": 9, "min_hours": 7, "pto_days": 2, "ceremony_days": 2}
            ]
        }
        response = self.app.post('/calculate_capacity', json=valid_input_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_hours_per_person', response.json)
        self.assertIn('total_hours', response.json)

    def test_calculate_capacity_with_missing_days(self):
        # Unhappy path: Test calculating team effort-hour capacity with missing days
        invalid_input_data = {
            "details": [
                {"max_hours": 8, "min_hours": 6, "pto_days": 1, "ceremony_days": 1},
                {"max_hours": 9, "min_hours": 7, "pto_days": 2, "ceremony_days": 2}
            ]
        }
        response = self.app.post('/calculate_capacity', json=invalid_input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Invalid Input')

    def test_calculate_capacity_with_invalid_days(self):
        # Unhappy path: Test calculating team effort-hour capacity with invalid days
        invalid_input_data = {
            "days": "ten",
            "details": [
                {"max_hours": 8, "min_hours": 6, "pto_days": 1, "ceremony_days": 1},
                {"max_hours": 9, "min_hours": 7, "pto_days": 2, "ceremony_days": 2}
            ]
        }
        response = self.app.post('/calculate_capacity', json=invalid_input_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Invalid Input')

if __name__ == '__main__':
    unittest.main()
