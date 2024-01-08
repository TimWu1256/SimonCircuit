from pprint import pprint

from qiskit import Aer, execute

from src.simon import Simon
from src.utils import draw, y_dot_s

def main(n:int, s:str, shots:int=1024) -> None:
    ## circuit
    qc = Simon(n, s)
    qc.build()

    ## compute
    backend = Aer.get_backend('qasm_simulator')
    results = execute(qc, backend, shots=shots).result()
    counts = results.get_counts()

    ## draw
    diagram = draw(qc)

    ## print
    print(diagram)
    print(f'Secret string = \'{s}\'')
    pprint(counts)

    ## y dot s = 0 (mod 2)
    for y in counts:
        print( f'{s} ⋅ {y} = {y_dot_s(s, y)} (mod 2)')

    ## solve s
    # solve_s()

if __name__ == '__main__':
    NUM = 2
    SECRET_STR = [format(i, f'0{NUM}b') for i in range(NUM**2)]
    for s in SECRET_STR:
        main(NUM, s, 1024)
        print('-------------------------------')