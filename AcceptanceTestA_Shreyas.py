import unittest
from run import app

class TestFeatureAAcceptance(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_calculate_velocity(self):
        # Happy path: Test calculating average velocity with valid points
        valid_points_data = {'points': '5,10,15'}
        response = self.app.post('/calculate_velocity', data=valid_points_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_velocity', response.json)
        self.assertEqual(response.json['average_velocity'], 10)

    def test_calculate_velocity_with_empty_points(self):
        # Unhappy path: Test calculating average velocity with empty points
        empty_points_data = {'points': ''}
        response = self.app.post('/calculate_velocity', data=empty_points_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Invalid Input')

    def test_calculate_velocity_with_invalid_points(self):
        # Unhappy path: Test calculating average velocity with invalid points
        invalid_points_data = {'points': '5,ten,15'}
        response = self.app.post('/calculate_velocity', data=invalid_points_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'Invalid Input')

if __name__ == '__main__':
    unittest.main()
