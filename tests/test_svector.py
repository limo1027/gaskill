import unittest

from gaskill.svector import vec2, vec3, vec4, v2, v3, v4, dot, cross, distance, normalize


class TestVec2(unittest.TestCase):
    def test_init(self):
        v = vec2(3, 4)
        self.assertEqual(v.x, 3.0)
        self.assertEqual(v.y, 4.0)

    def test_add(self):
        v1 = vec2(1, 2)
        v2 = vec2(3, 4)
        result = v1 + v2
        self.assertEqual(result.x, 4.0)
        self.assertEqual(result.y, 6.0)

    def test_sub(self):
        v1 = vec2(3, 4)
        v2 = vec2(1, 2)
        result = v1 - v2
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, 2.0)

    def test_mul(self):
        v = vec2(2, 3)
        result = v * 2
        self.assertEqual(result.x, 4.0)
        self.assertEqual(result.y, 6.0)

    def test_truediv(self):
        v = vec2(4, 6)
        result = v / 2
        self.assertEqual(result.x, 2.0)
        self.assertEqual(result.y, 3.0)

    def test_neg(self):
        v = vec2(3, -4)
        result = -v
        self.assertEqual(result.x, -3.0)
        self.assertEqual(result.y, 4.0)

    def test_dot(self):
        v1 = vec2(1, 2)
        v2 = vec2(3, 4)
        self.assertEqual(v1.dot(v2), 11)

    def test_cross(self):
        v1 = vec2(1, 0)
        v2 = vec2(0, 1)
        self.assertEqual(v1.cross(v2), 1)

    def test_length(self):
        v = vec2(3, 4)
        self.assertAlmostEqual(v.length(), 5.0)

    def test_normalize(self):
        v = vec2(3, 4)
        normalized = v.normalize()
        self.assertAlmostEqual(normalized.length(), 1.0)

    def test_distance(self):
        v1 = vec2(0, 0)
        v2 = vec2(3, 4)
        self.assertAlmostEqual(v1.distance(v2), 5.0)

    def test_lerp(self):
        v1 = vec2(0, 0)
        v2 = vec2(10, 10)
        result = v1.lerp(v2, 0.5)
        self.assertEqual(result.x, 5.0)
        self.assertEqual(result.y, 5.0)

    def test_rotate(self):
        v = vec2(1, 0)
        result = v.rotate(3.141592653589793 / 2)
        self.assertAlmostEqual(result.x, 0, places=5)
        self.assertAlmostEqual(result.y, 1, places=5)

    def test_reflect(self):
        v = vec2(1, -1)
        normal = vec2(0, 1)
        result = v.reflect(normal)
        self.assertAlmostEqual(result.x, 1)
        self.assertAlmostEqual(result.y, 1)

    def test_zero_vector(self):
        v = vec2(0, 0)
        self.assertEqual(v.length(), 0)
        self.assertEqual(v.dot(vec2(1, 1)), 0)

    def test_unit_vector(self):
        v = vec2(1, 0)
        self.assertAlmostEqual(v.length(), 1)

    def test_normalize_zero_vector(self):
        v = vec2(0, 0)
        normalized = v.normalize()
        self.assertEqual(normalized.x, 0)
        self.assertEqual(normalized.y, 0)

    def test_rotate_180(self):
        v = vec2(1, 0)
        result = v.rotate(3.141592653589793)
        self.assertAlmostEqual(result.x, -1, places=5)
        self.assertAlmostEqual(result.y, 0, places=5)

    def test_negative_coordinates(self):
        v = vec2(-3, -4)
        self.assertAlmostEqual(v.length(), 5)
        normalized = v.normalize()
        self.assertAlmostEqual(normalized.length(), 1)


class TestVec3(unittest.TestCase):
    def test_init(self):
        v = vec3(1, 2, 3)
        self.assertEqual(v.x, 1.0)
        self.assertEqual(v.y, 2.0)
        self.assertEqual(v.z, 3.0)

    def test_add(self):
        v1 = vec3(1, 2, 3)
        v2 = vec3(4, 5, 6)
        result = v1 + v2
        self.assertEqual(result.x, 5.0)
        self.assertEqual(result.y, 7.0)
        self.assertEqual(result.z, 9.0)

    def test_dot(self):
        v1 = vec3(1, 0, 0)
        v2 = vec3(0, 1, 0)
        self.assertEqual(v1.dot(v2), 0)

    def test_cross(self):
        v1 = vec3(1, 0, 0)
        v2 = vec3(0, 1, 0)
        result = v1.cross(v2)
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, 1)

    def test_length(self):
        v = vec3(1, 2, 2)
        self.assertAlmostEqual(v.length(), 3.0)

    def test_rotate_x(self):
        v = vec3(0, 1, 0)
        result = v.rotate_x(3.141592653589793 / 2)
        self.assertAlmostEqual(result.y, 0, places=5)
        self.assertAlmostEqual(result.z, 1, places=5)

    def test_to_tuple(self):
        v = vec3(1, 2, 3)
        self.assertEqual(v.to_tuple(), (1.0, 2.0, 3.0))

    def test_zero_vector(self):
        v = vec3(0, 0, 0)
        self.assertEqual(v.length(), 0)

    def test_normalize_zero_vector(self):
        v = vec3(0, 0, 0)
        normalized = v.normalize()
        self.assertEqual(normalized.x, 0)

    def test_cross_orthogonal(self):
        v1 = vec3(1, 0, 0)
        v2 = vec3(0, 1, 0)
        result = v1.cross(v2)
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.z, 1)

    def test_cross_parallel(self):
        v1 = vec3(1, 0, 0)
        v2 = vec3(2, 0, 0)
        result = v1.cross(v2)
        self.assertEqual(result.length(), 0)

    def test_negative_coordinates(self):
        v = vec3(-1, -2, -3)
        self.assertAlmostEqual(v.length(), (1**2 + 2**2 + 3**2)**0.5)


class TestVec4(unittest.TestCase):
    def test_init(self):
        v = vec4(1, 2, 3, 4)
        self.assertEqual(v.w, 4.0)

    def test_to_vec3(self):
        v = vec4(2, 4, 6, 2)
        result = v.to_vec3()
        self.assertEqual(result.x, 1.0)
        self.assertEqual(result.y, 2.0)
        self.assertEqual(result.z, 3.0)

    def test_from_rgba(self):
        v = vec4.from_rgba(255, 128, 64, 255)
        self.assertAlmostEqual(v.x, 1.0)
        self.assertAlmostEqual(v.y, 128/255)


class TestShortcutFunctions(unittest.TestCase):
    def test_v2(self):
        v = v2(1, 2)
        self.assertIsInstance(v, vec2)

    def test_v3(self):
        v = v3(1, 2, 3)
        self.assertIsInstance(v, vec3)

    def test_v4(self):
        v = v4(1, 2, 3, 4)
        self.assertIsInstance(v, vec4)

    def test_dot_function(self):
        v1 = vec2(1, 2)
        v2 = vec2(3, 4)
        self.assertEqual(dot(v1, v2), 11)

    def test_cross_function(self):
        v1 = vec3(1, 0, 0)
        v2 = vec3(0, 1, 0)
        result = cross(v1, v2)
        self.assertEqual(result.z, 1)

    def test_distance_function(self):
        v1 = vec2(0, 0)
        v2 = vec2(3, 4)
        self.assertAlmostEqual(distance(v1, v2), 5.0)

    def test_normalize_function(self):
        v = vec2(3, 4)
        result = normalize(v)
        self.assertAlmostEqual(result.length(), 1.0)


if __name__ == '__main__':
    unittest.main()
