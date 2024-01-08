from pprint import pprint

from qiskit import Aer, execute

from src.simon import Simon
from src.utils import draw, y_dot_s, solve

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
    if 0:
        for y in counts:
            print( f'{s} ⋅ {y} = {y_dot_s(s, y)} (mod 2)')

    ## solve s
    counts_list = [count for count in list(counts.keys()) if not all(c == '0' for c in count)]   # remove all zero counts
    s = solve(counts_list)
    print(f's = {s}')

    ## end
    print('-------------------------------')

if __name__ == '__main__':
    NUM = 2
    SECRET_STR = [format(i, f'0{NUM}b') for i in range(2**NUM)]
    for s in SECRET_STR:
        main(NUM, s)