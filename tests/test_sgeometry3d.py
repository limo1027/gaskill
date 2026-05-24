import unittest
from gaskill.sgeometry3d import AABB, Ray, Sphere, Plane, project_3d_to_2d
from gaskill.svector import vec3


class TestAABB(unittest.TestCase):
    def test_init(self):
        aabb = AABB(vec3(0, 0, 0), vec3(10, 10, 10))
        self.assertEqual(aabb.min.x, 0)
        self.assertEqual(aabb.max.x, 10)

    def test_from_center_size(self):
        aabb = AABB.from_center_size(vec3(5, 5, 5), vec3(10, 10, 10))
        self.assertAlmostEqual(aabb.min.x, 0)
        self.assertAlmostEqual(aabb.max.x, 10)

    def test_center(self):
        aabb = AABB(vec3(0, 0, 0), vec3(10, 10, 10))
        center = aabb.center
        self.assertAlmostEqual(center.x, 5)
        self.assertAlmostEqual(center.y, 5)
        self.assertAlmostEqual(center.z, 5)

    def test_contains_point(self):
        aabb = AABB(vec3(0, 0, 0), vec3(10, 10, 10))
        self.assertTrue(aabb.contains_point(vec3(5, 5, 5)))
        self.assertFalse(aabb.contains_point(vec3(15, 15, 15)))

    def test_intersects_aabb(self):
        aabb1 = AABB(vec3(0, 0, 0), vec3(10, 10, 10))
        aabb2 = AABB(vec3(5, 5, 5), vec3(15, 15, 15))
        self.assertTrue(aabb1.intersects_aabb(aabb2))

    def test_expand(self):
        aabb = AABB(vec3(0, 0, 0), vec3(10, 10, 10))
        aabb.expand(vec3(20, 20, 20))
        self.assertAlmostEqual(aabb.max.x, 20)


class TestRay(unittest.TestCase):
    def test_init(self):
        ray = Ray(vec3(0, 0, 0), vec3(1, 0, 0))
        self.assertEqual(ray.origin.x, 0)
        self.assertEqual(ray.direction.x, 1)

    def test_point_at(self):
        ray = Ray(vec3(0, 0, 0), vec3(1, 0, 0))
        point = ray.point_at(5)
        self.assertAlmostEqual(point.x, 5)

    def test_intersect_sphere(self):
        ray = Ray(vec3(0, 0, 0), vec3(1, 0, 0))
        hit, t1, t2 = ray.intersect_sphere(vec3(5, 0, 0), 2)
        self.assertTrue(hit)

    def test_intersect_plane(self):
        ray = Ray(vec3(0, 0, 0), vec3(0, 1, 0))
        hit, t = ray.intersect_plane(vec3(0, 5, 0), vec3(0, 1, 0))
        self.assertTrue(hit)
        self.assertAlmostEqual(t, 5)

    def test_intersect_aabb(self):
        ray = Ray(vec3(0, 0, 0), vec3(1, 0, 0))
        aabb = AABB(vec3(5, -1, -1), vec3(10, 1, 1))
        hit, tmin, tmax = ray.intersect_aabb(aabb)
        self.assertTrue(hit)


class TestSphere(unittest.TestCase):
    def test_init(self):
        sphere = Sphere(vec3(0, 0, 0), 5)
        self.assertEqual(sphere.radius, 5)

    def test_contains_point(self):
        sphere = Sphere(vec3(0, 0, 0), 5)
        self.assertTrue(sphere.contains_point(vec3(0, 0, 0)))
        self.assertFalse(sphere.contains_point(vec3(10, 10, 10)))

    def test_intersects_sphere(self):
        s1 = Sphere(vec3(0, 0, 0), 5)
        s2 = Sphere(vec3(8, 0, 0), 5)
        self.assertTrue(s1.intersects_sphere(s2))

    def test_volume(self):
        import math
        sphere = Sphere(vec3(0, 0, 0), 1)
        self.assertAlmostEqual(sphere.volume(), 4/3 * math.pi, places=5)


class TestPlane(unittest.TestCase):
    def test_init(self):
        plane = Plane(vec3(0, 1, 0), vec3(0, 0, 0))
        self.assertIsNotNone(plane.normal)

    def test_from_three_points(self):
        p1 = vec3(0, 0, 0)
        p2 = vec3(1, 0, 0)
        p3 = vec3(0, 1, 0)
        plane = Plane.from_three_points(p1, p2, p3)
        self.assertIsNotNone(plane.normal)

    def test_distance_to_point(self):
        plane = Plane(vec3(0, 1, 0), vec3(0, 0, 0))
        dist = plane.distance_to_point(vec3(0, 5, 0))
        self.assertAlmostEqual(dist, 5)

    def test_project_point(self):
        plane = Plane(vec3(0, 1, 0), vec3(0, 0, 0))
        projected = plane.project_point(vec3(5, 10, 5))
        self.assertAlmostEqual(projected.y, 0, places=5)


class TestProject3DTo2D(unittest.TestCase):
    def test_project_front(self):
        result = project_3d_to_2d(
            vec3(0, 0, 10),
            vec3(0, 0, 0),
            vec3(0, 0, 0),
            fov=60,
            width=800,
            height=600
        )
        self.assertIsNotNone(result)
        x, y = result
        self.assertEqual(x, 400)
        self.assertEqual(y, 300)

    def test_project_behind_camera(self):
        result = project_3d_to_2d(
            vec3(0, 0, -10),
            vec3(0, 0, 0),
            vec3(0, 0, 0),
            fov=60,
            width=800,
            height=600
        )
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
