import numpy as np

class NotFullRankError(Exception):
    pass

def solve(bitstrings: list[str]) -> str:
    # bitstrings = [np.array([int(x) for x in s], dtype=bool) for s in bitstrings]
    matrix = np.vstack([np.array([int(x) for x in s], dtype=bool) for s in bitstrings])

    # Check if there are n - 1 equations and whether the nil vector is among them
    if not matrix.any(axis=1).all() or matrix.shape[0] != matrix.shape[1] - 1:
        raise NotFullRankError()

    # Reduce
    for i in range(matrix.shape[0] - 1):
        mask = matrix[i:, i]
        matrix[i:] = np.vstack((matrix[i:][mask], matrix[i:][~mask]))
        matrix[i + 1:i + mask.sum()] ^= matrix[i]

        # Check if the equations were linearly independent
        if not matrix.any(axis=1).all():
            raise NotFullRankError()

    # Transforming matrix from a ref to a rref
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

if __name__ == '__main__':
    res = solve(['010', '001']) # Compute s
    print(res)