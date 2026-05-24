import unittest
import os
import tempfile
import shutil


from gaskill.ssaver import SGTsaver


class TestSGTsaver(unittest.TestCase):
    def setUp(self):
        self.saver = SGTsaver()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "test_save.txt")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_set_value(self):
        self.saver.set_value(score=100, name="hero")
        self.assertEqual(self.saver.get('score'), 100)
        self.assertEqual(self.saver.get('name'), 'hero')

    def test_add(self):
        self.saver.add('health', 50)
        self.assertEqual(self.saver['health'], 50)

    def test_save_and_load(self):
        self.saver.set_value(score=100, name="hero", level=5)
        self.saver.save(self.temp_file, use_hash=False)

        new_saver = SGTsaver()
        new_saver.load(self.temp_file, require_hash=False)

        self.assertEqual(new_saver.get('score'), 100)
        self.assertEqual(new_saver.get('name'), 'hero')
        self.assertEqual(new_saver.get('level'), 5)

    def test_save_with_hash(self):
        self.saver.set_value(score=100, name="hero")
        self.saver.save(self.temp_file, use_hash=True)

        new_saver = SGTsaver()
        new_saver.load(self.temp_file, require_hash=True)
        self.assertEqual(new_saver.get('score'), 100)

    def test_load_modified_file_raises(self):
        self.saver.set_value(score=100)
        self.saver.save(self.temp_file, use_hash=True)

        with open(self.temp_file, 'a') as f:
            f.write('\n#modified=true')

        new_saver = SGTsaver()
        with self.assertRaises(ValueError):
            new_saver.load(self.temp_file, require_hash=True)

    def test_save_types(self):
        self.saver.set_value(
            int_val=42,
            float_val=3.14,
            str_val="hello",
            bool_val=True,
            list_val=[1, 2, 3]
        )
        self.saver.save(self.temp_file, use_hash=False)

        new_saver = SGTsaver()
        new_saver.load(self.temp_file, require_hash=False)

        self.assertEqual(new_saver.get('int_val'), 42)
        self.assertAlmostEqual(new_saver.get('float_val'), 3.14)
        self.assertEqual(new_saver.get('str_val'), 'hello')
        self.assertEqual(new_saver.get('bool_val'), True)

    def test_vec2_support(self):
        from gaskill.svector import vec2
        self.saver.set_value(position=vec2(10, 20))
        self.saver.save(self.temp_file, use_hash=False)

        new_saver = SGTsaver()
        new_saver.load(self.temp_file, require_hash=False)

        pos = new_saver.get('position')
        self.assertAlmostEqual(pos[0], 10)
        self.assertAlmostEqual(pos[1], 20)


if __name__ == '__main__':
    unittest.main()
