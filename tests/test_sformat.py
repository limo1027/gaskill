import unittest


from gaskill.sformat import (
    to_UUID, superscript, visual_len, center, table,
    ordinal, to_poly, number_to_english, english_to_number,
    insert, encode, decode, time_format, file_size
)


class TestUUID(unittest.TestCase):
    def test_to_UUID(self):
        uuid1 = to_UUID("test")
        uuid2 = to_UUID("test")
        self.assertEqual(uuid1, uuid2)

    def test_to_UUID_different(self):
        uuid1 = to_UUID("test1")
        uuid2 = to_UUID("test2")
        self.assertNotEqual(uuid1, uuid2)


class TestSuperscript(unittest.TestCase):
    def test_superscript_digits(self):
        self.assertEqual(superscript(0), '\u2070')
        self.assertEqual(superscript(1), '\u00b9')
        self.assertEqual(superscript(2), '\u00b2')
        self.assertEqual(superscript(3), '\u00b3')


class TestVisualLength(unittest.TestCase):
    def test_visual_len_english(self):
        self.assertEqual(visual_len("hello"), 5)

    def test_visual_len_chinese(self):
        self.assertEqual(visual_len("你好"), 4)

    def test_visual_len_mixed(self):
        self.assertEqual(visual_len("hi你好"), 6)


class TestCenter(unittest.TestCase):
    def test_center(self):
        result = center("hi", 10)
        self.assertTrue(result.startswith(' '))
        self.assertTrue(result.endswith(' '))
        self.assertIn('hi', result)

    def test_center_exact(self):
        result = center("ab", 10)
        self.assertEqual(len(result), 10)


class TestTable(unittest.TestCase):
    def test_table_basic(self):
        data = [['Name', 'Age'], ['Alice', '25'], ['Bob', '30']]
        result = table(data)
        self.assertIsInstance(result, str)
        self.assertIn('Name', result)

    def test_table_empty(self):
        result = table([])
        self.assertEqual(result, "")


class TestOrdinal(unittest.TestCase):
    def test_ordinal_first(self):
        self.assertEqual(ordinal(1), "1st")
        self.assertEqual(ordinal(2), "2nd")
        self.assertEqual(ordinal(3), "3rd")

    def test_ordinal_teens(self):
        self.assertEqual(ordinal(11), "11th")
        self.assertEqual(ordinal(13), "13th")

    def test_ordinal_regular(self):
        self.assertEqual(ordinal(4), "4th")
        self.assertEqual(ordinal(21), "21st")
        self.assertEqual(ordinal(22), "22nd")


class TestToPoly(unittest.TestCase):
    def test_to_poly_simple(self):
        self.assertEqual(to_poly("2x+3"), "2*x+3")
        self.assertEqual(to_poly("x+1"), "x+1")

    def test_to_poly_power(self):
        result = to_poly("x^2+2x+1")
        self.assertIn("x**2", result)
        self.assertIn("2*x", result)


class TestNumberEnglish(unittest.TestCase):
    def test_number_to_english(self):
        self.assertEqual(number_to_english(0), "zero")
        self.assertEqual(number_to_english(1), "one")
        self.assertEqual(number_to_english(100), "one hundred")

    def test_english_to_number(self):
        self.assertEqual(english_to_number("one"), 1)
        self.assertEqual(english_to_number("one hundred"), 100)

    def test_roundtrip(self):
        for n in [0, 1, 42, 100, 1234]:
            word = number_to_english(n)
            back = english_to_number(word)
            self.assertEqual(back, n)


class TestStringManipulation(unittest.TestCase):
    def test_insert(self):
        result = insert("hello", 2, "XX")
        self.assertEqual(result, "heXXllo")

    def test_encode_decode(self):
        original = "Hello, 世界!"
        encoded = encode(original)
        decoded = decode(encoded)
        self.assertEqual(decoded, original)


class TestTimeFormat(unittest.TestCase):
    def test_time_format_seconds(self):
        self.assertEqual(time_format(45), "45s")

    def test_time_format_minutes(self):
        self.assertEqual(time_format(90), "1m 30s")

    def test_time_format_hours(self):
        self.assertEqual(time_format(3661), "1h 1m 1s")

    def test_time_format_full(self):
        result = time_format(3661, mode='full')
        self.assertIn(':', result)

    def test_time_format_words(self):
        result = time_format(90, mode='words')
        self.assertIn('minute', result)


class TestFileSize(unittest.TestCase):
    def test_file_size_bytes(self):
        self.assertEqual(file_size(500), "500 B")

    def test_file_size_kilobytes(self):
        result = file_size(1024)
        self.assertTrue(result == "1 KB" or "KB" in str(result))

    def test_file_size_megabytes(self):
        result = file_size(1048576)
        self.assertTrue(result == "1 MB" or "MB" in str(result))

    def test_file_size_mode_si(self):
        result = file_size(1000, mode='si')
        self.assertTrue(result == "1 KB" or "KB" in str(result))

    def test_file_size_mode_binary(self):
        result = file_size(1024, mode='binary')
        self.assertTrue(result == "1 KiB" or "KB" in str(result))


if __name__ == '__main__':
    unittest.main()
