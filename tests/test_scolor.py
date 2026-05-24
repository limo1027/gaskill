import unittest

from gaskill.scolor import (
    rgb, rgba, hex_to_rgb, rgb_to_hex, complementary, color_lerp,
    rgb_to_hsv, hsv_to_rgb, blend, gradient_at,
    grayscale, invert, adjust_brightness,
    luminance, contrast_ratio,
    is_dark, is_light, rgb_to_cymb, cymb_to_rgb,
    WHITE, BLACK, RED, GREEN, BLUE, SUCCESS, WARNING, ERROR, INFO, TRANSPARENT
)


class TestColorConversion(unittest.TestCase):
    def test_rgb(self):
        r, g, b = rgb(255, 128, 64)
        self.assertEqual((r, g, b), (255, 128, 64))

    def test_rgba(self):
        r, g, b, a = rgba(255, 128, 64, 128)
        self.assertEqual((r, g, b, a), (255, 128, 64, 128))

    def test_hex_to_rgb(self):
        r, g, b = hex_to_rgb('#FF8040')
        self.assertEqual((r, g, b), (255, 128, 64))

    def test_rgb_to_hex(self):
        hex_str = rgb_to_hex(255, 128, 64)
        self.assertEqual(hex_str, '#ff8040')


class TestColorManipulation(unittest.TestCase):
    def test_complementary(self):
        c = complementary((255, 0, 0))
        self.assertEqual(c, (0, 255, 255))

    def test_color_lerp(self):
        c1 = (0, 0, 0)
        c2 = (255, 255, 255)
        result = color_lerp(c1, c2, 0.5)
        self.assertEqual(result, (127, 127, 127))

    def test_grayscale(self):
        gray = grayscale((100, 100, 100))
        self.assertEqual(gray, (100, 100, 100))

    def test_invert(self):
        inv = invert((255, 128, 64))
        self.assertEqual(inv, (0, 127, 191))

    def test_adjust_brightness(self):
        bright = adjust_brightness((100, 100, 100), 2.0)
        self.assertEqual(bright, (200, 200, 200))


class TestColorModels(unittest.TestCase):
    def test_rgb_to_hsv(self):
        h, s, v = rgb_to_hsv(255, 0, 0)
        self.assertAlmostEqual(h, 0)
        self.assertAlmostEqual(s, 1)
        self.assertAlmostEqual(v, 1)

    def test_hsv_to_rgb(self):
        r, g, b = hsv_to_rgb(0, 1, 1)
        self.assertEqual((r, g, b), (255, 0, 0))

    def test_rgb_to_hsv_to_rgb(self):
        original = (255, 128, 64)
        h, s, v = rgb_to_hsv(*original)
        back = hsv_to_rgb(h, s, v)
        self.assertEqual(back, original)

    def test_rgb_to_cymb(self):
        c, y, m, k = rgb_to_cymb(255, 0, 0)
        self.assertAlmostEqual(c, 0)
        self.assertAlmostEqual(k, 0)

    def test_cymb_to_rgb(self):
        r, g, b = cymb_to_rgb(0, 1, 1, 0)
        self.assertEqual((r, g, b), (255, 0, 0))


class TestColorBlending(unittest.TestCase):
    def test_blend_normal(self):
        c1 = (100, 100, 100)
        c2 = (200, 200, 200)
        result = blend(c1, c2, 'normal', 0.5)
        self.assertEqual(result, (150, 150, 150))

    def test_blend_multiply(self):
        c1 = (128, 128, 128)
        c2 = (128, 128, 128)
        result = blend(c1, c2, 'multiply')
        self.assertEqual(result, (64, 64, 64))

    def test_blend_screen(self):
        c1 = (0, 0, 0)
        c2 = (255, 255, 255)
        result = blend(c1, c2, 'screen')
        self.assertEqual(result, (255, 255, 255))


class TestGradient(unittest.TestCase):
    def test_gradient_at(self):
        colors = {(255, 0, 0): 0, (0, 255, 0): 1}
        result = gradient_at(colors, 0.5)
        self.assertEqual(result, (127, 127, 0))

    def test_gradient_at_boundary(self):
        colors = {(255, 0, 0): 0, (0, 255, 0): 1}
        self.assertEqual(gradient_at(colors, 0), (255, 0, 0))
        self.assertEqual(gradient_at(colors, 1), (0, 255, 0))


class TestColorAnalysis(unittest.TestCase):
    def test_luminance_white(self):
        lum = luminance(WHITE)
        self.assertAlmostEqual(lum, 1.0)

    def test_luminance_black(self):
        lum = luminance(BLACK)
        self.assertLess(lum, 0.01)

    def test_contrast_ratio(self):
        ratio = contrast_ratio(WHITE, BLACK)
        self.assertGreater(ratio, 18)  # WCAG 要求至少 18

    def test_is_dark(self):
        self.assertTrue(is_dark(BLACK))
        self.assertFalse(is_dark(WHITE))

    def test_is_light(self):
        self.assertTrue(is_light(WHITE))
        self.assertFalse(is_light(BLACK))


class TestColorConstants(unittest.TestCase):
    def test_basic_colors(self):
        self.assertEqual(RED, (255, 0, 0))
        self.assertEqual(GREEN, (0, 255, 0))
        self.assertEqual(BLUE, (0, 0, 255))

    def test_transparent(self):
        self.assertEqual(TRANSPARENT, (0, 0, 0, 0))

    def test_status_colors(self):
        self.assertEqual(SUCCESS, (100, 255, 100))
        self.assertEqual(WARNING, (255, 255, 100))
        self.assertEqual(ERROR, (255, 100, 100))
        self.assertEqual(INFO, (173, 216, 230))


if __name__ == '__main__':
    unittest.main()
