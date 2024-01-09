from qiskit import Aer, execute

from collections import Counter
import numpy as np

from src.simon import Simon
from src.utils import draw, y_dot_s, post_processing

def main(n:int, n_samples:int) -> None:
    ## init
    SECRET_STR = [format(i, f'0{NUM}b') for i in range(2**NUM)]
    s = np.random.choice(SECRET_STR)
    root = []

    ## circuit
    qc = Simon(n, s)
    qc.build()

    ## main
    backend = Aer.get_backend('qasm_simulator')
    for _ in range(n_samples):
        flag = False  # check if we have a linearly independent set of measures
        while not flag:

            ## compute
            data = []
            for _ in range(n - 1):
                counts = execute(qc, backend, shots=1).result().get_counts()
                data.append(np.array([bit for bit in list(counts.keys())[0]], dtype=np.int8))

            ## solve
            flag = post_processing(root, data)

    ## count freq
    freqs = Counter(root)
    most_common = freqs.most_common(1)[0]

    ## draw qc
    diagram = draw(qc)

    ## print
    print(f'Secret string = \'{s}\'')
    print(diagram)
    print(f'Most common answer was : {most_common[0]}')
    print(f'Count: {most_common[1]}')

    ## check y dot s = 0 (mod 2) ?
    # for y in counts:
    #     print( f'{s} ⋅ {y} = {y_dot_s(s, y)} (mod 2)')

if __name__ == '__main__':
    NUM = 8
    NUM_SAMPLES = 100
    main(NUM, NUM_SAMPLES)