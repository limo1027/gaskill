import unittest

from gaskill.spool import ObjectPool, PooledObject, AutoReleasePool, StackAllocator


class TestObjectPool(unittest.TestCase):
    def test_init(self):
        pool = ObjectPool()
        self.assertEqual(pool.available_count, 0)
        self.assertEqual(pool.in_use_count, 0)

    def test_acquire_with_factory(self):
        pool = ObjectPool(factory=lambda: {"value": 0}, max_size=5)
        obj = pool.acquire()
        self.assertEqual(pool.in_use_count, 1)
        self.assertEqual(pool.available_count, 0)

    def test_release(self):
        pool = ObjectPool(factory=lambda: {"value": 0}, max_size=5)
        obj = pool.acquire()
        pool.release(obj)
        self.assertEqual(pool.in_use_count, 0)
        self.assertEqual(pool.available_count, 1)

    def test_max_size(self):
        pool = ObjectPool(factory=lambda: {"value": 0}, max_size=2)
        pool.acquire()
        pool.acquire()
        with self.assertRaises(RuntimeError):
            pool.acquire()

    def test_reset_func(self):
        def factory():
            return {"value": 1}

        def reset(obj):
            obj["value"] = 0

        pool = ObjectPool(factory=factory, reset_func=reset, max_size=2)
        obj = pool.acquire()
        obj["value"] = 5
        pool.release(obj)
        obj2 = pool.acquire()
        self.assertEqual(obj2["value"], 0)


class TestPooledObject(unittest.TestCase):
    def test_init(self):
        obj = PooledObject()
        self.assertTrue(obj.is_active)

    def test_recycle(self):
        pool = ObjectPool()
        obj = PooledObject()
        obj._pool = pool
        obj.recycle()
        self.assertFalse(obj.is_active)


class TestAutoReleasePool(unittest.TestCase):
    def test_with_statement(self):
        released = []

        class MockObj:
            def recycle(self):
                released.append(True)

        with AutoReleasePool() as pool:
            obj = MockObj()
            pool.add(obj)

        self.assertEqual(len(released), 1)

    def test_release_all(self):
        released = []

        class MockObj:
            def recycle(self):
                released.append(True)

        pool = AutoReleasePool()
        pool.add(MockObj())
        pool.add(MockObj())
        pool.release_all()

        self.assertEqual(len(released), 2)


class TestStackAllocator(unittest.TestCase):
    def test_init(self):
        stack = StackAllocator(10)
        self.assertEqual(stack.size, 0)
        self.assertEqual(stack.capacity, 10)

    def test_push_pop(self):
        stack = StackAllocator(10)
        stack.push(1)
        stack.push(2)
        self.assertEqual(stack.size, 2)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.size, 1)

    def test_grow(self):
        stack = StackAllocator(2)
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.capacity, 4)
        self.assertEqual(stack.size, 3)

    def test_empty_pop(self):
        stack = StackAllocator(10)
        with self.assertRaises(IndexError):
            stack.pop()


if __name__ == '__main__':
    unittest.main()
