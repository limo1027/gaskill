import unittest

from gaskill.solver import (
    solve_linear, solve_quadratic, solve_cubic, solve_polynomial,
    solve_polynomial_numerical, NoSolutionError, roots, poly
)


class TestSolveLinear(unittest.TestCase):
    def test_solve_linear(self):
        result = solve_linear(2, -4)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], 2)

    def test_solve_linear_no_solution(self):
        with self.assertRaises(NoSolutionError):
            solve_linear(0, 1)

    def test_solve_linear_infinite(self):
        result = solve_linear(0, 0)
        self.assertEqual(result, 'infinite')


class TestSolveQuadratic(unittest.TestCase):
    def test_solve_quadratic_single(self):
        result = solve_quadratic(1, -2, 1)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], 1)

    def test_solve_quadratic_double(self):
        result = solve_quadratic(1, 0, -1)
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(-1, result)

    def test_solve_quadratic_complex(self):
        result = solve_quadratic(1, 0, 1)
        self.assertEqual(len(result), 2)


class TestSolveCubic(unittest.TestCase):
    def test_solve_cubic(self):
        result = solve_cubic(1, 0, 0, 0)
        self.assertEqual(len(result), 3)


class TestSolvePolynomial(unittest.TestCase):
    def test_solve_polynomial_linear(self):
        result = solve_polynomial([2, -4])  # 2x - 4 = 0
        self.assertAlmostEqual(result[0], 2)

    def test_solve_polynomial_quadratic(self):
        result = solve_polynomial([1, 0, -1])  # x² - 1 = 0
        self.assertEqual(len(result), 2)


class TestSolvePolynomialNumerical(unittest.TestCase):
    def test_solve_polynomial_numerical(self):
        result = solve_polynomial_numerical([1, 0, -1])  # x² - 1 = 0
        self.assertTrue(len(result) >= 1)


class TestRoots(unittest.TestCase):
    def test_roots(self):
        result = roots([1, 0, -1])
        self.assertEqual(len(result), 2)


class TestPoly(unittest.TestCase):
    def test_poly(self):
        result = poly(2, [1, 0, -1])  # 2² - 1
        self.assertEqual(result, 3)

    def test_poly_linear(self):
        result = poly(3, [2, -4])  # 2*3 - 4
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()
