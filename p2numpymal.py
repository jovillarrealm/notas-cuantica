import numpy as np
from itertools import combinations_with_replacement, cycle
# Convecion: Q0 Q1 Q2


def vec_at(number):
    v = np.zeros((8, 1),dtype=np.uint8)
    v[number][0] = 1
    return v
def self_outer(number: int):
    v = vec_at(number)
    return np.outer(v, v)


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


def imprimir_multiplicacion_matrices_latex(A, B, C):
    r"""
  Función para imprimir la multiplicación de matrices de arreglos en numpy como LaTeX.

  Args:
    A: Matriz numpy.
    B: Matriz numpy.
    C: Matriz numpy como resultado de la multiplicación A x B.

  Ejemplo:
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    C = np.dot(A, B)
    imprimir_multiplicacion_matrices_latex(A, B, C)

  Salida:
    \begin{equation}
    \begin{pmatrix}
      1 & 2 \\
      3 & 4
    \end{pmatrix}
    \begin{pmatrix}
      5 & 6 \\
      7 & 8
    \end{pmatrix}
    =
    \begin{pmatrix}
      19 & 22 \\
      43 & 50
    \end{pmatrix}
    \end{equation}
  """
    syms = cycle(["\\alpha", "\\beta"])
    is_vec = lambda v: 1 in v.shape
    A_is_vec, B_is_vec, C_is_vec = is_vec(A),is_vec(B),is_vec(C)
    C_is_scalar = (1,1) == C.shape
    # Imprimir matrices A y B
    print(r"\begin{equation}")

    print(r"\begin{pmatrix}")
    for fila in A:
        for elemento in fila:
            if elemento ==1 and A_is_vec:
                print(f"{syms.__next__()} & ", end="")
            else:
                print(f"{elemento} & ", end="")

        print(r"\\")
    print(r"\end{pmatrix}")
    print(r" \begin{pmatrix}")
    for fila in B:
        for elemento in fila:
            if elemento ==1 and B_is_vec:
                print(f"{syms.__next__()} & ", end="")
            else:
                print(f"{elemento} & ", end="")
        print(r"\\")
    print(r"\end{pmatrix}")
    print(r" = ")

    # Imprimir matriz C
    if C_is_scalar:
        if  C[0][0] == 1:
            print(f"{syms.__next__()}^2+{syms.__next__()}^2 & ", end="")
            print(r" = ")
            print("1")
        elif  C[0][0] == 0:
            print("0")
    else:
        print(r"\begin{pmatrix}")
        for fila in C:
            for elemento in fila:
                if elemento ==1 and C_is_vec:
                    print(f"{syms.__next__()} & ", end="")
                else:
                    print(f"{elemento} & ", end="")
            print(r"\\")
        print(r"\end{pmatrix}")

    print(r"\end{equation}")


def print_ij(i, j):
    print(r"\begin{equation}")
    print(r"\begin{pmatrix}")
    print(f"i={i} & ", end="")
    print(r"\\")
    print(f"j={j} & ", end="")
    print(r"\\")
    print(r"\end{pmatrix}")
    print(r"\end{equation}")


def imprinting(P, p, cond):
    for i, j in combinations_with_replacement(range(4), 2):
        if cond(i, j):
            # print(f"{i}, {j}")
            P_j = P[j]
            p_i = p[i]
            m_i = P_j @ p_i
            r_i:np.ndarray = np.dot(p[i].T, m_i)
            print_ij(i, j)
            imprimir_multiplicacion_matrices_latex(P_j, p_i, m_i)
            imprimir_multiplicacion_matrices_latex(p_i.T, m_i, r_i)

            # print("P_I", P_j, sep="\n")
            #print("p_I", p_i, sep="\n")
            #print("m_I", m_i, sep="\n")
            #print("r_I", r_i, sep="\n")
            assert r_i.shape == (1, 1)
            respuesta = r_i[0][0]
            if i == j:
                assert np.allclose(respuesta, 1)
            else:
                assert np.allclose(respuesta, 0)


same = lambda i, j: i == j
not_same = lambda i, j: i != j

#imprinting(P, p, same)
#imprinting(P, p, not_same)

