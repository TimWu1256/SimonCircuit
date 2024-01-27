from qiskit import Aer, execute
from qiskit.visualization import plot_histogram

from collections import Counter
import numpy as np

import argparse

from src.simon import Simon
from src.utils import post_processing

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--secret', type=str, help='Secret string')
    parser.add_argument('-l', '--length', type=int, help='Length of secret string', default='8')
    parser.add_argument('-n', '--samples', type=int, help='Number of samples', default=100)

    args = parser.parse_args()
    if args.secret:
        args.length = 0

    return parser

def main() -> None:
    ## init
    args = parser().parse_args()
    NUM_SAMPLES = args.samples
    if args.secret:
        S = args.secret
        NUM = len(S)
    elif args.length:
        NUM = args.length
        SECRET_STR = [format(i, f'0{NUM}b') for i in range(2**NUM)]
        S = np.random.choice(SECRET_STR)
    root = []
    one_to_one_flag = False

    ## pre-processing
    if '1' not in S:
        one_to_one_flag = True

    ## circuit
    qc = Simon(NUM, S)
    qc.build()

    ## main
    backend = Aer.get_backend('qasm_simulator')
    for _ in range(NUM_SAMPLES):
        flag = False  # check if we have a linearly independent set of measures
        while not flag:

            ## compute
            data = []
            for _ in range(NUM - 1):
                counts = execute(qc, backend, shots=1).result().get_counts()
                data.append(np.array([bit for bit in list(counts.keys())[0]], dtype=np.int8))

            ## solve
            flag = post_processing(root, data)

    ## count freq
    freqs = Counter(root)
    most_common = freqs.most_common(1)[0]

    ## draw qc
    # qc = transpile(qc, optimization_level=0)
    diagram = qc.draw_text()
    # qc.draw_mpl(f'figs/simon_{NUM*2}.png')
    # plot_histogram(freqs, figsize=(7, 7), filename='figs/simon_hist.png')

    ## print
    print(diagram)
    print(f'Secret string = \'{S}\'')
    if one_to_one_flag:
        print('It\'s one-to-one mapping!')
    else:
        print('It\'s two-to-one mapping!')
        print(f'Most common answer was : {most_common[0]}')
        print(f'Count: {most_common[1]}/{NUM_SAMPLES}')

if __name__ == '__main__':
    main()