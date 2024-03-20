import numpy as np

"""___________Gaussian Elimination with Partial Pivoting___________"""

def pp_backward_substitution(A, b):
    n = len(A)
    x = np.zeros(n)
    for i in reversed(range(n)):
        x[i] = (b[i] - np.dot(A[i, i+1:], x[i+1:])) / A[i, i]
    return x

def gaussian_elimination_partial_pivot(A, b, epsilon):
    n = len(A)
    for k in range(n-1):
        i_max = np.abs(A[k:, k]).argmax() + k
        if abs(A[i_max, k]) < epsilon:
            raise ValueError("Tolerance reached.")
        A[[k, i_max]] = A[[i_max, k]]
        b[[k, i_max]] = b[[i_max, k]]
        for i in range(k+1, n):
            factor = A[i, k]/A[k, k]
            A[i, k:] -= factor * A[k, k:]
            b[i] -= factor * b[k]
    x = pp_backward_substitution(A, b)
    return x

"""___________Gaussian Elimination with Rook Pivoting___________"""

def rp_forward_elimination(F, c, n, epsilon):
    for k in range(n):
        # Search for maximum element in the current column (including row k)
        max_index = k + np.argmax(np.abs(F[k:, k])) 
        max_val = np.abs(F[max_index, k])
        
        # Swap rows if necessary to bring the pivot to the diagonal
        if max_index != k:
            F[[k, max_index]] = F[[max_index, k]]
            c[[k, max_index]] = c[[max_index, k]]
        
        # Check if the maximum element is below epsilon
        if max_val < epsilon:
            print("Pivot element is less than defined epsilon.")
            return None
        
        # Gaussian elimination
        pivot_row = F[k, k:].copy()
        for i in range(k+1, n):
            factor = F[i, k] / pivot_row[0]
            F[i, k:] -= factor * pivot_row
            c[i] -= factor * c[k]

def rp_backward_substitution(F, c, x, n):
    for i in range(n-1, -1, -1):
        x[i] = (c[i] - np.dot(F[i, i+1:], x[i+1:])) / F[i, i]

def gaussian_elimination_rook_pivot(A, b, epsilon):
    n = len(b)
    x = np.zeros(n)
    c = np.copy(b)
    F = np.copy(A)
    
    rp_forward_elimination(F, c, n, epsilon)
    rp_backward_substitution(F, c, x, n)

    return x

"""___________Gaussian Elimination with Complete Pivoting___________"""

def gaussian_elimination_complete_pivot(A, b, epsilon):
    n = len(b)
    x = np.zeros(n)
    P = np.eye(n)  # Permutation matrix
    e = np.copy(b)
    G = np.copy(A)

    result = complete_pivot_forward_elimination(P, G, e, epsilon)
    if result is None:
        return None
    else:
        P, G, e = result

    # Perform backward substitution
    x = cp_backward_substitution(G, e)

    # Apply permutation to the solution
    x = np.dot(P.T, x)

    return x

def complete_pivot_forward_elimination(P, G, e, epsilon):
    n = len(e)
    for k in range(n):
        # Find index of maximum element in the remaining submatrix
        max_indices = np.unravel_index(np.abs(G[k:, k:]).argmax(), (n - k, n - k))
        max_index_row, max_index_col = max_indices[0] + k, max_indices[1] + k

        # Check if the maximum element is below epsilon
        if np.abs(G[max_index_row, max_index_col]) < epsilon:
            return None

        # Swap rows if necessary
        if max_index_row != k:
            G[[k, max_index_row]] = G[[max_index_row, k]]
            P[[k, max_index_row]] = P[[max_index_row, k]]
            e[[k, max_index_row]] = e[[max_index_row, k]]

        # Swap columns if necessary
        if max_index_col != k:
            G[:, [k, max_index_col]] = G[:, [max_index_col, k]]

        # Perform elimination
        factors = G[k+1:, k] / G[k, k]
        factors = factors.reshape(-1, 1)  # Reshape factors to match e[k+1:]
        G[k+1:, k:] -= factors * G[k, k:]
        e[k+1:] -= factors * e[k]

    return P, G, e

def cp_backward_substitution(G, e):
    n = len(e)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (e[i] - np.dot(G[i, i + 1:], x[i + 1:])) / G[i, i]
    return x

"""___________Gaussian Elimination with pivoting using Cholesky Factorization___________"""

def N_cholesky_pivot(A, epsilon):
    n = len(A)
    L = np.zeros((n, n))
    P = np.identity(n)
    for i in range(n):
        # Find index of maximum element in the ith column
        max_index = i + np.argmax(np.abs(A[i:, i]))
        max_val = np.abs(A[max_index, i])
        if max_val < epsilon:
            print("Pivot element below tolerance.")
            return None, None
        if i != max_index:
            # Swap rows in A and P
            A[[i, max_index]] = A[[max_index, i]]
            P[[i, max_index]] = P[[max_index, i]]
            L[[i, max_index], :i] = L[[max_index, i], :i]
        L[i, i] = np.sqrt(A[i, i] - np.sum(L[i, :i]**2))
        for j in range(i+1, n):
            L[j, i] = (A[j, i] - np.dot(L[j, :i], L[i, :i])) / L[i, i]
    return L, P

def gaussian_elimination_cholesky_pivot(A, b, epsilon):
    L, P = N_cholesky_pivot(A, epsilon)
    n = len(A)
    # Solve Ly = Pb using forward substitution
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]
    # Solve L^T x = y using backward substitution
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = (y[i] - np.dot(L[i+1:, i], x[i+1:])) / L[i, i]
    return x