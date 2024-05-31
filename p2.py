import numpy as np
from itertools import combinations_with_replacement
# Convecion: Q0 Q1 Q2


def self_outer(number: int):
    v = vec_at(number)
    return np.outer(v, v)


def vec_at(number):
    v = np.zeros((8, 1))
    v[number][0] = 1
    return v


P = [
    self_outer(0) + self_outer(0b111),
    self_outer(0b001) + self_outer(0b110),
    self_outer(0b010) + self_outer(0b101),
    self_outer(0b100) + self_outer(0b011),
]

b = vec_at(0b0)
p = [
    vec_at(0b111),
    vec_at(0b110),
    vec_at(0b101),
    vec_at(0b011),
]
for i, j in combinations_with_replacement(range(4), 2):
    print(f"{i}, {j}")
    P_j = P[j]
    p_i = p[i]
    m_i = P_j @ p_i
    r_i = np.inner(p[i].T, m_i.T)

    #print("P_I", P_j, sep="\n")
    #print("p_I", p_i, sep="\n")
    #print("r_I", r_i, sep="\n")
    if i == j:
        assert np.allclose(r_i, np.ones_like(r_i))
    else:
        assert np.allclose(r_i, np.zeros_like(r_i))
