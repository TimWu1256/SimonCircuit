from qiskit.visualization import circuit_drawer

def solve_s(counts, s):
    pass

def y_dot_s(s, y):
    accum = 0
    for i in range(len(s)):
        accum += int(s[i]) * int(y[i])
    return (accum % 2)

def draw(qc):
    return circuit_drawer(qc, output='text')