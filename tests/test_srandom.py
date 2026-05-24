import unittest

from gaskill.srandom import Random


class TestRandom(unittest.TestCase):
    def test_init(self):
        rng = Random(42)
        self.assertIsNotNone(rng)

    def test_seed_consistency(self):
        rng1 = Random(42)
        rng2 = Random(42)
        values1 = [rng1.random() for _ in range(10)]
        values2 = [rng2.random() for _ in range(10)]
        self.assertEqual(values1, values2)

    def test_random_range(self):
        rng = Random(42)
        for _ in range(100):
            value = rng.random()
            self.assertGreaterEqual(value, 0)
            self.assertLess(value, 1)

    def test_randint(self):
        rng = Random(42)
        for _ in range(100):
            value = rng.randint(0, 10)
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 10)

    def test_random_float(self):
        rng = Random(42)
        for _ in range(100):
            value = rng.random_float(1.0, 5.0)
            self.assertGreaterEqual(value, 1.0)
            self.assertLess(value, 5.0)

    def test_choice(self):
        rng = Random(42)
        items = [1, 2, 3, 4, 5]
        for _ in range(100):
            choice = rng.choice(items)
            self.assertIn(choice, items)

    def test_shuffle(self):
        rng = Random(42)
        items = [1, 2, 3, 4, 5]
        original = list(items)
        rng.shuffle(items)
        self.assertEqual(set(items), set(original))

    def test_sample(self):
        rng = Random(42)
        items = list(range(10))
        sample = rng.sample(items, 3)
        self.assertEqual(len(sample), 3)
        self.assertEqual(len(set(sample)), 3)


if __name__ == '__main__':
    unittest.main()
