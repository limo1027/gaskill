# -*- coding: utf-8 -*-
from gaskill import Frac


class Radical:
    """
    表示 coeff * (radicand)^(1/index)
    radicand 可以是：
      - int / float               （数字）
      - Radical                    （嵌套根式）
      - tuple                      （和式，例如 (sqrt2, sqrt3) 表示 sqrt2 + sqrt3）
      - list                       （积式，例如 [2, sqrt3] 表示 2 * sqrt3）
    """

    def __init__(self, index, radicand, coeff=1):
        self.index = index
        self.radicand = radicand
        self.coeff = coeff
        self._simplify()

    # ---------- 核心化简 ----------
    def _simplify(self):
        # 零系数直接化为 0
        if self.coeff == 0:
            self.index = 1
            self.radicand = 0
            return
        if self.coeff == 1 and self.radicand == 1:
            self.index = 1
            self.radicand = 1
            return

        # ✅ 新增：如果 radicand 是 1，直接化为 1
        if self.radicand == 1:
            self.index = 1
            self.radicand = 1
            return
        # 情形1：radicand 是数字
        if isinstance(self.radicand, (int, float)):
            if self.index == 1:
                if self.radicand < 0:
                    self.coeff *= -1
                    self.radicand = -self.radicand
                return
            if isinstance(self.radicand, int) and self.radicand > 0:
                n = self.radicand
                factors = {}
                d = 2
                while d * d <= n:
                    while n % d == 0:
                        factors[d] = factors.get(d, 0) + 1
                        n //= d
                    d += 1
                if n > 1:
                    factors[n] = factors.get(n, 0) + 1

                outside = 1
                inside = 1
                for p, e in factors.items():
                    q, r = divmod(e, self.index)
                    if q:
                        outside *= p ** q
                    if r:
                        inside *= p ** r
                self.coeff *= outside
                self.radicand = inside
                if self.radicand == 1:
                    self.index = 1
                return
            return

        # 情形1.1：radicand 是 Frac 对象
        if isinstance(self.radicand, Frac):
            frac = self.radicand
            # 根指数为1，就是普通分数
            if self.index == 1:
                return
            # 对分子和分母分别进行质因数分解

            def factorize(n):
                if n <= 1:
                    return {}
                factors = {}
                d = 2
                while d * d <= n:
                    while n % d == 0:
                        factors[d] = factors.get(d, 0) + 1
                        n //= d
                    d += 1
                if n > 1:
                    factors[n] = factors.get(n, 0) + 1
                return factors

            num_factors = factorize(frac.n)
            den_factors = factorize(frac.d)

            outside_num = 1
            inside_num = 1
            for p, e in num_factors.items():
                q, r = divmod(e, self.index)
                if q:
                    outside_num *= p ** q
                if r:
                    inside_num *= p ** r

            outside_den = 1
            inside_den = 1
            for p, e in den_factors.items():
                q, r = divmod(e, self.index)
                if q:
                    outside_den *= p ** q
                if r:
                    inside_den *= p ** r

            self.coeff *= outside_num / outside_den
            if inside_num == 1 and inside_den == 1:
                self.radicand = 1
                self.index = 1
            elif inside_den == 1:
                self.radicand = inside_num
            else:
                self.radicand = Frac(inside_num, inside_den)
            return

        # 情形1.5：radicand 是 tuple（分数形式），尝试化简
        if isinstance(self.radicand, tuple) and len(self.radicand) == 2:
            a, b = self.radicand
            if isinstance(a, (int, float)) and isinstance(b, (int, float)) and b != 0:
                # 计算最大公约数来化简分数
                if isinstance(a, int) and isinstance(b, int):
                    def gcd(x, y):
                        while y:
                            x, y = y, x % y
                        return x
                    g = gcd(abs(a), abs(b))
                    if g > 1:
                        a, b = a // g, b // g
                        self.radicand = (a, b)
                # 如果分母是完全幂次，可以提取
                if isinstance(b, int) and b > 1:
                    n = b
                    factors = {}
                    d = 2
                    while d * d <= n:
                        while n % d == 0:
                            factors[d] = factors.get(d, 0) + 1
                            n //= d
                        d += 1
                    if n > 1:
                        factors[n] = factors.get(n, 0) + 1
                    # 检查 index 是否能整除某个指数
                    for p, e in factors.items():
                        if e >= self.index:
                            q = e // self.index
                            if q > 0:
                                self.coeff *= p ** q
                                remaining_exp = e % self.index
                                if remaining_exp:
                                    self.radicand = (a, p ** remaining_exp)
                                else:
                                    self.radicand = a
                                if self.radicand == 1:
                                    self.index = 1
                                return
                return

        # 情形2：radicand 是根式（嵌套） (a^(1/n))^(1/m) = a^(1/(n*m))
        if isinstance(self.radicand, Radical):
            self.index = self.index * self.radicand.index
            self.radicand = self.radicand.radicand
            self._simplify()
            return

        # 情形3：radicand 是 tuple（和式）
        if isinstance(self.radicand, tuple):
            # 只有根指数为1时，才能展开合并同类项
            if self.index == 1:
                # 展平嵌套的 tuple，并应用系数
                flat_terms = []
                for item in self.radicand:
                    if isinstance(item, Radical):
                        if item.coeff == 0:
                            continue
                        # 应用当前系数
                        item = Radical(item.index, item.radicand,
                                       item.coeff * self.coeff)
                        if item.index == 1 and isinstance(item.radicand, tuple):
                            # 展开内部和式
                            for sub in item.radicand:
                                flat_terms.append(
                                    Radical(sub.index, sub.radicand, sub.coeff * self.coeff))
                            continue
                        flat_terms.append(item)
                    else:
                        # 数字项乘以系数
                        flat_terms.append(item * self.coeff)

                # 按 (index, radicand) 分组，合并同类项
                groups = {}
                for term in flat_terms:
                    if isinstance(term, Radical):
                        key = (term.index, term.radicand)
                        if key in groups:
                            groups[key] = groups[key] + term   # 利用 __add__
                        else:
                            groups[key] = term
                    else:
                        # 数字项，用 0 作为key
                        if 0 in groups:
                            groups[0] = groups[0] + term
                        else:
                            groups[0] = term

                new_terms = []
                for key, val in groups.items():
                    if isinstance(val, Radical):
                        if val.coeff != 0:
                            new_terms.append(val)
                    else:
                        if val != 0:
                            new_terms.append(val)

                if len(new_terms) == 0:
                    self.index = 1
                    self.radicand = 0
                    self.coeff = 1
                    return
                if len(new_terms) == 1:
                    t = new_terms[0]
                    if isinstance(t, Radical):
                        self.index = t.index
                        self.radicand = t.radicand
                        self.coeff = t.coeff
                    else:
                        self.index = 1
                        self.radicand = t
                        self.coeff = 1
                    return
                # 多个项，保留为和式
                self.radicand = tuple(new_terms)
                self.coeff = 1
                return
            # index > 1 时，如果和式可以化简为单个数字，先化简
            if self.index > 1:
                # 尝试创建一个临时 Radical(1, 和式) 来化简
                temp = Radical(1, self.radicand, 1)
                # 如果化简后是单个数字，替换 radicand
                if temp.index == 1 and isinstance(temp.radicand, (int, float)):
                    self.radicand = temp.radicand
                    self._simplify()
                    return
            # index > 1 时，根号内是和式，无法化简，保留
            return

        # 情形4：radicand 是 list（积式）
        if isinstance(self.radicand, list):
            # 仅当根指数为1时，尝试将数字因子乘到系数上
            if self.index == 1:
                num_factors = []
                rad_factors = []
                for item in self.radicand:
                    if isinstance(item, (int, float)):
                        num_factors.append(item)
                    else:
                        rad_factors.append(item)
                # 数字相乘
                prod = 1
                for x in num_factors:
                    prod *= x
                self.coeff *= prod
                if len(rad_factors) == 0:
                    self.index = 1
                    self.radicand = 1
                    return
                if len(rad_factors) == 1:
                    t = rad_factors[0]
                    if isinstance(t, Radical):
                        self.index = t.index
                        self.radicand = t.radicand
                        self.coeff *= t.coeff
                    else:
                        self.radicand = t
                    return
                # 多个根式因子，保持积式
                self.radicand = rad_factors
                return
            # index > 1 时，根号内是积式，无法进一步化简
            return

    # ---------- 辅助：底数乘法 ----------
    def _mul_radicand(self, a, b):
        """递归地相乘两个底数（数字/根式/和式/积式）"""
        # 两者都是数字
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a * b
        # 其中一个是数字
        if isinstance(a, (int, float)):
            if a == 1:
                return b
            if isinstance(b, tuple):        # 数字 × 和式
                return tuple(self._mul_radicand(a, x) for x in b)
            if isinstance(b, list):         # 数字 × 积式
                return [self._mul_radicand(a, x) for x in b]
            if isinstance(b, Radical):
                return Radical(b.index, b.radicand, a * b.coeff)
            return a * b
        if isinstance(b, (int, float)):
            return self._mul_radicand(b, a)

        # 和式 × 和式 -> 展开
        if isinstance(a, tuple) and isinstance(b, tuple):
            # 单元素元组直接取元素
            if len(a) == 1:
                a = a[0]
            if len(b) == 1:
                b = b[0]
            # 如果取元素后不是元组了，重新调用
            if not isinstance(a, tuple) or not isinstance(b, tuple):
                return self._mul_radicand(a, b)
            # 检测平方差: (x+y)(x-y) = x² - y²
            if len(a) == 2 and len(b) == 2:
                a0, a1 = a[0], a[1]
                b0, b1 = b[0], b[1]
                # 检查是否是 (x+y)(x-y) 形式，不考虑顺序
                # 情况1: (x+y)(x-y)
                if (a0 == b0 and a1 == b1) or (a0 == b1 and a1 == b0):
                    pass  # 不是平方差，是完全平方
                # 情况2: (x+y)(x-y) 其中一个符号相反

                def is_opposite(x, y):
                    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
                        return x == -y
                    if isinstance(x, Radical) and isinstance(y, Radical):
                        return x.index == y.index and x.radicand == y.radicand and x.coeff == -y.coeff
                    return False

                def to_number(x):
                    """尝试将值转换为数字"""
                    if isinstance(x, (int, float)):
                        return x
                    if isinstance(x, Radical) and x.index == 1 and isinstance(x.radicand, (int, float)):
                        return x.radicand * x.coeff
                    return None

                # 尝试匹配 (x+y)(x-y)
                if a0 == b0 and is_opposite(a1, b1):
                    x2 = self._pow_radicand(a0, 2)
                    y2 = self._pow_radicand(a1, 2)
                    x2_num = to_number(x2)
                    y2_num = to_number(y2)
                    if x2_num is not None and y2_num is not None:
                        return x2_num - y2_num
                    result = (x2, self._mul_radicand(y2, -1))
                    return result
                if a0 == b1 and is_opposite(a1, b0):
                    x2 = self._pow_radicand(a0, 2)
                    y2 = self._pow_radicand(a1, 2)
                    x2_num = to_number(x2)
                    y2_num = to_number(y2)
                    if x2_num is not None and y2_num is not None:
                        return x2_num - y2_num
                    result = (x2, self._mul_radicand(y2, -1))
                    return result
                # 另一种情况：(x+y)(y-x) = -(x-y)^2 = y² - x²
                if is_opposite(a0, b1) and a1 == b0:
                    x2 = self._pow_radicand(a1, 2)
                    y2 = self._pow_radicand(a0, 2)
                    x2_num = to_number(x2)
                    y2_num = to_number(y2)
                    if x2_num is not None and y2_num is not None:
                        return x2_num - y2_num
                    result = (x2, self._mul_radicand(y2, -1))
                    return result

            # 一般情况：展开
            terms = []
            for x in a:
                for y in b:
                    terms.append(self._mul_radicand(x, y))
            # 尝试合并同类项
            if len(terms) > 0:
                return Radical(1, tuple(terms), 1)
            return tuple(terms)

        # 和式 × 其他
        if isinstance(a, tuple):
            # 单元素元组直接取元素
            if len(a) == 1:
                return self._mul_radicand(a[0], b)
            return tuple(self._mul_radicand(x, b) for x in a)
        if isinstance(b, tuple):
            # 单元素元组直接取元素
            if len(b) == 1:
                return self._mul_radicand(a, b[0])
            return tuple(self._mul_radicand(a, x) for x in b)

        # 其他情况（根式×根式，积式×积式等）
        if isinstance(a, Radical) and isinstance(b, Radical):
            # 两个根式相乘
            new_coeff = a.coeff * b.coeff
            if a.index == b.index:
                new_rad = self._mul_radicand(a.radicand, b.radicand)
                return Radical(a.index, new_rad, new_coeff)
            # 指数不同，化为公指数
            common_idx = a.index * b.index
            r1 = self._pow_radicand(a.radicand, b.index)
            r2 = self._pow_radicand(b.radicand, a.index)
            new_rad = self._mul_radicand(r1, r2)
            return Radical(common_idx, new_rad, new_coeff)

        if isinstance(a, list) and isinstance(b, list):
            return a + b
        if isinstance(a, list):
            return a + [b]
        if isinstance(b, list):
            return [a] + b
        return [a, b]

    # ---------- 辅助：底数乘方 ----------
    def _pow_radicand(self, radicand, exp):
        """底数的非负整数次幂"""
        if exp == 0:
            return 1
        if exp == 1:
            return radicand
        # 数字
        if isinstance(radicand, (int, float)):
            return radicand ** exp
        # 根式
        if isinstance(radicand, Radical):
            # (a^(1/n))^exp = a^(exp/n)
            # 用新的根式表示，再化简
            return Radical(radicand.index, radicand.radicand ** exp, radicand.coeff ** exp)
        # 和式 (二项式展开)
        if isinstance(radicand, tuple):
            # 将和式视为多项式 (a1 + a2 + ...)^exp
            # 使用递归展开
            if exp == 0:
                return 1
            if exp == 1:
                return radicand
            # 取第一项 + 剩余项
            first = radicand[0]
            rest = radicand[1:]
            if len(rest) == 0:
                return self._pow_radicand(first, exp)
            # (first + rest)^exp = sum_{k=0}^{exp} C(exp,k) * first^k * rest^(exp-k)

            def binom(n, k):
                if k < 0 or k > n:
                    return 0
                k = min(k, n-k)
                res = 1
                for i in range(k):
                    res = res * (n - i) // (i + 1)
                return res

            total = None
            rest_poly = rest  # rest 作为整体
            for k in range(exp + 1):
                c = binom(exp, k)
                term1 = self._pow_radicand(first, k)
                term2 = self._pow_radicand(rest_poly, exp - k)
                prod = self._mul_radicand(term1, term2)
                if c != 1:
                    prod = self._mul_radicand(c, prod)
                if total is None:
                    total = prod
                else:
                    total = (total, prod) if isinstance(
                        total, tuple) else (total, prod)
            if total is None:
                return 0
            # 展平嵌套的元组

            def flatten(t):
                if isinstance(t, tuple):
                    result = []
                    for item in t:
                        result.extend(flatten(item))
                    return result
                return [t]
            total = tuple(flatten(total))
            # 展开后尝试化简：如果是和式，创建 Radical 并让 _simplify 处理
            if isinstance(total, tuple):
                temp = Radical(1, total, 1)
                # 如果化简后是单个项，直接返回
                if temp.index == 1 and isinstance(temp.radicand, (int, float)):
                    return temp.radicand * temp.coeff
                if len(temp.radicand) == 1 and isinstance(temp.radicand, tuple):
                    return temp.radicand[0]
                return temp
            return total
        # 积式
        if isinstance(radicand, list):
            # (a*b*c)^exp = a^exp * b^exp * c^exp
            result = 1
            for item in radicand:
                result = self._mul_radicand(
                    result, self._pow_radicand(item, exp))
            return result
        return radicand

    # ---------- 共轭（用于分母有理化）----------
    def conjugate(self):
        """返回二项式和式的共轭，仅当 self 是 a + b 形式"""
        if self.index == 1 and isinstance(self.radicand, tuple) and len(self.radicand) == 2:
            a, b = self.radicand[0], self.radicand[1]
            if isinstance(b, Radical):
                # 取反系数
                return Radical(1, (a, Radical(b.index, b.radicand, -b.coeff)), self.coeff)
            if isinstance(b, (int, float)):
                return Radical(1, (a, -b), self.coeff)
        return None

    # ---------- 四则运算 ----------
    def __add__(self, other):
        if not isinstance(other, Radical):
            other = Radical(1, other, 1)
        if self.coeff == 0:
            return other
        if other.coeff == 0:
            return self

        def to_frac(val):
            if isinstance(val, Frac):
                return val
            if isinstance(val, (int, float)):
                return Frac(val)
            return val
        if self.index == other.index and self.radicand == other.radicand:
            new_coeff = to_frac(self.coeff) + to_frac(other.coeff)
            return Radical(self.index, self.radicand, new_coeff)
        if self.index == 1 and isinstance(self.radicand, tuple):
            return Radical(1, self.radicand + (other,), 1)
        if other.index == 1 and isinstance(other.radicand, tuple):
            return other + self
        return Radical(1, (self, other), 1)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, Radical):
            other = Radical(1, other, 1)
        return self + Radical(other.index, other.radicand, -other.coeff)

    def __rsub__(self, other):
        return Radical(1, other, 1) - self

    def __mul__(self, other):
        if not isinstance(other, Radical):
            other = Radical(1, other, 1)
        if self.coeff == 0 or other.coeff == 0:
            return Radical(1, 0, 0)

        def to_frac(val):
            if isinstance(val, Frac):
                return val
            if isinstance(val, (int, float)):
                return Frac(val)
            return val
        new_coeff = to_frac(self.coeff) * to_frac(other.coeff)

        if (self.index == 1 and isinstance(self.radicand, (int, float)) and
                other.index == 1 and isinstance(other.radicand, (int, float))):
            return Radical(1, self.radicand * other.radicand, new_coeff)

        if self.index == other.index:
            if self.radicand == other.radicand:
                return Radical(1, self.radicand, to_frac(self.coeff) * to_frac(other.coeff))
            new_rad = self._mul_radicand(self.radicand, other.radicand)
            if isinstance(new_rad, tuple):
                new_rad = Radical(1, new_rad, 1)
            return Radical(self.index, new_rad, new_coeff)

        common_idx = self.index * other.index
        r1 = self._pow_radicand(self.radicand, other.index)
        r2 = self._pow_radicand(other.radicand, self.index)
        new_rad = self._mul_radicand(r1, r2)
        return Radical(common_idx, new_rad, new_coeff)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, Radical):
            other = Radical(1, other, 1)
        if other.coeff == 0:
            raise ZeroDivisionError("Division by zero radical")

        def to_frac(val):
            if isinstance(val, Frac):
                return val
            if isinstance(val, (int, float)):
                return Frac(val)
            return val

        # ========== 1. 分母是纯数字 ==========
        if other.index == 1 and isinstance(other.radicand, (int, float, Frac)):
            # ✅ 关键修复：正确处理纯数字分母
            if self.index == 1 and isinstance(self.radicand, tuple):
                # 分子是和式，需要把系数除到每一项
                terms = list(self.radicand)
                new_terms = []
                for term in terms:
                    if isinstance(term, Radical):
                        new_coeff = to_frac(term.coeff) / \
                            to_frac(other.radicand)
                        new_terms.append(
                            Radical(term.index, term.radicand, new_coeff))
                    else:
                        # 数字项
                        new_terms.append(term / other.radicand)
                return Radical(1, tuple(new_terms), 1)

            new_coeff = to_frac(self.coeff) / to_frac(other.radicand)
            return Radical(self.index, self.radicand, new_coeff)

        # ========== 2. 分母是根式表达式 ==========
        # 核心思想：改变最后一项的符号，递归消元
        if other.index == 1 and isinstance(other.radicand, tuple):
            terms = list(other.radicand)

            # 二项式：直接用共轭
            if len(terms) == 2:
                conj = other.conjugate()
                if conj:
                    num = self * conj
                    den = other * conj
                    return num / den  # 递归调用自己

            # 三项及以上：改变最后一项的符号
            if len(terms) >= 3:
                last = terms[-1]
                rest = terms[:-1]

                # 构造共轭：rest - last
                if isinstance(last, Radical):
                    last_neg = Radical(last.index, last.radicand, -last.coeff)
                else:
                    last_neg = -last

                conj = Radical(1, tuple(rest + [last_neg]), 1)

                num = self * conj
                den = other * conj

                # 递归有理化
                return num / den

        # ========== 3. 同类根式相除 ==========
        if self.index == other.index and self.radicand == other.radicand:
            if isinstance(other, (int, float, Frac)):
                return self / other
            new_coeff = to_frac(self.coeff) / to_frac(other.coeff)
            return Radical(1, 1, new_coeff)

        # ========== 4. 同指数不同底数 ==========
        if self.index == other.index:
            a = self.radicand
            b = other.radicand
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                new_rad = Frac(a, b)
                new_coeff = to_frac(self.coeff) / to_frac(other.coeff)
                return Radical(self.index, new_rad, new_coeff)
            else:
                new_coeff = to_frac(self.coeff) / to_frac(other.coeff)
                return Radical(self.index, [a, b] if not isinstance(b, (int, float)) else [a, 1/b], new_coeff)

        # ========== 5. 一般情况 ==========
        common_idx = self.index * other.index
        r1 = self._pow_radicand(self.radicand, other.index)
        r2 = self._pow_radicand(other.radicand, self.index)

        if isinstance(r2, (int, float)) and r2 != 0:
            new_coeff = to_frac(self.coeff) / \
                (to_frac(other.coeff) * to_frac(r2))
            return Radical(other.index, other.radicand, new_coeff)

        new_coeff = to_frac(self.coeff) / to_frac(other.coeff)
        new_rad = [r1, r2] if not isinstance(r2, (int, float)) else [r1, 1/r2]
        return Radical(common_idx, new_rad, new_coeff)

    def __rtruediv__(self, other):
        return Radical(1, other, 1) / self

    def __neg__(self):
        if isinstance(self.coeff, Frac):
            new_coeff = Frac(-self.coeff.n, self.coeff.d)
        else:
            new_coeff = -self.coeff
        return Radical(self.index, self.radicand, new_coeff)

    def __pos__(self):
        return self

    def __pow__(self, exp):
        if not isinstance(exp, int) or exp < 0:
            raise ValueError("Exponent must be a non-negative integer")
        if exp == 0:
            return Radical(1, 1, 1)
        if exp == 1:
            return self
        # (coeff * a^(1/n))^p = coeff^p * a^(p/n)
        new_coeff = self.coeff ** exp
        new_rad = self._pow_radicand(self.radicand, exp)
        # 如果 exp 是 index 的倍数，化简
        if exp % self.index == 0:
            # (a^(1/n))^(n*k) = a^k
            k = exp // self.index
            return Radical(1, self._pow_radicand(self.radicand, k), new_coeff)
        # 化简 (a^(p/n)) 为根式
        if isinstance(new_rad, int) and new_rad > 0:
            sqrt_val = int(new_rad ** 0.5)
            if sqrt_val * sqrt_val == new_rad:
                return Radical(1, 1, new_coeff * sqrt_val)
            return Radical(self.index, new_rad, new_coeff)
        if isinstance(new_rad, float) and new_rad > 0:
            sqrt_val = int(new_rad ** 0.5 + 0.5)
            if abs(sqrt_val * sqrt_val - new_rad) < 1e-9:
                return Radical(1, 1, new_coeff * sqrt_val)
        # 其他情况，保留根式形式让 _simplify 处理
        return Radical(self.index, new_rad, new_coeff)

    # ---------- 比较与显示 ----------
    def __eq__(self, other):
        if not isinstance(other, Radical):
            return False

        # 先比较简单属性
        if self.index != other.index:
            return False

        # 比较系数
        if self.coeff != other.coeff:
            return False

        # 比较 radicand - 只有简单类型才直接比较
        def is_simple_type(val):
            return isinstance(val, (int, float, str, Frac))

        if is_simple_type(self.radicand) and is_simple_type(other.radicand):
            return self.radicand == other.radicand

        # 对于复杂类型（tuple, list, Radical），用 repr 比较
        return repr(self.radicand) == repr(other.radicand)

    def __hash__(self):
        return hash((self.index, self.radicand, self.coeff))

    def _to_str(self, radicand):
        if isinstance(radicand, Frac):
            if radicand.d == 1:
                return str(radicand.n)
            return f"({radicand.n}/{radicand.d})"
        if isinstance(radicand, (int, float)):
            return str(radicand)
        if isinstance(radicand, Radical):
            return radicand.__str__()

        def is_fraction(t):
            """检测 tuple 是否是分数形式（两个整数）"""
            if not isinstance(t, tuple) or len(t) != 2:
                return False
            a, b = t
            return isinstance(a, int) and isinstance(b, int) and b > 1

        if isinstance(radicand, tuple):
            if is_fraction(radicand):
                a, b = radicand
                a_str = self._to_str(a)
                b_str = self._to_str(b)
                return f"({a_str}/{b_str})"
            parts = []
            for i, x in enumerate(radicand):
                s = self._to_str(x)
                if i > 0 and s.startswith('-'):
                    parts.append(" - " + s[1:])
                elif i > 0:
                    parts.append(" + " + s)
                else:
                    parts.append(s)
            return "(" + "".join(parts) + ")"
        if isinstance(radicand, list):
            return "(" + " * ".join(self._to_str(x) for x in radicand) + ")"
        return str(radicand)

    def __str__(self):
        if self.coeff == 0:
            return "0"

        def format_coeff(c):
            if isinstance(c, Frac):
                if c.d == 1:
                    return str(c.n)
                if c.n < 0:
                    return f"({c.n}/{c.d})"
                return f"({c.n}/{c.d})"
            if isinstance(c, float) and c == int(c):
                return str(int(c))
            return str(c)

        def is_one(c):
            if isinstance(c, Frac):
                return c.n == 1 and c.d == 1
            return c == 1

        def is_neg_one(c):
            if isinstance(c, Frac):
                return c.n == -1 and c.d == 1
            return c == -1

        coeff_str = format_coeff(self.coeff)

        if self.index == 1:
            if self.radicand == 1:
                return coeff_str
            rad_str = self._to_str(self.radicand)
            if is_one(self.coeff):
                return rad_str
            if is_neg_one(self.coeff):
                return "-" + rad_str
            return coeff_str + "*" + rad_str

        rad_str = self._to_str(self.radicand)
        if self.index == 2:
            root_symbol = "sqrt"
        else:
            root_symbol = f"root[{self.index}]"
        if is_one(self.coeff):
            return f"{root_symbol}({rad_str})"
        if is_neg_one(self.coeff):
            return f"-{root_symbol}({rad_str})"
        return coeff_str + "*" + f"{root_symbol}({rad_str})"

    def __repr__(self):
        return self.__str__()
