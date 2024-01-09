from sympy import Symbol, Eq, solve, Xor, satisfiable, Not

# s = '01'
# counts = {'00': 523, '10': 501}
s = '11'
counts = {'00': 519, '11': 505}

_n = len(s)
_counts = [[_char for _char in _str] for _str in list(counts.keys())]
_s = [Symbol(f's{i}') for i in range(_n)]

lhs = []
for i in range(_n):
    lhs.append(_s[0]*int(_counts[i][0]))
for j in range(_n):
    for k in range(1, _n):
        lhs[j] = Xor(lhs[j], _s[k]*int(_counts[j][k]))
rhs = 0

res = []
for lhsx in lhs:
    sols = list(satisfiable(Not(lhsx), all_models=True))
    res.append(sols)

for r in res:
    if len(r) > 1:
        print(r)