import unittest
from run import app

class TestCalculateVelocity(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_valid_points(self):
        # Test with valid points
        response = self.app.post('/calculate_velocity', data={'points': '5,10,15'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_velocity', response.json)
        self.assertEqual(response.json['average_velocity'], 10)

    def test_empty_points(self):
        # Test with empty points
        response = self.app.post('/calculate_velocity', data={'points': ''})
        self.assertEqual(response.status_code, 400)

    def test_invalid_points(self):
        # Test with invalid points (non-integer values)
        response = self.app.post('/calculate_velocity', data={'points': '5,ten,15'})
        self.assertEqual(response.status_code, 400)

    def test_single_point(self):
        # Test with a single point
        response = self.app.post('/calculate_velocity', data={'points': '10'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_velocity', response.json)
        self.assertEqual(response.json['average_velocity'], 10)

    def test_negative_points(self):
        # Test with negative points
        response = self.app.post('/calculate_velocity', data={'points': '-5,-10,-15'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_velocity', response.json)
        self.assertEqual(response.json['average_velocity'], -10)

    def test_large_number_of_points(self):
        # Test with a large number of points
        large_points = '1,' * 1000
        response = self.app.post('/calculate_velocity', data={'points': large_points})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
