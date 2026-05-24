import unittest

from gaskill.scurve import (
    quadratic_bezier, cubic_bezier, bezier, bezier_derivative,
    uniform_knots, clamped_knots, b_spline_curve,
    nurbs, bezier_path, bezier_length, de_casteljau_subdivide
)
from gaskill.svector import vec2, vec3


class TestBezier(unittest.TestCase):
    def test_quadratic_bezier_endpoints(self):
        p0 = vec2(0, 0)
        p1 = vec2(50, 50)
        p2 = vec2(100, 0)
        start = quadratic_bezier(p0, p1, p2, 0)
        end = quadratic_bezier(p0, p1, p2, 1)
        self.assertEqual(start.x, 0)
        self.assertEqual(end.x, 100)

    def test_cubic_bezier_endpoints(self):
        p0 = vec2(0, 0)
        p1 = vec2(25, 50)
        p2 = vec2(75, 50)
        p3 = vec2(100, 0)
        start = cubic_bezier(p0, p1, p2, p3, 0)
        end = cubic_bezier(p0, p1, p2, p3, 1)
        self.assertEqual(start.x, 0)
        self.assertEqual(end.x, 100)

    def test_bezier_two_points(self):
        p0 = vec2(0, 0)
        p1 = vec2(100, 100)
        result = bezier([p0, p1], 0.5)
        self.assertEqual(result.x, 50)
        self.assertEqual(result.y, 50)

    def test_bezier_derivative(self):
        p0 = vec2(0, 0)
        p1 = vec2(50, 50)
        p2 = vec2(100, 0)
        deriv = bezier_derivative([p0, p1, p2], 0.5)
        self.assertIsNotNone(deriv)


class TestBSpline(unittest.TestCase):
    def test_uniform_knots(self):
        knots = uniform_knots(3, 2)
        self.assertEqual(len(knots), 7)

    def test_clamped_knots(self):
        knots = clamped_knots(3, 2)
        self.assertEqual(knots[0], 0)
        self.assertEqual(knots[-1], 4)

    def test_b_spline_curve(self):
        points = [vec2(0, 0), vec2(50, 100), vec2(100, 0)]
        curve = b_spline_curve(points, degree=2, steps=10)
        self.assertTrue(len(curve) > 0)


class TestNURBS(unittest.TestCase):
    def test_nurbs_circle(self):
        points = [vec2(1, 0), vec2(0, 1), vec2(-1, 0), vec2(0, -1)]
        weights = [1, 1, 1, 1]
        knots = [0, 0, 0, 0, 1, 1, 1, 1]
        result = nurbs(points, weights, knots, 2, 0.25)
        self.assertIsNotNone(result)


class TestCurveAnalysis(unittest.TestCase):
    def test_bezier_path(self):
        points = [vec2(0, 0), vec2(50, 50), vec2(100, 0)]
        path = bezier_path(points, steps=10)
        self.assertEqual(len(path), 11)

    def test_bezier_length(self):
        points = [vec2(0, 0), vec2(100, 0)]
        length = bezier_length(points)
        self.assertAlmostEqual(length, 100, places=1)

    def test_de_casteljau_subdivide(self):
        points = [vec2(0, 0), vec2(50, 50), vec2(100, 0)]
        left, right = de_casteljau_subdivide(points, 0.5)
        self.assertTrue(len(left) > 0)
        self.assertTrue(len(right) > 0)


class TestCurveWithTuples(unittest.TestCase):
    def test_bezier_with_tuples(self):
        p0 = (0, 0)
        p1 = (50, 50)
        p2 = (100, 0)
        result = quadratic_bezier(p0, p1, p2, 0.5)
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
