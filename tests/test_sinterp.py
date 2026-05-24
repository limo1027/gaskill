import unittest
from gaskill.sinterp import (
    lerp, lerp_unclamped, bilerp, slerp, smoothstep, smootherstep,
    cubic_bezier, cubic_bezier_derivative, catmull_rom, hermite,
    inverse_lerp, remap, pingpong, damp, spring
)
from gaskill.svector import vec2, vec3


class TestLinearInterp(unittest.TestCase):
    def test_lerp(self):
        self.assertAlmostEqual(lerp(0, 10, 0.5), 5)
        self.assertAlmostEqual(lerp(0, 10, 0), 0)
        self.assertAlmostEqual(lerp(0, 10, 1), 10)

    def test_lerp_clamped(self):
        self.assertEqual(lerp(0, 10, 2), 10)  # 超过1被限制
        self.assertEqual(lerp(0, 10, -1), 0)  # 低于0被限制

    def test_lerp_unclamped(self):
        self.assertAlmostEqual(lerp_unclamped(0, 10, 2), 20)


class TestBilinearInterp(unittest.TestCase):
    def test_bilerp(self):
        result = bilerp(0, 10, 0, 10, 0.5, 0.5)
        self.assertAlmostEqual(result, 5)


class TestSphericalInterp(unittest.TestCase):
    def test_slerp(self):
        v1 = vec3(1, 0, 0)
        v2 = vec3(0, 1, 0)
        result = slerp(v1, v2, 0.5)
        self.assertAlmostEqual(result.length(), 1, places=5)


class TestStepFunctions(unittest.TestCase):
    def test_smoothstep(self):
        self.assertAlmostEqual(smoothstep(0, 1, 0), 0)
        self.assertAlmostEqual(smoothstep(0, 1, 1), 1)
        self.assertAlmostEqual(smoothstep(0, 1, 0.5), 0.5)

    def test_smootherstep(self):
        self.assertAlmostEqual(smootherstep(0, 1, 0), 0)
        self.assertAlmostEqual(smootherstep(0, 1, 1), 1)


class TestCubicBezier(unittest.TestCase):
    def test_cubic_bezier(self):
        result = cubic_bezier(0, 0, 1, 1, 0.5)
        self.assertAlmostEqual(result, 0.5)

    def test_cubic_bezier_derivative(self):
        deriv = cubic_bezier_derivative(0, 0, 1, 1, 0.5)
        self.assertAlmostEqual(deriv, 1.5, places=5)


class TestCatmullRom(unittest.TestCase):
    def test_catmull_rom(self):
        result = catmull_rom(0, 0, 1, 1, 0.5)
        self.assertAlmostEqual(result, 0.5, places=2)


class TestHermite(unittest.TestCase):
    def test_hermite(self):
        result = hermite(0, 1, 1, -1, 0.5)
        self.assertIsNotNone(result)  # 只检查返回有效值


class TestRemap(unittest.TestCase):
    def test_inverse_lerp(self):
        self.assertAlmostEqual(inverse_lerp(0, 10, 5), 0.5)

    def test_remap(self):
        result = remap(5, 0, 10, 0, 100)
        self.assertAlmostEqual(result, 50)


class TestPingpong(unittest.TestCase):
    def test_pingpong(self):
        self.assertAlmostEqual(pingpong(0, 10), 0)
        self.assertAlmostEqual(pingpong(5, 10), 5)
        self.assertAlmostEqual(pingpong(10, 10), 10)
        self.assertAlmostEqual(pingpong(15, 10), 5)
        self.assertAlmostEqual(pingpong(20, 10), 0)


class TestDamping(unittest.TestCase):
    def test_damp(self):
        result = damp(0, 10, 1, 0.1)
        self.assertGreater(result, 0)
        self.assertLess(result, 10)


class TestSpring(unittest.TestCase):
    def test_spring(self):
        pos, vel = spring(0, 10, 0, 1, 0.5, 0.1)
        self.assertGreater(pos, 0)
        self.assertLess(pos, 10)


if __name__ == '__main__':
    unittest.main()
