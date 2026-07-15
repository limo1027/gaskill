from .srandom import Random


class SGTsaver:
    """sgt存档器"""

    def __init__(self):
        self.saver_dicts = {}
        self.hasher = Random("sgt_checksum")

    def set_value(self, **kwargs):
        """设置值：set_value(score=100, name="hero")"""
        for key, value in kwargs.items():
            self.saver_dicts[key] = value
        return self

    def add(self, key, value):
        """添加单个值"""
        self.saver_dicts[key] = value
        return self

    def _value_to_str(self, value):
        """值转字符串"""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, (list, tuple)):
            return "[" + ",".join(("\""+str(v))+"\"" for v in value) + "]"
        elif hasattr(value, 'x') and hasattr(value, 'y') and hasattr(value, 'z'):
            return f"({value.x},{value.y},{value.z})"
        elif hasattr(value, 'x') and hasattr(value, 'y'):
            return f"({value.x},{value.y})"
        else:
            return str(value)

    def _str_to_value(self, s):
        """字符串转值"""
        s = s.strip()
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1]
        elif s == "true":
            return True
        elif s == "false":
            return False
        elif s.startswith('[') and s.endswith(']'):
            items = s[1:-1].split(',')
            return [self._str_to_value(item) for item in items if item]
        elif s.startswith('(') and s.endswith(')'):
            items = s[1:-1].split(',')
            if len(items) == 2:
                return (float(items[0]), float(items[1]))
            elif len(items) == 3:
                return (float(items[0]), float(items[1]), float(items[2]))
        else:
            try:
                return int(s)
            except:
                try:
                    return float(s)
                except:
                    return s

    def save(self, filename, use_hash=True):
        """保存到文件"""
        lines = []

        for key, value in self.saver_dicts.items():
            value_str = self._value_to_str(value)
            lines.append(f"#{key}={value_str}")

        if use_hash:
            content = "\n".join([l for l in lines if l.startswith('#')])
            hash_value = self.hasher.hash(content)
            if hasattr(hash_value, '__iter__') and not isinstance(hash_value, (str, int)):
                hash_value = ''.join(str(h) for h in hash_value)
            lines.append(f"hash={hash_value}")

        if isinstance(filename, str):
            with open(filename, 'w') as f:
                f.write("\n".join(lines))
        else:
            filename.write("\n".join(lines))

        return True

    def load(self, filename, require_hash=True):
        """从文件加载"""
        self.saver_dicts = {}

        if isinstance(filename, str):
            with open(filename, 'r') as f:
                lines = f.readlines()
        else:
            lines = filename.read().split("\n")
        hash_lines = []
        saved_hash = None

        for line in lines:
            line = line.strip()
            if line.startswith("hash"):
                saved_hash = line[5:]
            if not line.startswith('#'):
                continue

            hash_lines.append(line)

            line = line[1:]

            if '=' not in line:
                continue

            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()

            self.saver_dicts[key] = self._str_to_value(value)

        if require_hash and saved_hash is None:
            raise ValueError("文件缺少校验和")
        if not saved_hash:
            return self.saver_dicts

        content = "\n".join([l for l in hash_lines])
        calc_hash = self.hasher.hash(content)
        calc_hash = ''.join(str(h) for h in calc_hash)

        if str(calc_hash) != str(saved_hash):
            raise ValueError("文件被修改过")
        return self.saver_dicts

    def get(self, key, default=None):
        """获取值"""
        return self.saver_dicts.get(key, default)

    def __getitem__(self, key):
        """支持 [] 访问"""
        return self.saver_dicts[key]

    def __setitem__(self, key, value):
        """支持 [] 赋值"""
        self.saver_dicts[key] = value
        return self
