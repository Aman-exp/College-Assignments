import numpy as np

def lu_decomposition(A):
    """
    Perform LU decomposition with partial pivoting.
    Returns the permutation matrix P, the unit lower triangular matrix L,
    and the upper triangular matrix U.
    """
    if A.shape[0] != A.shape[1] or np.linalg.matrix_rank(A) != A.shape[0]:
        raise ValueError("Input matrix A must be a square invertible matrix")

    n = A.shape[0]
    P = np.eye(n)
    L = np.eye(n)
    U = A.copy()

    for k in range(n - 1):
        pivot_row = np.argmax(np.abs(U[k:, k])) + k

        if U[pivot_row, k] == 0:
            raise ValueError("Unable to find nonzero pivot")

        U[[k, pivot_row], k:] = U[[pivot_row, k], k:]
        L[[k, pivot_row], :k] = L[[pivot_row, k], :k]
        P[[k, pivot_row], :] = P[[pivot_row, k], :]

        L[k + 1:, k] = U[k + 1:, k] / U[k, k]
        U[k + 1:, k:] -= np.outer(L[k + 1:, k], U[k, k:])

    return P, L, U

def forward_substitution(L, b):
    """
    Solve the system Ly = b using forward substitution.
    """
    n = L.shape[0]
    y = np.zeros_like(b)

    for i in range(n):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]

    return y

def backward_substitution(U, y):
    """
    Solve the system Ux = y using backward substitution.
    """
    n = U.shape[0]
    x = np.zeros_like(y)

    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

    return x

def lu_solver(A, b):
    """
    Solve the system Ax = b using LU decomposition.
    Returns the permutation matrix P, the unit lower triangular matrix L,
    the upper triangular matrix U, and the solution vector x.
    """
    P, L, U = lu_decomposition(A)

    # Solve Ly = Pb using forward substitution
    y = forward_substitution(L, np.dot(P, b))

    # Solve Ux = y using backward substitution
    x = backward_substitution(U, y)

    return P, L, U, x