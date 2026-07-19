from .smath import sqrt, cos, sin, pi, EPSILON, Complex


class NoSolutionError(Exception):
    pass


def solve_linear(a, b):
    """解一次方程 ax + b = 0"""
    if a == 0:
        if b == 0:
            return 'infinite'  # 无数解
        else:
            raise NoSolutionError("无解")
    return [(-b) / a]


def solve_quadratic(a, b, c):
    """解二次方程 ax² + bx + c = 0（支持复数）"""
    if a == 0:
        return solve_linear(b, c)

    delta = b*b - 4*a*c

    # 直接计算平方根（复数自动处理）
    sqrt_delta = sqrt(delta)
    x1 = (-b - sqrt_delta) / (2*a)
    x2 = (-b + sqrt_delta) / (2*a)

    if x1 == x2:
        return [x1]
    return [x1, x2]


def solve_cubic(a, b, c, d):
    """解三次方程 ax³ + bx² + cx + d = 0（支持复数）"""
    if a == 0:
        return solve_quadratic(b, c, d)
    # 1. 计算 p, q
    p = (3*a*c - b*b) / (3*a*a)
    q = (2*b*b*b - 9*a*b*c + 27*a*a*d) / (27*a*a*a)

    # 2. 判别式
    delta = (q/2)**2 + (p/3)**3

    # 3. 计算 u, v
    u = Complex(-q/2 + delta**0.5, 0) ** (1/3)  # 主立方根
    v = Complex(-q/2 - delta**0.5, 0) ** (1/3)

    # 4. 关键：调整 v 使 u*v = -p/3
    if abs(u*v + p/3) > EPSILON:
        v = -p/(3*u)  # 强制满足关系

    # 5. 三个根
    omega = Complex(-0.5, 0.8660254037844386)
    omega2 = omega * omega

    y1 = u + v
    y2 = u*omega + v*omega2
    y3 = u*omega2 + v*omega

    # 6. 还原 x
    x1 = y1 - b/(3*a)
    x2 = y2 - b/(3*a)
    x3 = y3 - b/(3*a)

    return [x1, x2, x3]


def _is_zero(x, eps=EPSILON):
    """判断是否接近0"""
    return abs(x) < eps


def solve_quartic(a, b, c, d, e):
    """
    解 ax^4 + bx^3 + cx^2 + dx + e = 0
    返回四个复根列表
    """
    if abs(a) < EPSILON:
        # 降级为三次（你的 solve_cubic 应该处理这种情况）
        return solve_cubic(b, c, d, e)

    # 归一化：x^4 + px^3 + qx^2 + rx + s = 0
    p = b / a
    q = c / a
    r = d / a
    s = e / a

    # 消去三次项：令 x = y - p/4
    # 得到 y^4 + P y^2 + Q y + R = 0
    P = q - (3 * p * p) / 8
    Q = r - (p * q) / 2 + (p * p * p) / 8
    R = s - (p * r) / 4 + (p * p * q) / 16 - (3 * p * p * p * p) / 256

    # 特殊情况：Q=0，双二次方程
    if abs(Q) < EPSILON:
        # y^4 + P y^2 + R = 0
        y2_roots = solve_quadratic(1, P, R)
        roots_y = []
        for y2 in y2_roots:
            roots_y.extend(solve_quadratic(1, 0, -y2))
        return [y - p/4 for y in roots_y]

    # 辅助三次方程：8z^3 - 4P z^2 - 8R z + (4PR - Q^2) = 0
    A3 = 8.0
    B3 = -4.0 * P
    C3 = -8.0 * R
    D3 = 4.0 * P * R - Q * Q

    z_roots = solve_cubic(A3, B3, C3, D3)

    # 选取合适的 z（使 2z-P ≠ 0）
    z = z_roots[0]
    for zz in z_roots:
        if abs(2 * zz - P) > EPSILON:
            z = zz
            break

    denom = 2 * z - P
    if abs(denom) < EPSILON:
        # 退化情况：尝试用另一个根
        for zz in z_roots:
            if abs(2 * zz - P) > EPSILON:
                z = zz
                denom = 2 * z - P
                break
        if abs(denom) < EPSILON:
            # 极端退化，理论上不会发生
            return []

    sqrt_term = sqrt(denom)  # 你的 sqrt 支持复数
    coef = Q / denom

    # 两个二次方程：
    # y^2 + sqrt_term * y + (z - sqrt_term * coef) = 0
    # y^2 - sqrt_term * y + (z + sqrt_term * coef) = 0
    roots_y1 = solve_quadratic(1, sqrt_term, z - sqrt_term * coef)
    roots_y2 = solve_quadratic(1, -sqrt_term, z + sqrt_term * coef)

    all_y = roots_y1 + roots_y2
    return [y - p/4 for y in all_y]


def solve_polynomial(coefficients):
    """自动选择解法"""
    # 去掉开头的0
    while len(coefficients) > 1 and _is_zero(coefficients[0]):
        coefficients.pop(0)

    n = len(coefficients) - 1  # 次数

    if n == 0:
        return 'infinite' if _is_zero(coefficients[0]) else []
    elif n == 1:
        return solve_linear(coefficients[0], coefficients[1])
    elif n == 2:
        return solve_quadratic(coefficients[0], coefficients[1], coefficients[2])
    elif n == 3:
        return solve_cubic(coefficients[0], coefficients[1], coefficients[2], coefficients[3])
    else:
        raise ValueError(f"不支持 {n} 次方程")


def solve_polynomial_numerical(coefficients, max_iter=1000, tol=1e-10):
    """数值求解任意次多项式方程"""

    # 去除前导零
    while len(coefficients) > 1 and abs(coefficients[0]) < EPSILON:
        coefficients.pop(0)

    n = len(coefficients) - 1

    if n == 0:
        return []
    elif n == 1:
        return solve_linear(coefficients[0], coefficients[1])
    elif n == 2:
        return solve_quadratic(coefficients[0], coefficients[1], coefficients[2])
    elif n == 3:
        return solve_cubic(coefficients[0], coefficients[1], coefficients[2], coefficients[3])
    # n >= 4，用 Durand-Kerner 数值方法
    roots = []
    for k in range(n):
        angle = 2 * pi * k / n
        roots.append(Complex(cos(angle), sin(angle)))

    # 迭代优化
    for _ in range(max_iter):
        max_delta = 0
        new_roots = []

        for i, r in enumerate(roots):
            # 计算 P(r)
            p = Complex(coefficients[0], 0)
            for coef in coefficients[1:]:
                p = p * r + Complex(coef, 0)

            # 计算分母 ∏(r - r_j) for j≠i
            denom = Complex(1, 0)
            for j, rj in enumerate(roots):
                if i != j:
                    denom *= (r - rj)

            # 牛顿步长
            if abs(denom) < EPSILON:
                delta = Complex(0, 0)
            else:
                delta = p / denom

            new_root = r - delta
            new_roots.append(new_root)

            if abs(delta) > max_delta:
                max_delta = abs(delta)

        roots = new_roots

        if max_delta < tol:
            break

    # 清理极小虚部
    cleaned = []
    for r in roots:
        if abs(r.imag) < tol:
            cleaned.append(r.real)
        else:
            cleaned.append(r)

    return cleaned
# ========== 便捷函数 ==========


def roots(coefficients):
    """求根（别名）"""
    return solve_polynomial(coefficients.copy())


def poly(val, coefficients):
    """计算多项式值（支持复数）"""
    result = 0
    for c in coefficients:
        result = result * val + c
    return result
