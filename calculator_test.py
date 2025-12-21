from unittest import TestCase
from calculator_lambda import calculator

class CalculatorTest(TestCase):
    def test_good_request(self):
        event={"Records":[{"Sns":{"Message": '{"op1": 1.7, "op2": 2.3, "operation": "+"}', "someother": "data"}}]}
        result = calculator(event, None)
        self.assertEqual(result, 4.0)
        
    def test_bad_request(self):
        event={"Records":[{"Sns":{"Message": '{"op1": 1, "op2": 2, "operation": "bad"}', "someother": "data"}}]}
        with self.assertRaises(ValueError):
            calculator(event, None)
        event={"Records":[{"Sns":{"Message": '{"op1": 1, "op2": 0, "operation": "/"}', "someother": "data"}}]}
        self.assertIsNone(calculator(event, None))
