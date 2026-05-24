import unittest

from gaskill.sfrac import Frac, is_int


class TestFrac(unittest.TestCase):
    def test_init_integer(self):
        f = Frac(5)
        self.assertEqual(f.n, 5)
        self.assertEqual(f.d, 1)

    def test_init_fraction(self):
        f = Frac(1, 2)
        self.assertEqual(f.n, 1)
        self.assertEqual(f.d, 2)

    def test_init_float(self):
        f = Frac(0.5)
        self.assertEqual(f.n, 1)
        self.assertEqual(f.d, 2)

    def test_auto_simplify(self):
        f = Frac(2, 4)
        self.assertEqual(f.n, 1)
        self.assertEqual(f.d, 2)

    def test_negative(self):
        f = Frac(-1, 2)
        self.assertEqual(f.n, -1)
        self.assertEqual(f.d, 2)

    def test_zero_denominator(self):
        with self.assertRaises(ValueError):
            Frac(1, 0)

    def test_divide_by_zero(self):
        f = Frac(1, 2)
        with self.assertRaises(ZeroDivisionError):
            f / 0


class TestFracOperations(unittest.TestCase):
    def test_addition(self):
        f1 = Frac(1, 2)
        f2 = Frac(1, 3)
        result = f1 + f2
        self.assertEqual(result.n, 5)
        self.assertEqual(result.d, 6)

    def test_subtraction(self):
        f1 = Frac(1, 2)
        f2 = Frac(1, 4)
        result = f1 - f2
        self.assertEqual(result.n, 1)
        self.assertEqual(result.d, 4)

    def test_multiplication(self):
        f1 = Frac(1, 2)
        f2 = Frac(2, 3)
        result = f1 * f2
        # 自动约分后应该是 1/3
        self.assertEqual(float(result), 1/3)

    def test_division(self):
        f1 = Frac(1, 2)
        f2 = Frac(2, 3)
        result = f1 / f2
        self.assertEqual(result.n, 3)
        self.assertEqual(result.d, 4)

    def test_power(self):
        f = Frac(2, 3)
        result = f ** 2
        self.assertEqual(result.n, 4)
        self.assertEqual(result.d, 9)

    def test_power_negative(self):
        f = Frac(2, 3)
        result = f ** (-1)
        self.assertEqual(result.n, 3)
        self.assertEqual(result.d, 2)

    def test_inverse(self):
        f = Frac(2, 3)
        inv = ~f
        self.assertEqual(inv.n, 3)
        self.assertEqual(inv.d, 2)

    def test_abs(self):
        f = Frac(-3, 4)
        result = abs(f)
        self.assertEqual(result.n, 3)
        self.assertEqual(result.d, 4)


class TestFracComparison(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(Frac(1, 2), Frac(2, 4))
        self.assertEqual(Frac(5), Frac(5, 1))

    def test_less_than(self):
        self.assertTrue(Frac(1, 3) < Frac(1, 2))
        self.assertTrue(Frac(1, 2) > Frac(1, 3))

    def test_comparison_boundary_cases(self):
        self.assertTrue(Frac(0, 1) < Frac(1, 1))
        self.assertTrue(Frac(-1, 1) < Frac(0, 1))
        self.assertTrue(Frac(-1, 2) > Frac(-1, 1))

    def test_zero_comparison(self):
        self.assertEqual(Frac(0, 5), Frac(0, 1))
        self.assertTrue(Frac(0, 1) < Frac(1, 1))


class TestFracSpecialCases(unittest.TestCase):
    def test_zero_fraction(self):
        f = Frac(0, 5)
        self.assertEqual(f.n, 0)
        self.assertEqual(f.d, 1)

    def test_one_fraction(self):
        f = Frac(5, 5)
        self.assertEqual(f.n, 1)
        self.assertEqual(f.d, 1)

    def test_large_numbers(self):
        f = Frac(10**18, 10**18)
        self.assertEqual(f.n, 1)
        self.assertEqual(f.d, 1)

    def test_add_zero(self):
        f = Frac(1, 2)
        result = f + Frac(0, 1)
        self.assertEqual(result, f)

    def test_multiply_zero(self):
        f = Frac(1, 2)
        result = f * Frac(0, 1)
        self.assertEqual(result.n, 0)

    def test_multiply_one(self):
        f = Frac(1, 2)
        result = f * Frac(1, 1)
        self.assertEqual(result, f)

    def test_divide_one(self):
        f = Frac(1, 2)
        result = f / Frac(1, 1)
        self.assertEqual(result, f)

    def test_power_zero(self):
        f = Frac(2, 3)
        result = f ** 0
        self.assertEqual(result.n, 1)
        self.assertEqual(result.d, 1)

    def test_large_exponent(self):
        f = Frac(2, 1)
        result = f ** 30
        self.assertEqual(result.n, 2**30)
        self.assertEqual(result.d, 1)

    def test_reciprocal_nonzero(self):
        f = Frac(2, 3)
        inv = ~f
        self.assertEqual(inv.n, 3)
        self.assertEqual(inv.d, 2)

    def test_divide_by_fraction(self):
        f1 = Frac(1, 2)
        f2 = Frac(1, 4)
        result = f1 / f2
        self.assertEqual(result.n, 2)
        self.assertEqual(result.d, 1)

    def test_sorting(self):
        fracs = [Frac(1, 3), Frac(1, 2), Frac(2, 3)]
        sorted_fracs = sorted(fracs)
        self.assertEqual(sorted_fracs[0], Frac(1, 3))
        self.assertEqual(sorted_fracs[-1], Frac(2, 3))


class TestFracConversion(unittest.TestCase):
    def test_float(self):
        f = Frac(1, 2)
        self.assertEqual(float(f), 0.5)

    def test_int(self):
        f = Frac(7, 2)
        self.assertEqual(int(f), 3)

    def test_round(self):
        f = Frac(7, 3)
        self.assertAlmostEqual(round(f, 2), 2.33, places=2)


class TestFracFormat(unittest.TestCase):
    def test_format_percent(self):
        f = Frac(1, 2)
        self.assertEqual(f"{f:%}", "50%")

    def test_format_mixed(self):
        f = Frac(7, 4)
        result = f"{f:m}"
        self.assertIn('1', result)

    def test_format_latex(self):
        f = Frac(1, 2)
        result = f"{f:l}"
        self.assertIn('frac', result)


class TestIsInt(unittest.TestCase):
    def test_is_int_true(self):
        self.assertTrue(is_int(5.0))
        self.assertTrue(is_int(3.0))

    def test_is_int_false(self):
        self.assertFalse(is_int(5.1))
        self.assertFalse(is_int(3.14))


if __name__ == '__main__':
    unittest.main()
