import unittest
from gaskill.scrypt import (
    simple_decrypt, share_secret, simple_encrypt,
    rsa_decrypt, rsa_encrypt, rsa_generate_keys, recover_secret
)


class TestRSA(unittest.TestCase):
    def test_rsa_basic(self):
        keys = rsa_generate_keys(bits=256)
        self.assertIn('e', keys)
        self.assertIn('d', keys)
        self.assertIn('n', keys)
        self.assertIn('p', keys)
        self.assertIn('q', keys)

    def test_rsa_encrypt_decrypt(self):
        keys = rsa_generate_keys(bits=256)
        original = "Hello, RSA!"
        cipher = rsa_encrypt(original, keys)
        decrypted = rsa_decrypt(cipher, keys)
        self.assertEqual(decrypted, original)

    def test_rsa_encrypt_decrypt_chinese(self):
        keys = rsa_generate_keys(bits=256)
        original = "你好，RSA加密！"
        cipher = rsa_encrypt(original, keys)
        decrypted = rsa_decrypt(cipher, keys)
        self.assertEqual(decrypted, original)

    def test_rsa_encrypt_decrypt_long_text(self):
        keys = rsa_generate_keys(bits=512)
        original = "A" * 50
        cipher = rsa_encrypt(original, keys)
        decrypted = rsa_decrypt(cipher, keys)
        self.assertEqual(decrypted, original)

    def test_rsa_deterministic(self):
        keys = rsa_generate_keys(bits=256)
        original = "test"
        cipher1 = rsa_encrypt(original, keys)
        cipher2 = rsa_encrypt(original, keys)
        self.assertEqual(cipher1, cipher2)


class TestSimpleEncrypt(unittest.TestCase):
    def test_simple_encrypt_decrypt(self):
        original = "Hello, World!"
        cipher, key, IV = simple_encrypt(original)
        decrypted = simple_decrypt(cipher, key, IV)
        self.assertEqual(decrypted, original)

    def test_simple_encrypt_decrypt_chinese(self):
        original = "你好，加密！"
        cipher, key, IV = simple_encrypt(original)
        decrypted = simple_decrypt(cipher, key, IV)
        self.assertEqual(decrypted, original)

    def test_simple_encrypt_with_custom_key(self):
        original = "Custom Key Test"
        custom_key = "my_secret_key"
        cipher, returned_IV = simple_encrypt(original, key=custom_key)
        decrypted = simple_decrypt(cipher, custom_key, returned_IV)
        self.assertEqual(decrypted, original)

    def test_simple_encrypt_with_second_key(self):
        original = "Second Key Test"
        second_key = [1001, 1002, 1003]
        cipher, key, IV = simple_encrypt(original, second=second_key)
        decrypted = simple_decrypt(cipher, key, IV, second=second_key)
        self.assertEqual(decrypted, original)

    def test_simple_encrypt_produces_different_output(self):
        original = "Hello"
        cipher1, key1, IV1 = simple_encrypt(original)
        cipher2, key2, IV2 = simple_encrypt(original)
        self.assertNotEqual(cipher1, cipher2)

    def test_simple_decrypt_wrong_key(self):
        original = "Secret Message"
        cipher, key, IV = simple_encrypt(original)
        with self.assertRaises((ValueError, ZeroDivisionError)):
            simple_decrypt(cipher, "wrong_key", IV)

    def test_simple_decrypt_wrong_IV(self):
        original = "Secret Message"
        cipher, key, IV = simple_encrypt(original)
        with self.assertRaises((ValueError, ZeroDivisionError)):
            simple_decrypt(cipher, key, "000000000000")


class TestShareSecret(unittest.TestCase):
    def test_share_recover_basic(self):
        original = "My Secret"
        keys = ["key1", "key2", "key3"]
        threshold = 2
        shares = share_secret(original, keys, threshold)
        self.assertEqual(len(shares), len(keys))

        recovered = recover_secret(shares, threshold)
        self.assertEqual(recovered, original)

    def test_share_recover_with_threshold_equals_keys(self):
        original = "Full Recovery Test"
        keys = ["a", "b", "c"]
        threshold = 3
        shares = share_secret(original, keys, threshold)
        recovered = recover_secret(shares, threshold)
        self.assertEqual(recovered, original)

    def test_share_recover_chinese(self):
        original = "秘密信息"
        keys = ["K1", "K2", "K3", "K4"]
        threshold = 3
        shares = share_secret(original, keys, threshold)
        subset = dict(list(shares.items())[:3])
        recovered = recover_secret(subset, threshold)
        self.assertEqual(recovered, original)

    def test_share_recover_long_text(self):
        original = "A" * 100
        keys = ["k1", "k2", "k3", "k4", "k5"]
        threshold = 3
        shares = share_secret(original, keys, threshold)
        recovered = recover_secret(shares, threshold)
        self.assertEqual(recovered, original)

    def test_share_recover_insufficient_keys(self):
        original = "Secret"
        keys = ["key1", "key2", "key3"]
        threshold = 3
        shares = share_secret(original, keys, threshold)
        subset = dict(list(shares.items())[:2])
        with self.assertRaises(ValueError):
            recover_secret(subset, threshold)

    def test_share_recover_different_combinations(self):
        original = "Test Combination"
        keys = ["k1", "k2", "k3", "k4"]
        threshold = 2
        shares = share_secret(original, keys, threshold)

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                subset = {keys[i]: shares[keys[i]], keys[j]: shares[keys[j]]}
                recovered = recover_secret(subset, threshold)
                self.assertEqual(recovered, original)


if __name__ == '__main__':
    unittest.main()
