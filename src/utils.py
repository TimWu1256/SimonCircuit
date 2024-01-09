from qiskit.visualization import circuit_drawer

import numpy as np
import scipy as sp

"""
    https://quantumcomputing.stackexchange.com/questions/29401/implementing-a-gaussian-elimination-solver-for-simons-algorithms-outcome-of-li
"""
def error():
    return 'NotFullRankError!'
def solve(bitstrings: list[str]) -> str:
    matrix = np.vstack([np.array([int(x) for x in s], dtype=bool) for s in bitstrings])

    ## Check if there are n - 1 equations and whether the nil vector is among them
    if not matrix.any(axis=1).all() or matrix.shape[0] != matrix.shape[1] - 1:
        return error()

    ## Reduce
    for i in range(matrix.shape[0] - 1):
        mask = matrix[i:, i]
        matrix[i:] = np.vstack((matrix[i:][mask], matrix[i:][~mask]))
        matrix[i + 1:i + mask.sum()] ^= matrix[i]

        ## Check if the equations were linearly independent
        if not matrix.any(axis=1).all():
            return error()

    ## Transforming matrix from a ref to a rref
    for i in range(1, matrix.shape[0]):
        index = np.where(matrix[i])[0][0]
        mask = matrix[:i, index]
        matrix[:i][mask] ^= matrix[i]

    index = np.where(~np.diag(matrix))[0]

    if index.shape[0]:
        index = index[0]
    else:
        index = matrix.shape[1] - 1

    return "".join(str(x) for x in np.hstack((matrix[:index, index], [1], matrix[index:, index])))

"""
    https://github.com/quantumlib/Cirq/blob/main/examples/simon_algorithm.py
"""
def post_processing(root, data):
    """Solves a system of equations with modulo 2 numbers"""
    sing_values = sp.linalg.svdvals(data)
    tolerance = 1e-5
    if sum(sing_values < tolerance) == 0:  # check if measurements are linearly dependent
        flag = True
        null_space = sp.linalg.null_space(data).T[0]
        solution = np.around(null_space, 3)  # chop very small values
        minval = abs(min(solution[np.nonzero(solution)], key=abs))
        solution = (solution / minval % 2).astype(int)  # renormalize vector mod 2
        root.append(str(solution))
        return flag


def y_dot_s(s, y):
    accum = 0
    for i in range(len(s)):
        accum += int(s[i]) * int(y[i])
    return (accum % 2)

def draw(qc):
    return circuit_drawer(qc, output='text')