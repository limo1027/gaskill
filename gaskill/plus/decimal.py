class Decimal:
    def __init__(self, value, fr_len=None):
        if fr_len is not None:
            self.value = value
            self.fr_len = fr_len
            self._simplify()
            return
        self.value = float(value)
        self.fr_len = len(str(self.value).split(".")[-1])
        self.value = int(self.value*(10 ** self.fr_len))
        self._simplify()

    def _simplify(self):
        while self.value % 10 == 0:
            self.value /= 10
            self.fr_len += 1

    def _to_decimal(self, value):
        return Decimal(value)

    def __add__(self, other):
        other = self._to_decimal(other)
        if self.fr_len == other.fr_len:
            return Decimal(self.value + other.value, self.fr_len)
        else:
            while self.fr_len == other.fr_len:
                self.fr_len -= 1
                self.value *= 10
            result = self + other
            self._simplify()
            return result

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        other = self._to_decimal(other)
        return self + (-other)

    def __neg__(self):
        return Decimal(-self.value, self.fr_len)

    def __eq__(self, other):
        other = self._to_decimal(other)
        return self.value == other.value and self.fr_len == other.fr_len

    def __repr__(self):
        result = list(str(int(self.value)))
        result.insert(-self.fr_len, ".")
        if result[0] == ".":
            result.insert(0, "0")
        return f"Decimal({"".join(result)})"

    def __str__(self):
        return repr(self)

    def __mul__(self, other):
        other = self._to_decimal(other)
        return Decimal(self.value * other.value, self.fr_len + other.fr_len)

    def __truediv__(self, other):
        other = self._to_decimal(other)
        result = ""
        mod = self.value
        for i in range(50):
            quo, mod = divmod(mod, other.value)
            result += str(int(quo))
            mod *= 10
        return Decimal(int(result), 50)

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return self / other

    def __lt__(self, other):
        if self.fr_len != other.fr_len and len(str(self.value)) == len(str(other.value)):
            return self.fr_len > other.fr_len
        for i, j in zip(str(self.value), str(other.value)):
            if i < j:
                return True
            elif i > j:
                return False

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, ohter):
        return not (self == other or self < other)

    def __ge__(self, ohter):
        return self == other or self > ohter

    def __ne__(self, other):
        return not self == other

    def __float__(self):
        return self.value / (10 ** self.fr_len)
