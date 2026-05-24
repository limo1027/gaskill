import unittest

from gaskill.scache import LRUCache, TTLCache, RingBuffer, CacheStats, memoize


class TestLRUCache(unittest.TestCase):
    def test_init(self):
        cache = LRUCache(max_size=3)
        self.assertEqual(cache.size, 0)
        self.assertEqual(cache.max_size, 3)

    def test_set_get(self):
        cache = LRUCache(max_size=3)
        cache.set('key1', 'value1')
        self.assertEqual(cache.get('key1'), 'value1')

    def test_eviction(self):
        cache = LRUCache(max_size=2)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.set('c', 3)  # 应该驱逐 'a'
        self.assertIsNone(cache.get('a'))
        self.assertEqual(cache.get('b'), 2)
        self.assertEqual(cache.get('c'), 3)

    def test_contains(self):
        cache = LRUCache(max_size=3)
        cache.set('key', 'value')
        self.assertTrue('key' in cache)
        self.assertFalse('nonexistent' in cache)

    def test_pop(self):
        cache = LRUCache(max_size=3)
        cache.set('key', 'value')
        result = cache.pop('key')
        self.assertEqual(result, 'value')
        self.assertEqual(cache.size, 0)

    def test_clear(self):
        cache = LRUCache(max_size=3)
        cache.set('a', 1)
        cache.set('b', 2)
        cache.clear()
        self.assertEqual(cache.size, 0)


class TestTTLCache(unittest.TestCase):
    def test_init(self):
        cache = TTLCache(max_size=3)
        self.assertEqual(cache.size, 0)

    def test_set_get(self):
        cache = TTLCache(max_size=3)
        cache.set('key', 'value', current_time=0)
        self.assertEqual(cache.get('key', current_time=0), 'value')

    def test_expiration(self):
        cache = TTLCache(max_size=3)
        cache.set('key', 'value', ttl=5, current_time=0)
        self.assertIsNone(cache.get('key', current_time=10))

    def test_remove_expired(self):
        cache = TTLCache(max_size=3)
        cache.set('a', 1, ttl=5, current_time=0)
        cache.set('b', 2, ttl=10, current_time=0)
        count = cache.remove_expired(6)
        self.assertEqual(count, 1)


class TestRingBuffer(unittest.TestCase):
    def test_init(self):
        buffer = RingBuffer(3)
        self.assertEqual(buffer.capacity, 3)
        self.assertEqual(len(buffer), 0)

    def test_push_pop(self):
        buffer = RingBuffer(3)
        buffer.push(1)
        buffer.push(2)
        self.assertEqual(len(buffer), 2)
        self.assertEqual(buffer.pop(), 1)
        self.assertEqual(len(buffer), 1)

    def test_overwrite(self):
        buffer = RingBuffer(2)
        buffer.push(1)
        buffer.push(2)
        buffer.push(3)  # 覆盖
        self.assertEqual(buffer.pop(), 2)
        self.assertEqual(buffer.pop(), 3)

    def test_is_full(self):
        buffer = RingBuffer(2)
        buffer.push(1)
        buffer.push(2)
        self.assertTrue(buffer.is_full())

    def test_peek(self):
        buffer = RingBuffer(3)
        buffer.push(42)
        self.assertEqual(buffer.peek(), 42)


class TestCacheStats(unittest.TestCase):
    def test_init(self):
        stats = CacheStats()
        self.assertEqual(stats.hits, 0)
        self.assertEqual(stats.misses, 0)
        self.assertEqual(stats.hit_rate, 0.0)

    def test_record_hit(self):
        stats = CacheStats()
        stats.record_hit()
        stats.record_hit()
        self.assertEqual(stats.hits, 2)

    def test_record_miss(self):
        stats = CacheStats()
        stats.record_miss()
        self.assertEqual(stats.misses, 1)

    def test_hit_rate(self):
        stats = CacheStats()
        stats.record_hit()
        stats.record_hit()
        stats.record_miss()
        self.assertAlmostEqual(stats.hit_rate, 2/3)


class TestMemoize(unittest.TestCase):
    def test_memoize_function(self):
        call_count = [0]

        @memoize(max_size=10)
        def expensive_func(x):
            call_count[0] += 1
            return x * 2

        self.assertEqual(expensive_func(5), 10)
        self.assertEqual(call_count[0], 1)
        self.assertEqual(expensive_func(5), 10)  # 应该使用缓存
        self.assertEqual(call_count[0], 1)  # 未增加调用


if __name__ == '__main__':
    unittest.main()
