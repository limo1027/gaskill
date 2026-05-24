import unittest

from gaskill.smatrix import (
    Matrix, matrix,
    rotation_matrix_2d, rotation_matrix_x,
    scaling_matrix_2d, translation_matrix_2d,
    solve_linear, eigenvalues_2x2,
    kronecker, outer_product
)


class TestMatrixBasics(unittest.TestCase):
    def test_init(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.rows, 2)
        self.assertEqual(m.cols, 2)
        self.assertEqual(m[0, 0], 1)
        self.assertEqual(m[1, 1], 4)

    def test_add(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[5, 6], [7, 8]])
        result = m1 + m2
        self.assertEqual(result[0, 0], 6)
        self.assertEqual(result[1, 1], 12)

    def test_sub(self):
        m1 = Matrix([[5, 6], [7, 8]])
        m2 = Matrix([[1, 2], [3, 4]])
        result = m1 - m2
        self.assertEqual(result[0, 0], 4)
        self.assertEqual(result[1, 1], 4)

    def test_mul_scalar(self):
        m = Matrix([[1, 2], [3, 4]])
        result = m * 2
        self.assertEqual(result[0, 0], 2)
        self.assertEqual(result[1, 1], 8)

    def test_mul_matrix(self):
        m1 = Matrix([[1, 2], [3, 4]])
        m2 = Matrix([[5, 6], [7, 8]])
        result = m1 * m2
        self.assertEqual(result[0, 0], 19)
        self.assertEqual(result[1, 0], 43)

    def test_transpose(self):
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        result = m.transpose()
        self.assertEqual(result.rows, 3)
        self.assertEqual(result.cols, 2)
        self.assertEqual(result[0, 1], 4)

    def test_trace(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.trace(), 5)

    def test_det(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.det(), -2)

    def test_inverse(self):
        m = Matrix([[4, 7], [2, 6]])
        inv = m.inverse()
        result = m * inv
        self.assertAlmostEqual(result[0, 0], 1)
        self.assertAlmostEqual(result[0, 1], 0)
        self.assertAlmostEqual(result[1, 0], 0)
        self.assertAlmostEqual(result[1, 1], 1)

    def test_inverse_singular(self):
        m = Matrix([[1, 2], [2, 4]])
        with self.assertRaises(ValueError):
            m.inverse()

    def test_det_singular(self):
        m = Matrix([[1, 2], [2, 4]])
        self.assertEqual(m.det(), 0)

    def test_large_matrix(self):
        size = 10
        data = [[i + j for j in range(size)] for i in range(size)]
        m = Matrix(data)
        self.assertEqual(m.rows, size)
        self.assertEqual(m.cols, size)

    def test_multiply_incompatible(self):
        m1 = Matrix([[1, 2, 3]])
        m2 = Matrix([[1], [2]])
        with self.assertRaises(ValueError):
            m1 * m2


class TestMatrixSpecialFunctions(unittest.TestCase):
    def test_rank(self):
        m = Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9]])
        self.assertEqual(m.rank(), 1)

    def test_is_symmetric(self):
        m = Matrix([[1, 2, 3], [2, 4, 5], [3, 5, 6]])
        self.assertTrue(m.is_symmetric())

    def test_is_identity(self):
        m = Matrix([[1, 0], [0, 1]])
        self.assertTrue(m.is_identity())

    def test_diagonal(self):
        m = Matrix([[1, 2], [3, 4]])
        self.assertEqual(m.diagonal(), [1, 4])


class TestMatrixFactories(unittest.TestCase):
    def test_rotation_matrix_2d(self):
        m = rotation_matrix_2d(0)
        self.assertAlmostEqual(m[0, 0], 1)
        self.assertAlmostEqual(m[0, 1], 0)

    def test_scaling_matrix_2d(self):
        m = scaling_matrix_2d(2, 3)
        self.assertEqual(m[0, 0], 2)
        self.assertEqual(m[1, 1], 3)

    def test_translation_matrix_2d(self):
        m = translation_matrix_2d(5, 10)
        self.assertEqual(m[0, 2], 5)
        self.assertEqual(m[1, 2], 10)


class TestMatrixOperations(unittest.TestCase):
    def test_solve_linear(self):
        A = Matrix([[1, 2], [3, 4]])
        b = [5, 11]
        x = solve_linear(A, b)
        self.assertAlmostEqual(x[0], 1)
        self.assertAlmostEqual(x[1], 2)

    def test_eigenvalues_2x2(self):
        m = Matrix([[1, 2], [3, 4]])
        ev = eigenvalues_2x2(m)
        self.assertAlmostEqual(sum(ev), 5)  # trace

    def test_outer_product(self):
        v1 = [1, 2]
        v2 = [3, 4, 5]
        result = outer_product(v1, v2)
        self.assertEqual(result.rows, 2)
        self.assertEqual(result.cols, 3)
        self.assertEqual(result[0, 0], 3)


if __name__ == '__main__':
    unittest.main()
