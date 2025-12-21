from unittest import TestCase
from calculator_lambda import calculator

class CalculatorTest(TestCase):
    def test_good_request(self):
        event={"Records":[{"Sns":{"Message": '{"op1": 1.7, "op2": 2.3, "operation": "+"}', "someother": "data"}}]}
        result = calculator(event, None)
        self.assertEqual(result, 4.0)
        
    def test_bad_request(self):
        event={"Records":[{"Sns":{"Message": '{"op1": 1, "op2": 2, "operation": "bad"}', "someother": "data"}}]}
        result = calculator(event, None)
        self.assertIsNone(result)
        event={"Records":[{"Sns":{"Message": '{"nothing": 1}', "someother": "data"}}]}
        self.assertIsNone(calculator(event, None))
        event={"Records":[{"Sns":{"Message": '{"op1": 1, "op2": 0, "operation": "/"}', "someother": "data"}}]}
        self.assertIsNone(calculator(event, None))
        event={"Records":[{"Sns":{"Message": '{"op1": "smth", "op2": 2, "operation": "bad"}', "someother": "data"}}]}
        self.assertIsNone(calculator(event, None))