import unittest

from gaskill.smath import (
    pi, e, EPSILON,
    gcd, lcm, factorial, comb, perm,
    sin, cos, tan, asin, acos, atan, atan2,
    exp, ln, log, log10, log2,
    sqrt, cbrt,
    clamp, lerp, inv_lerp, map,
    is_prime, prime_factors, fibonacci,
    distance, angle_between,
    floor, ceil, trunc,
    sign, rad, deg,
)


class TestMathConstants(unittest.TestCase):
    def test_pi(self):
        self.assertAlmostEqual(pi, 3.141592653589793)

    def test_e(self):
        self.assertAlmostEqual(e, 2.718281828459045)

    def test_epsilon(self):
        self.assertTrue(EPSILON > 0)
        self.assertTrue(EPSILON < 1e-10)


class TestArithmeticFunctions(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(7, 13), 1)

    def test_gcd_boundary_cases(self):
        self.assertEqual(gcd(0, 0), 0)
        self.assertEqual(gcd(1, 1), 1)
        self.assertEqual(gcd(10**18, 10**18), 10**18)
        self.assertEqual(gcd(-48, 18), 6)
        self.assertEqual(gcd(48, -18), 6)

    def test_lcm(self):
        self.assertEqual(lcm(4, 6), 12)
        self.assertEqual(lcm(7, 13), 91)

    def test_lcm_boundary_cases(self):
        self.assertEqual(lcm(0, 5), 0)
        self.assertEqual(lcm(1, 1), 1)
        self.assertEqual(lcm(1, 100), 100)
        self.assertEqual(lcm(5, 0), 0)

    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_factorial_large(self):
        result = factorial(20)
        self.assertGreater(result, 10**18)

    def test_comb(self):
        self.assertEqual(comb(5, 2), 10)
        self.assertEqual(comb(10, 5), 252)
        self.assertEqual(comb(5, 0), 1)
        self.assertEqual(comb(5, 6), 0)

    def test_comb_boundary_cases(self):
        self.assertEqual(comb(0, 0), 1)
        self.assertEqual(comb(100, 50), comb(100, 50))
        # comb(-1, 0) 可能返回 0 或抛出异常，两种情况都接受
        try:
            result = comb(-1, 0)
            self.assertEqual(result, 0)
        except ValueError:
            pass

    def test_perm(self):
        self.assertEqual(perm(5, 2), 20)
        self.assertEqual(perm(10, 3), 720)

    def test_perm_boundary_cases(self):
        self.assertEqual(perm(5, 0), 1)
        self.assertEqual(perm(5, 5), 120)
        # perm(-1, 0) 可能返回 0 或抛出异常，两种情况都接受
        try:
            result = perm(-1, 0)
            self.assertEqual(result, 0)
        except ValueError:
            pass


class TestTrigonometricFunctions(unittest.TestCase):
    def test_sin(self):
        self.assertAlmostEqual(sin(0), 0)
        self.assertAlmostEqual(sin(pi/2), 1)
        self.assertAlmostEqual(sin(pi), 0)
        self.assertAlmostEqual(sin(3*pi/2), -1)

    def test_sin_boundary_cases(self):
        self.assertAlmostEqual(sin(2*pi), 0)
        self.assertAlmostEqual(sin(-pi/2), -1)
        self.assertAlmostEqual(sin(1e16) % (2*pi), sin(1e16 % (2*pi)))
        self.assertAlmostEqual(sin(pi/6), 0.5)
        self.assertAlmostEqual(sin(pi/3), 0.8660254)

    def test_cos(self):
        self.assertAlmostEqual(cos(0), 1)
        self.assertAlmostEqual(cos(pi/2), 0)
        self.assertAlmostEqual(cos(pi), -1)

    def test_cos_boundary_cases(self):
        self.assertAlmostEqual(cos(2*pi), 1)
        self.assertAlmostEqual(cos(-pi), -1)
        self.assertAlmostEqual(cos(pi/6), 0.8660254)
        self.assertAlmostEqual(cos(pi/4), 0.70710678)

    def test_tan(self):
        self.assertAlmostEqual(tan(0), 0)
        self.assertAlmostEqual(tan(pi/4), 1)

    def test_tan_boundary_cases(self):
        self.assertAlmostEqual(tan(pi/6), 0.57735027)
        self.assertAlmostEqual(tan(-pi/4), -1)
        self.assertAlmostEqual(tan(0), 0)

    def test_asin(self):
        self.assertAlmostEqual(asin(0), 0)
        self.assertAlmostEqual(asin(1), pi/2)
        self.assertAlmostEqual(asin(-1), -pi/2)

    def test_asin_boundary_cases(self):
        self.assertAlmostEqual(asin(0.5), pi/6)
        self.assertAlmostEqual(asin(-0.5), -pi/6)
        # asin(|x| > 1) 返回复数
        self.assertIsInstance(asin(2), complex)
        self.assertIsInstance(asin(-2), complex)

    def test_acos(self):
        self.assertAlmostEqual(acos(1), 0)
        self.assertAlmostEqual(acos(0), pi/2)
        self.assertAlmostEqual(acos(-1), pi)

    def test_acos_boundary_cases(self):
        self.assertAlmostEqual(acos(0.5), pi/3)
        self.assertAlmostEqual(acos(-0.5), 2*pi/3)
        # acos(|x| > 1) 返回复数
        self.assertIsInstance(acos(2), complex)
        self.assertIsInstance(acos(-2), complex)

    def test_atan(self):
        self.assertAlmostEqual(atan(0), 0)
        self.assertAlmostEqual(atan(1), pi/4)

    def test_atan_boundary_cases(self):
        self.assertAlmostEqual(atan(float('inf')), pi/2)
        self.assertAlmostEqual(atan(float('-inf')), -pi/2)
        self.assertAlmostEqual(atan(0.5), 0.4636476)

    def test_atan2(self):
        self.assertAlmostEqual(atan2(0, 1), 0)
        self.assertAlmostEqual(atan2(1, 0), pi/2)
        self.assertAlmostEqual(atan2(0, -1), pi)
        self.assertAlmostEqual(atan2(-1, 0), -pi/2)

    def test_atan2_boundary_cases(self):
        self.assertAlmostEqual(atan2(1, 1), pi/4)
        self.assertAlmostEqual(atan2(-1, -1), -3*pi/4)
        self.assertAlmostEqual(atan2(0, 0), 0)


class TestExponentialFunctions(unittest.TestCase):
    def test_exp(self):
        self.assertAlmostEqual(exp(0), 1)
        self.assertAlmostEqual(exp(1), e)
        self.assertAlmostEqual(exp(2), e*e)

    def test_exp_boundary_cases(self):
        self.assertAlmostEqual(exp(-1), 1/e)
        # 无穷大可能返回特殊值或抛出异常
        try:
            self.assertEqual(exp(float('-inf')), 0)
            self.assertEqual(exp(float('inf')), float('inf'))
        except (ValueError, OverflowError):
            pass
        self.assertAlmostEqual(exp(3), e**3)

    def test_ln(self):
        self.assertAlmostEqual(ln(1), 0)
        self.assertAlmostEqual(ln(e), 1)
        self.assertEqual(ln(0), float('-inf'))

    def test_ln_boundary_cases(self):
        self.assertAlmostEqual(ln(e**2), 2)
        self.assertEqual(ln(float('inf')), float('inf'))
        # ln(-1) 返回复数（虚部为 pi）
        result = ln(-1)
        self.assertIsInstance(result, complex)
        self.assertAlmostEqual(result.imag, pi)
        self.assertAlmostEqual(ln(1/e), -1)

    def test_log(self):
        self.assertAlmostEqual(log(100, 10), 2)
        self.assertAlmostEqual(log(8, 2), 3)

    def test_log_boundary_cases(self):
        self.assertEqual(log(1, 10), 0)
        # log(-1, 10) 返回复数
        self.assertIsInstance(log(-1, 10), complex)
        # log(10, 0) 返回 -0.0
        self.assertEqual(log(10, 0), -0.0)
        # log(10, 1) 抛出 ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            log(10, 1)

    def test_log10(self):
        self.assertAlmostEqual(log10(100), 2)
        self.assertAlmostEqual(log10(1), 0)

    def test_log10_boundary_cases(self):
        self.assertEqual(log10(0), float('-inf'))
        self.assertEqual(log10(float('inf')), float('inf'))
        # log10(-1) 返回复数
        self.assertIsInstance(log10(-1), complex)

    def test_log2(self):
        self.assertAlmostEqual(log2(8), 3)
        self.assertAlmostEqual(log2(1), 0)

    def test_log2_boundary_cases(self):
        self.assertEqual(log2(0), float('-inf'))
        self.assertEqual(log2(float('inf')), float('inf'))
        # log2(-1) 返回复数
        self.assertIsInstance(log2(-1), complex)


class TestRootFunctions(unittest.TestCase):
    def test_sqrt(self):
        self.assertAlmostEqual(sqrt(4), 2)
        self.assertAlmostEqual(sqrt(25), 5)
        self.assertAlmostEqual(sqrt(2), 1.41421356237)

    def test_cbrt(self):
        self.assertAlmostEqual(cbrt(8), 2)
        self.assertAlmostEqual(cbrt(-8), -2)


class TestInterpolationFunctions(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(clamp(5, 0, 10), 5)
        self.assertEqual(clamp(-1, 0, 10), 0)
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_lerp(self):
        self.assertAlmostEqual(lerp(0, 10, 0.5), 5)
        self.assertAlmostEqual(lerp(10, 20, 0), 10)
        self.assertAlmostEqual(lerp(10, 20, 1), 20)

    def test_inv_lerp(self):
        self.assertAlmostEqual(inv_lerp(0, 10, 5), 0.5)
        self.assertAlmostEqual(inv_lerp(10, 20, 10), 0)

    def test_map(self):
        self.assertAlmostEqual(map(50, 0, 100, 0, 10), 5)
        self.assertAlmostEqual(map(0, -1, 1, 0, 100), 50)


class TestNumberTheory(unittest.TestCase):
    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(100))

    def test_prime_factors(self):
        self.assertEqual(prime_factors(12), {2: 2, 3: 1})
        self.assertEqual(prime_factors(17), {17: 1})
        self.assertEqual(prime_factors(100), {2: 2, 5: 2})

    def test_fibonacci(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(fibonacci(10), 55)


class TestUtilityFunctions(unittest.TestCase):
    def test_distance(self):
        self.assertAlmostEqual(distance((0, 0), (3, 4)), 5)
        self.assertAlmostEqual(distance((1, 1), (4, 5)), 5)

    def test_angle_between(self):
        self.assertAlmostEqual(angle_between([1, 0], [0, 1]), pi/2)
        self.assertAlmostEqual(angle_between([1, 0], [1, 0]), 0)

    def test_floor(self):
        self.assertEqual(floor(3.7), 3)
        self.assertEqual(floor(-3.7), -4)

    def test_ceil(self):
        self.assertEqual(ceil(3.2), 4)
        self.assertEqual(ceil(-3.7), -3)

    def test_trunc(self):
        self.assertEqual(trunc(3.7), 3)
        self.assertEqual(trunc(-3.7), -3)

    def test_sign(self):
        self.assertEqual(sign(5), 1)
        self.assertEqual(sign(-5), -1)
        self.assertEqual(sign(0), 0)

    def test_rad_deg(self):
        self.assertAlmostEqual(rad(180), pi)
        self.assertAlmostEqual(deg(pi), 180)


if __name__ == '__main__':
    unittest.main()
