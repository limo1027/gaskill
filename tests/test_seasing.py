import unittest

from gaskill.seasing import (
    linear,
    quad_in, quad_out, quad_in_out,
    cubic_in, cubic_out, cubic_in_out,
    sine_in, sine_out, sine_in_out,
    back_in, back_out,
    bounce_in, bounce_out, bounce_in_out,
    elastic_in, elastic_out,
)


class TestEasingFunctions(unittest.TestCase):
    def test_linear(self):
        self.assertAlmostEqual(linear(0), 0)
        self.assertAlmostEqual(linear(0.5), 0.5)
        self.assertAlmostEqual(linear(1), 1)

    def test_sine_in(self):
        self.assertAlmostEqual(sine_in(0), 0)
        self.assertAlmostEqual(sine_in(1), 1)

    def test_sine_out(self):
        self.assertAlmostEqual(sine_out(0), 0)
        self.assertAlmostEqual(sine_out(1), 1)

    def test_sine_in_out(self):
        self.assertAlmostEqual(sine_in_out(0), 0)
        self.assertAlmostEqual(sine_in_out(0.5), 0.5)
        self.assertAlmostEqual(sine_in_out(1), 1)

    def test_quad_in(self):
        self.assertAlmostEqual(quad_in(0), 0)
        self.assertAlmostEqual(quad_in(1), 1)
        self.assertAlmostEqual(quad_in(0.5), 0.25)

    def test_quad_out(self):
        self.assertAlmostEqual(quad_out(0), 0)
        self.assertAlmostEqual(quad_out(1), 1)

    def test_quad_in_out(self):
        self.assertAlmostEqual(quad_in_out(0), 0)
        self.assertAlmostEqual(quad_in_out(0.5), 0.5)
        self.assertAlmostEqual(quad_in_out(1), 1)

    def test_cubic_in(self):
        self.assertAlmostEqual(cubic_in(0), 0)
        self.assertAlmostEqual(cubic_in(1), 1)

    def test_cubic_out(self):
        self.assertAlmostEqual(cubic_out(0), 0)
        self.assertAlmostEqual(cubic_out(1), 1)

    def test_cubic_in_out(self):
        self.assertAlmostEqual(cubic_in_out(0), 0)
        self.assertAlmostEqual(cubic_in_out(0.5), 0.5)
        self.assertAlmostEqual(cubic_in_out(1), 1)

    def test_back_in(self):
        self.assertAlmostEqual(back_in(0), 0)
        self.assertAlmostEqual(back_in(1), 1)

    def test_back_out(self):
        self.assertAlmostEqual(back_out(0), 0)
        self.assertAlmostEqual(back_out(1), 1)

    def test_elastic_in(self):
        self.assertAlmostEqual(elastic_in(0), 0)
        self.assertAlmostEqual(elastic_in(1), 1)

    def test_elastic_out(self):
        self.assertAlmostEqual(elastic_out(0), 0)
        self.assertAlmostEqual(elastic_out(1), 1)

    def test_bounce_out(self):
        self.assertAlmostEqual(bounce_out(0), 0)
        self.assertAlmostEqual(bounce_out(1), 1)

    def test_bounce_in(self):
        self.assertAlmostEqual(bounce_in(0), 0)
        self.assertAlmostEqual(bounce_in(1), 1)

    def test_bounce_in_out(self):
        self.assertAlmostEqual(bounce_in_out(0), 0)
        self.assertAlmostEqual(bounce_in_out(1), 1)


if __name__ == '__main__':
    unittest.main()
