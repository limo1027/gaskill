import unittest

from gaskill.sgeometry import Polygon, Rect, Circle, Line2, rect, circle, line, reflect
from gaskill.svector import vec2


class TestPolygon(unittest.TestCase):
    def test_init(self):
        points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        poly = Polygon(points)
        self.assertEqual(len(poly.vertices), 4)

    def test_contains_point_inside(self):
        points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        poly = Polygon(points)
        self.assertTrue(poly.contains_point(vec2(50, 50)))

    def test_contains_point_outside(self):
        points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        poly = Polygon(points)
        self.assertFalse(poly.contains_point(vec2(150, 150)))

    def test_get_aabb(self):
        points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        poly = Polygon(points)
        x, y, w, h = poly.get_aabb()
        self.assertEqual(w, 100)
        self.assertEqual(h, 100)

    def test_move(self):
        points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        poly = Polygon(points)
        moved = poly.move(10, 20)
        self.assertEqual(moved.vertices[0].x, 10)
        self.assertEqual(moved.vertices[0].y, 20)


class TestRect(unittest.TestCase):
    def test_init(self):
        r = Rect(10, 20, 100, 50)
        self.assertEqual(r.x, 10)
        self.assertEqual(r.y, 20)
        self.assertEqual(r.w, 100)
        self.assertEqual(r.h, 50)

    def test_properties(self):
        r = Rect(10, 20, 100, 50)
        self.assertEqual(r.left, 10)
        self.assertEqual(r.right, 110)
        self.assertEqual(r.bottom, 70)
        self.assertEqual(r.area, 5000)

    def test_collide_point(self):
        r = Rect(10, 20, 100, 50)
        self.assertTrue(r.collide_point(50, 40))
        self.assertFalse(r.collide_point(200, 200))

    def test_collide_rect(self):
        r1 = Rect(0, 0, 50, 50)
        r2 = Rect(30, 30, 50, 50)
        self.assertTrue(r1.collide_rect(r2))

    def test_collide_rect_no_collision(self):
        r1 = Rect(0, 0, 50, 50)
        r2 = Rect(100, 100, 50, 50)
        self.assertFalse(r1.collide_rect(r2))

    def test_inflate(self):
        r = Rect(10, 10, 20, 20)
        inflated = r.inflate(10, 10)
        self.assertEqual(inflated.w, 30)
        self.assertEqual(inflated.h, 30)

    def test_factory_function(self):
        r = rect(10, 20, 100, 50)
        self.assertIsInstance(r, Rect)


class TestCircle(unittest.TestCase):
    def test_init(self):
        c = Circle((50, 50), 25)
        self.assertEqual(c.center.x, 50)
        self.assertEqual(c.radius, 25)

    def test_collide_point(self):
        c = Circle((50, 50), 25)
        self.assertTrue(c.collide_point(50, 50))
        self.assertFalse(c.collide_point(100, 100))

    def test_collide_circle(self):
        c1 = Circle((0, 0), 25)
        c2 = Circle((30, 0), 25)
        self.assertTrue(c1.collide_circle(c2))

    def test_area(self):
        import math
        c = Circle((0, 0), 1)
        self.assertAlmostEqual(c.area, math.pi)


class TestLine2(unittest.TestCase):
    def test_init(self):
        l = Line2((0, 0), (100, 100))
        self.assertIsInstance(l.p1, vec2)
        self.assertIsInstance(l.p2, vec2)

    def test_length(self):
        l = Line2((0, 0), (30, 40))
        self.assertAlmostEqual(l.length(), 50)

    def test_closest_point(self):
        l = Line2((0, 0), (100, 0))
        closest = l.closest_point(vec2(50, 50))
        self.assertAlmostEqual(closest.x, 50, places=5)
        self.assertAlmostEqual(closest.y, 0, places=5)

    def test_intersect_line(self):
        l1 = Line2((0, 0), (100, 100))
        l2 = Line2((0, 100), (100, 0))
        intersection = l1.intersect_line(l2)
        self.assertIsNotNone(intersection)


class TestReflect(unittest.TestCase):
    def test_reflect(self):
        v = vec2(1, -1)
        n = vec2(0, 1)
        result = reflect(v, n)
        self.assertAlmostEqual(result.x, 1)
        self.assertAlmostEqual(result.y, 1)


class TestCircleFactory(unittest.TestCase):
    def test_circle_factory(self):
        c = circle((50, 50), 25)
        self.assertIsInstance(c, Circle)


class TestLineFactory(unittest.TestCase):
    def test_line_factory(self):
        l = line((0, 0), (100, 100))
        self.assertIsInstance(l, Line2)


if __name__ == '__main__':
    unittest.main()
