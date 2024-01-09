from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

class Simon(QuantumCircuit):
    def __init__(self, n, s):
        _qr = QuantumRegister(2*n)
        _cr = ClassicalRegister(n)
        super().__init__(_qr, _cr)
        self.secret_str = s

    """
        https://github.com/qiskit-community/qiskit-textbook/blob/main/qiskit-textbook-src/qiskit_textbook/tools/__init__.py
    """
    def oracle(self):
        """returns a Simon oracle for bitstring s"""
        s = self.secret_str[::-1] # reverse b for easy iteration
        n = len(s)
        ## Do copy; |x>|0> -> |x>|x>
        for q in range(n):
            self.cx(q, q+n)
        if '1' not in s:
            return  # 1:1 mapping, so just exit
        i = s.find('1') # index of first non-zero bit in b
        ## Do |x> -> |s.x> on condition that q_i is 1
        for q in range(n):
            if s[q] == '1':
                self.cx(i, (q)+n)

    def build(self):
        n = self.num_qubits
        _qr = self.qregs[0]
        _cr = self.cregs[0]

        ## hadamard
        for i in range(n//2):
            self.h(_qr[i])
        self.barrier()

        ## simon's oracle
        self.oracle()
        self.barrier()

        ## hadamard
        for i in range(n//2):
            self.h(_qr[i])
        self.barrier()

        ## measure
        for i in range(n//2):
            self.measure(_qr[i], _cr[i])