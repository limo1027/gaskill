import unittest

from gaskill.squaternion import (
    Quaternion, slerp, nlerp, squad, angular_velocity,
    integrate_angular_velocity, look_at, random_quaternion,
    IDENTITY, ZERO
)
from gaskill.svector import vec3


class TestQuaternion(unittest.TestCase):
    def test_init(self):
        q = Quaternion(1, 0, 0, 0)
        self.assertEqual(q.w, 1)
        self.assertEqual(q.x, 0)

    def test_equality(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(1, 0, 0, 0)
        self.assertEqual(q1, q2)

    def test_addition(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(0, 1, 0, 0)
        result = q1 + q2
        self.assertEqual(result.w, 1)
        self.assertEqual(result.x, 1)

    def test_multiplication(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(0, 1, 0, 0)
        result = q1 * q2
        self.assertIsInstance(result, Quaternion)

    def test_conjugate(self):
        q = Quaternion(1, 2, 3, 4)
        conj = q.conjugate()
        self.assertEqual(conj.w, 1)
        self.assertEqual(conj.x, -2)

    def test_norm(self):
        q = Quaternion(3, 0, 0, 0)
        self.assertAlmostEqual(q.norm(), 3)

    def test_normalize(self):
        q = Quaternion(2, 0, 0, 0)
        normalized = q.normalize()
        self.assertAlmostEqual(normalized.norm(), 1)

    def test_inverse(self):
        q = Quaternion(1, 2, 3, 4)
        inv = q.inverse()
        result = q * inv
        self.assertAlmostEqual(result.w, 1, places=5)

    def test_dot(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(1, 0, 0, 0)
        self.assertAlmostEqual(q1.dot(q2), 1)


class TestQuaternionRotation(unittest.TestCase):
    def test_to_axis_angle(self):
        q = Quaternion.from_axis_angle(vec3(0, 0, 1), 3.14159)
        axis, angle = q.to_axis_angle()
        self.assertAlmostEqual(angle, 3.14159, places=2)

    def test_from_axis_angle(self):
        q = Quaternion.from_axis_angle(vec3(0, 0, 1), 3.14159)
        self.assertIsInstance(q, Quaternion)

    def test_from_euler(self):
        q = Quaternion.from_euler(0, 0, 0)
        self.assertIsInstance(q, Quaternion)

    def test_to_matrix(self):
        q = Quaternion(1, 0, 0, 0)
        matrix = q.to_matrix()
        self.assertEqual(matrix.rows, 3)
        self.assertEqual(matrix.cols, 3)

    def test_rotate_vector(self):
        q = Quaternion.from_axis_angle(vec3(0, 0, 1), 3.14159 / 2)
        v = vec3(1, 0, 0)
        rotated = q.rotate_vector(v)
        self.assertAlmostEqual(rotated.x, 0, places=2)
        self.assertGreater(rotated.y, 0)

    def test_from_two_vectors(self):
        v1 = vec3(1, 0, 0)
        v2 = vec3(0, 1, 0)
        q = Quaternion.from_two_vectors(v1, v2)
        self.assertIsInstance(q, Quaternion)


class TestSlerp(unittest.TestCase):
    def test_slerp_identity(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(1, 0, 0, 0)
        result = slerp(q1, q2, 0.5)
        self.assertAlmostEqual(result.w, 1, places=5)

    def test_slerp_90_degrees(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(0.7071, 0.7071, 0, 0)
        result = slerp(q1, q2, 0.5)
        self.assertAlmostEqual(result.norm(), 1, places=5)


class TestNlerp(unittest.TestCase):
    def test_nlerp(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(0, 1, 0, 0)
        result = nlerp(q1, q2, 0.5)
        self.assertAlmostEqual(result.norm(), 1, places=5)


class TestSquad(unittest.TestCase):
    def test_squad(self):
        q0 = Quaternion(1, 0, 0, 0)
        q1 = Quaternion(0.7071, 0.7071, 0, 0)
        q2 = Quaternion(0.7071, 0, 0.7071, 0)
        q3 = Quaternion(0.7071, 0, 0, 0.7071)
        result = squad(q0, q1, q2, q3, 0.5)
        self.assertIsInstance(result, Quaternion)


class TestAngularVelocity(unittest.TestCase):
    def test_angular_velocity(self):
        q1 = Quaternion(1, 0, 0, 0)
        q2 = Quaternion(0.7071, 0.7071, 0, 0)
        velocity = angular_velocity(q1, q2, 0.1)
        self.assertIsInstance(velocity, vec3)


class TestIntegrateAngularVelocity(unittest.TestCase):
    def test_integrate_angular_velocity(self):
        q = Quaternion(1, 0, 0, 0)
        omega = vec3(0, 0, 10)
        result = integrate_angular_velocity(q, omega, 0.1)
        self.assertIsInstance(result, Quaternion)


class TestLookAt(unittest.TestCase):
    def test_look_at(self):
        eye = vec3(0, 0, 0)
        target = vec3(1, 0, 0)
        q = look_at(eye, target)
        self.assertIsInstance(q, Quaternion)


class TestConstants(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(IDENTITY.w, 1)
        self.assertEqual(IDENTITY.x, 0)

    def test_zero(self):
        self.assertEqual(ZERO.w, 0)
        self.assertEqual(ZERO.x, 0)


if __name__ == '__main__':
    unittest.main()
