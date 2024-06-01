from sympy import Matrix, latex
from sympy.abc import alpha, beta
import numpy as np
from itertools import combinations_with_replacement
from typing import Callable
import sympy as sy


def vec_ab(ai, bi):
    v = [0] * 8
    v[ai] = alpha
    v[bi] = beta

    v = Matrix(v, shape=(8, 1))
    return v


def vec_at(number):
    v = [0] * 8
    v[number] = 1
    v = Matrix(v, shape=(8, 1))
    return v


def self_outer(n):
    v = vec_at(n)
    v = np.array(v, dtype=np.uint8)
    return np.outer(v, v)


def mul_print(A, B, C):
    if isinstance(C, sy.Add):
        ans = [
            f"""\\\\
{latex(A)}
\\cdot
{latex(B)}
=
{latex(C)}
=
1
\\\\"""
        ]

    else:
        ans = [
            f"""\\\\
{latex(A)}
\\cdot
{latex(B)}
=
{latex(C)}
\\\\"""
        ]
    return ans


p = [
    vec_ab(0b000, 0b111),
    vec_ab(0b001, 0b110),
    vec_ab(0b010, 0b101),
    vec_ab(0b100, 0b011),
]

P = [
    self_outer(0) + self_outer(0b111),
    self_outer(0b001) + self_outer(0b110),
    self_outer(0b010) + self_outer(0b101),
    self_outer(0b100) + self_outer(0b011),
]
P = [Matrix(p) for p in P]
# print(p)


def imprinting(P: list[Matrix], p: list[Matrix], cond: Callable):
    ans = []
    for i, j in combinations_with_replacement(range(4), 2):
        if cond(i, j):
            # print(f"{i}, {j}")
            P_j = P[j]
            p_i = p[i]
            m_i = P_j * p_i
            r_i = p[i].dot(m_i)

            # print("P_I", P_j, sep="\n")
            # print("p_I", p_i, sep="\n")
            # print("m_I", m_i, sep="\n")
            # print("r_I", r_i, sep="\n")
            ans.append(ij(i, j))
            ans.append(mul_print(P_j, p_i, m_i))
            if i == j:
                ans.append(mul_print(p_i.T, m_i, r_i))
                assert isinstance(r_i, sy.Add)
            else:
                ans.append(mul_print(p_i.T, m_i, r_i))
                assert r_i == 0
    ans = ("\n".join(line) for line in ans)
    for i in ans:
        print(i)


def same(i, j):
    return i == j
def not_same(i, j):
    return i != j


def ij(i, j):
    return (
        "\\begin{equation}",
        "\\begin{pmatrix}",
        f"i={i} & ",
        "\\\\",
        f"j={j} & ",
        "\\\\",
        "\\end{pmatrix}",
        "\\end{equation}",
        "\\\\",
    )


imprinting(P, p, same)
