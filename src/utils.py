import numpy as np
import scipy as sp

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
        solution = (solution / minval % 2).astype(np.int8)  # renormalize vector mod 2
        root.append(str(solution))
        return flag
