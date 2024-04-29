# %% [markdown]
#

# %%
from functools import lru_cache
from math import log, sqrt, ceil
from typing import Callable

import numpy as np
from numpy import ndarray
#from scipy import sparse as sp


# %%


@lru_cache(maxsize=1)
def H_otimes_n(n: int) -> ndarray:
    r"""
    Retorna :math:`H^{\otimes n}`

    Args:
        n (int): numero de qubits
    """

    hadamard: ndarray = np.sqrt(0.5) * np.array([[1, 1], [1, -1]])
    result = hadamard
    n -= 1  # primera iteración siempre inicia en hadamard, pero no cuenta como multiplicación

    for _ in range(n):
        result = np.kron(result, hadamard)
    # Kronecker products crea submatrices, esto reshapea a matriz
    op = result.reshape(-1, result.shape[-1])
    return op


# %%
@lru_cache(maxsize=1)
def proyection_about_mean(N: int):
    op = np.ones(N) * (2 / N) - np.eye(N)
    return op


# %%



# %%
# TODO!
@lru_cache(maxsize=1)
def phase_inversion(N, f: Callable) -> ndarray:
    """
    1s en la diagonal si f(x)=0
    -1 en la diagonal si f(x)=1

    Esta matriz debe ser más grande.
    si hay 3 qubits en el sistema, 
    U_f va a trabajar con un qubit auxiliar extra de f(x)
    Entonces si hay n qubits, la matriz de esta función es de 
    shape(2^{n+1},2^{n+1})?

    Args:
        N (int): El número de estados
        f (Callable): _description_

    Returns:
        ndarray: _description_
    """
    # Define data, row indices, and column indices for non-zero elements
    data = list(-1 if f(x) else 1 for x in range(N) )

    # Create a sparse CSC matrix
    #A_f = sp.csc_matrix((data, (row_indices, col_indices)), shape=(N,N))

    A_f = np.diag(data)
    op_deets(A_f, "A_f")
    U_f = np.kron(A_f,np.eye(2))
    # Kronecker products crea submatrices, esto reshapea a matriz
    U_f:ndarray = U_f.reshape(-1, U_f.shape[-1])
    return U_f


def op_deets(op: ndarray, label:str):
    print()
    print(label)
    print(op.shape)
    #print("norm:", np.linalg.norm(op, ord=np.inf))
    print(op)
    print()
    print()
    


def dag(A: ndarray):
    return np.conj(A.T)


def are_approximate(A, B) -> bool:
    """Are two matrices approximately equal with a tolerance

    Args:
        A (ndarray)
        B (ndarray):

    Returns:
        bool: true when the element-wise difference is lower than the tolerance threshold
    """
    tol = 1e-11  # Tolerance threshold
    #print(f"{tol:.11f}")
    # Element-wise absolute difference
    diff = np.abs(A - B)

    # Check if all elements are within tolerance (boolean mask)
    is_approx = np.all(diff <= tol)
    if is_approx:
        return True
    return False


def is_op_unitary(A, N):
    case1 = dag(A) @ A
    case2 = A @ dag(A)
    assert are_approximate(case1, case2) and are_approximate(case2, np.eye(N))


def test_ops(n, N, f):
    print(f"Qubits n: {n}, Estados totales N : {N}")
    H = H_otimes_n(n)
    is_op_unitary(H, N)
    # Hadamard además de unitaria, es Hermitian?
    assert are_approximate(H,dag(H))
    label = "Hadamard"
    op_deets(H, label)
    U_0n = proyection_about_mean(N)
    is_op_unitary(U_0n, N)
    label ="Proyection about mean:"
    op_deets(U_0n, label)
    # P_I es una función oráculo
    P_I = phase_inversion(N, f)
    is_op_unitary(P_I, N*2)
    label = "Phase inversion:"
    op_deets(P_I, label)


# %%
def grover(N: int, f: Callable):
    """Función donde se implementa Grover's Algorithm

    Args:
        N (int): numero de estados
        f (Callable): función que toma estados y dice si son x* o no
    """
    n = ceil(log(N, 2))   # Numero de qubits
    N = 2**n  # CAMBIANDO EL NUMERO DE ESTADOS; FIGHT ME o FIXME
    test_ops(n, 2**n, f)
    psi_0 = np.ones((N, 1))
    # Hacer el auxiliar

    print("psi_0:")
    print(psi_0)

    psi_i = H_otimes_n(n) @ psi_0  # inicialization
    
    print("psi_1:")
    print(psi_i)

    # sqrt(n) iteraciones
    for _ in range(int(sqrt(N)) + 1):
        # Phase Inversion
        psi_i = np.resize(psi_i,(2*N,1))
        psi_i = phase_inversion(N, f) @ psi_i
        print("psi_i:")
        print(psi_i)
        psi_i = np.resize(psi_i,(N,1))
        print("psi_i:")
        print(psi_i)
        # Proyection about mean
        psi_i = H_otimes_n(n) @ psi_i
        psi_i = proyection_about_mean(N) @ psi_i
        psi_i = H_otimes_n(n) @ psi_i
    print("psi_i:")
    print(psi_i)


# %%
N = 4


def f(x:int)->bool:
    """Función binaria de input a la función oráculo.
    Se supone que si la conozco pues medio ya se donde está lo que busco.

    A partir de esta función se genera la matriz U_f.

    Debe cumplir: f:{0,1}^n -> {0,1} por lo que hay 2^(2^N) 
    versiones diferentes de f


    Args:
        x (int): estado del sistema cuantico que puede o no ser el buscado

    Returns:
        int: binario que dice si esto es el estado buscado o no
    """
    return (x-1)%4==0


grover(N, f)

# TODO hacer phase inversion, como sparse matrix de ser posible
# TODO hacer el qubit auxiliar
# TODO hacer shots en esta vaina
# TODO print con LaTex? 

# %%
