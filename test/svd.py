import numpy as np
from qiskit import Aer, QuantumCircuit, transpile, assemble, execute

def post_processing(data, results):
    flag = True  # 預設標誌為 True

    # 取得結果的計數部分
    counts = results.get_counts()

    # 將計數轉換為矩陣形式
    matrix = np.array([[int(bit) for bit in format(int(key, 2), '0b').zfill(len(data[0]))] for key in counts.keys()])

    # 使用奇異值分解計算奇異值
    sing_values = np.linalg.svd(matrix, compute_uv=False)

    tolerance = 1e-5

    if sum(sing_values < tolerance) == 0:  # 檢查是否線性相依
        null_space = np.linalg.null_space(matrix)
        solution = np.around(null_space[:, 0], 3)  # 四捨五入

        # 找到最小絕對值的非零元素
        minval = abs(min(solution[np.nonzero(solution)], key=abs))

        # 將解歸一化為模 2
        solution = (solution / minval % 2).astype(int)

        data.append(str(solution))
    else:
        flag = False  # 如果線性相依，將標誌設為 False

    return flag

# 使用 Aer 的模擬器來執行
backend = Aer.get_backend('qasm_simulator')
shots = 1024

# 假設 simon_circuit 是你的 Simon's algorithm 量子電路
transpiled_simon_circuit = transpile(simon_circuit, backend, optimization_level=3)
qobj = assemble(transpiled_simon_circuit, shots=shots)
job = execute(qobj, backend)
results = job.result()

# 呼叫 post_processing 進行後處理
data = []  # 用來存放結果
flag = post_processing(data, results)

# 打印結果和標誌
print("Data:", data)
print("Flag:", flag)
