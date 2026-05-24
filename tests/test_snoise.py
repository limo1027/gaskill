import unittest

from gaskill.snoise import PerlinNoise, SimplexNoise, Snoise


class TestPerlinNoise(unittest.TestCase):
    def test_init(self):
        noise = PerlinNoise(seed=42)
        self.assertEqual(noise.octaves, 4)
        self.assertEqual(noise.persistence, 0.5)

    def test_noise2d_range(self):
        noise = PerlinNoise(seed=42)
        for i in range(10):
            for j in range(10):
                value = noise.noise2d(i * 0.1, j * 0.1)
                self.assertGreaterEqual(value, -1)
                self.assertLessEqual(value, 1)

    def test_fbm2d_range(self):
        noise = PerlinNoise(seed=42)
        value = noise.fbm2d(0.5, 0.5)
        self.assertGreaterEqual(value, -1)
        self.assertLessEqual(value, 1)

    def test_seed_consistency(self):
        noise1 = PerlinNoise(seed=42)
        noise2 = PerlinNoise(seed=42)
        value1 = noise1.noise2d(0.5, 0.5)
        value2 = noise2.noise2d(0.5, 0.5)
        self.assertAlmostEqual(value1, value2)


class TestSimplexNoise(unittest.TestCase):
    def test_init(self):
        noise = SimplexNoise(seed=123)
        self.assertIsInstance(noise, SimplexNoise)

    def test_noise2d_exists(self):
        noise = SimplexNoise(seed=123)
        value = noise.noise2d(0.5, 0.5)
        self.assertIsInstance(value, float)

    def test_fbm2d_exists(self):
        noise = SimplexNoise(seed=123, octaves=3)
        value = noise.fbm2d(0.5, 0.5)
        self.assertIsInstance(value, float)


class TestSnoise(unittest.TestCase):
    def test_init(self):
        noise = Snoise()
        self.assertEqual(len(noise.points), 0)

    def test_add_point(self):
        noise = Snoise()
        noise.add_point(0, 0, 1.0)
        self.assertEqual(len(noise.points), 1)

    def test_add_points(self):
        noise = Snoise()
        noise.add_points((0, 0, 1), (1, 1, 2))
        self.assertEqual(len(noise.points), 2)

    def test_call(self):
        noise = Snoise()
        noise.add_point(0, 0, 1.0)
        value = noise(0, 0)
        self.assertEqual(value, 1.0)

    def test_sample_rect(self):
        noise = Snoise()
        noise.add_point(0, 0, 1.0)
        samples = noise.sample_rect(-1, -1, 1, 1, step=1.0)
        self.assertEqual(len(samples), 3)
        self.assertEqual(len(samples[0]), 3)


if __name__ == '__main__':
    unittest.main()
