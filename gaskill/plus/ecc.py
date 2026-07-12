# -*- coding: utf-8 -*-
"""
ECDSA 签名 - 用户自定义临时私钥 k
用户提供：私钥、消息、临时私钥 k
"""

from .sha256 import sha256
from ..gaskill.smath import egcd as mod_inv


def mod_inv(a, p):
    return pow(a, -1, p)


class Point:
    def __init__(self, x, y, a, b, p):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        self.p = p

    def __repr__(self):
        if self.is_infinity():
            return "O"
        if self.p > 2**100:
            return f"({hex(self.x)}, {hex(self.y)})"
        return f"({self.x}, {self.y})"

    def is_infinity(self):
        return self.x is None or self.y is None

    def is_on_curve(self):
        if self.is_infinity():
            return True
        left = (self.y * self.y) % self.p
        right = (self.x * self.x * self.x + self.a * self.x + self.b) % self.p
        return left == right

    def __add__(self, other):
        if self.is_infinity():
            return other
        if other.is_infinity():
            return self
        if self.x == other.x and (self.y + other.y) % self.p == 0:
            return Point(None, None, self.a, self.b, self.p)
        if self.x != other.x:
            lam = (other.y - self.y) * \
                mod_inv(other.x - self.x, self.p) % self.p
        else:
            lam = (3 * self.x * self.x + self.a) * \
                mod_inv(2 * self.y, self.p) % self.p
        x3 = (lam * lam - self.x - other.x) % self.p
        y3 = (lam * (self.x - x3) - self.y) % self.p
        return Point(x3, y3, self.a, self.b, self.p)

    def __mul__(self, k):
        result = Point(None, None, self.a, self.b, self.p)
        base = self
        while k > 0:
            if k & 1:
                result = result + base
            base = base + base
            k >>= 1
        return result


p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
a = 0
b = 7
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

G = Point(
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    a, b, p
)


def sha256_int(message):
    """计算消息的 SHA256 哈希，返回整数"""
    if isinstance(message, str):
        message = message.encode('utf-8')
    return int(sha256(message), 16)


def is_valid_private_key(k):
    """检查私钥是否合法：1 <= k < n"""
    return isinstance(k, int) and 1 <= k < n


def is_valid_k(k):
    """检查临时私钥是否合法：1 <= k < n"""
    return isinstance(k, int) and 1 <= k < n


# ============================================================
# 核心签名函数
# ============================================================

def ecdsa_sign_with_k(private_key, message, k):
    """
    ECDSA 签名 - 用户提供临时私钥 k

    参数：
        private_key: 用户私钥 (整数，1 ~ n-1)
        message:     待签名消息 (字符串)
        k:           临时私钥 (整数，1 ~ n-1)

    返回：
        (r, s): 签名对
    """
    # 1. 参数校验
    if not is_valid_private_key(private_key):
        raise ValueError(f"私钥必须在 1 到 n-1 之间，n={n}")
    if not is_valid_k(k):
        raise ValueError(f"临时私钥 k 必须在 1 到 n-1 之间，n={n}")

    # 2. 计算消息哈希
    z = sha256_int(message) % n
    print(f"  消息哈希 z = {hex(z)}")

    # 3. 计算 R = k * G
    R = G * k
    r = R.x % n
    if r == 0:
        raise ValueError(f"r = 0，请换一个 k 值")
    print(f"  R = k*G = ({R.x}, {R.y})")
    print(f"  r = {hex(r)}")

    # 4. 计算 s = (z + r * 私钥) / k  (mod n)
    k_inv = mod_inv(k, n)
    s = (z + r * private_key) * k_inv % n
    if s == 0:
        raise ValueError(f"s = 0，请换一个 k 值")
    print(f"  s = {hex(s)}")

    return (r, s)


def ecdsa_verify(public_key, message, signature):
    """
    ECDSA 验签

    参数：
        public_key: 公钥 (Point 对象)
        message:    消息
        signature:  (r, s)

    返回：
        True/False
    """
    r, s = signature
    if not (1 <= r < n and 1 <= s < n):
        print("❌ 签名无效：r 或 s 超出范围")
        return False

    z = sha256_int(message) % n

    s_inv = mod_inv(s, n)
    u1 = z * s_inv % n
    u2 = r * s_inv % n

    P = G * u1 + public_key * u2
    return P.x % n == r


# ============================================================
# 用户交互演示
# ============================================================

def main():
    print("=" * 60)
    print("🧾 ECDSA 签名工具 - 用户提供临时私钥 k")
    print("=" * 60)

    # ---- 用户输入私钥 ----
    print("\n1️⃣ 请输入你的私钥:")
    private_key_str = input("  私钥 (整数): ").strip()
    try:
        private_key = int(private_key_str)
        if not is_valid_private_key(private_key):
            print(f"❌ 私钥必须在 1 ~ {n-1} 之间")
            return
    except ValueError:
        print("❌ 请输入有效的整数")
        return

    # 计算公钥
    public_key = G * private_key
    print(f"  公钥: ({public_key.x}, {public_key.y})")

    # ---- 用户输入消息 ----
    print("\n2️⃣ 请输入要签名的消息:")
    message = input("  消息: ").strip()
    if not message:
        message = "Hello, ECDSA!"
        print(f"  使用默认消息: {message}")

    # ---- 用户输入临时私钥 k ----
    print("\n3️⃣ 请输入临时私钥 k (随机数):")
    k_str = input("  k (整数): ").strip()
    try:
        k = int(k_str)
        if not is_valid_k(k):
            print(f"❌ k 必须在 1 ~ {n-1} 之间")
            return
    except ValueError:
        print("❌ 请输入有效的整数")
        return

    # ---- 签名 ----
    print("\n4️⃣ 签名中...")
    try:
        signature = ecdsa_sign_with_k(private_key, message, k)
        r, s = signature
        print(f"\n✅ 签名成功!")
        print(f"  r = {hex(r)}")
        print(f"  s = {hex(s)}")
    except Exception as e:
        print(f"❌ 签名失败: {e}")
        return

    # ---- 验签 ----
    print("\n5️⃣ 验证签名...")
    valid = ecdsa_verify(public_key, message, signature)
    if valid:
        print("✅ 签名有效!")
    else:
        print("❌ 签名无效!")

    # ---- 附加演示：用同一个 k 签不同消息 ----
    print("\n" + "=" * 60)
    print("🧪 附加实验：用同一个 k 签不同消息")
    print("=" * 60)

    message2 = input("\n输入另一条消息 (直接回车跳过): ").strip()
    if message2:
        sig2 = ecdsa_sign_with_k(private_key, message2, k)
        valid2 = ecdsa_verify(public_key, message2, sig2)
        print(f"  第二条消息签名有效? {valid2}")

        print("\n⚠️ 注意: 如果两条消息的 r 相同，说明用了同一个 k")
        print(f"  签名1 r = {hex(signature[0])}")
        print(f"  签名2 r = {hex(sig2[0])}")
        if signature[0] == sig2[0]:
            print("  ❗ r 相同！这意味着 k 被重复使用了，存在私钥泄露风险！")
        else:
            print("  ✅ r 不同，安全")

    print("\n🏁 程序结束")


if __name__ == "__main__":
    main()
