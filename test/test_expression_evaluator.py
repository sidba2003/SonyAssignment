import unittest
from src.evaluator import Evaluator

class TestExpressionEvaluator(unittest.TestCase):
    def test_simple_addition_expression(self):
        self.assertEqual(Evaluator.expression_evaluator('1 + 9'), 10)
        

    def test_simple_computation_expression(self):
        self.assertEqual(Evaluator.expression_evaluator('1 - 2 + 3'), 2)
    
    
    def test_simple_computation_with_multiplication_expression(self):
        self.assertEqual(Evaluator.expression_evaluator('3 + 4 * 2'), 14)
    
    
    def test_simple_nested_expression_correctness_with_division(self):
        self.assertEqual(Evaluator.expression_evaluator('(4 / 2) + 6'), 8)
    
    
    def test_simple_nested_expression_correctness_with_multiplication(self):
        self.assertEqual(Evaluator.expression_evaluator('(1 + 3) * 2'), 8)
    
    
    def test_complex_nested_expression_correctness(self):
        self.assertEqual(Evaluator.expression_evaluator('(1 + (6 / 3 + 2) / 5) * (2 * (1 * 5))'), 10)
    
    
    def test_invalidity_for_number_greater_than_9(self):
        self.assertEqual(Evaluator.expression_evaluator('4 + (12 / (1 * 2))'), None)
    
    
    def test_division_by_zero(self):
        self.assertEqual(Evaluator.expression_evaluator('1 + (9 * 9) / 0'), None)
    
    
    def test_empty_bracket_expression(self):
        self.assertEqual(Evaluator.expression_evaluator('() + 10'), None)
    
    
    def test_operator_misplacement(self):
        self.assertEqual(Evaluator.expression_evaluator('3 / (- 2 1)'), None)
    
    
    def test_nested_operator_misplacement(self):
        self.assertEqual(Evaluator.expression_evaluator('3 / (2 + (3 2 -))'), None)
    
    
    def test_higher_opening_brackets_inequality(self):
        self.assertEqual(Evaluator.expression_evaluator('(1 + (12 * 2)'), None)
    
    
    def test_higher_closing_brackets_inequality(self):
        self.assertEqual(Evaluator.expression_evaluator('(1 + 10 )) + (12 * 2)'), None)