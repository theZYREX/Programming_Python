import numpy as np
from scipy.optimize import linprog

N = 11
m = 10 * N

c = np.array([-(2 * i**2 - 4 * i + 5) for i in range(1, m + 1)], dtype=float)

A_ub = []
b_ub = []

for i in range(m - 2):
    row = np.zeros(m)
    row[i] = 1
    row[i + 1] = 3
    row[i + 2] = -2
    A_ub.append(row)
    b_ub.append(100)

for i in range(m - 2):
    row = np.zeros(m)
    row[i] = -1
    row[1] += -2
    A_ub.append(row)
    b_ub.append(-1)

A_ub = np.array(A_ub)
b_ub = np.array(b_ub)

A_eq = np.ones((1, m))
b_eq = np.array([200.0])


bounds = [(0, None) for _ in range(m)]

res = linprog(
    c=c,
    A_ub=A_ub,
    b_ub=b_ub,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method='highs'
)


if res.success:
    print("Оптимальное решение найдено.")
    print("Максимум целевой функции =", -res.fun)
    print("Значения x:")
    for i, val in enumerate(res.x, start=1):
        print(f"x{i} = {val:.6f}")
else:
    print("Решение не найдено.")
    print(res.message)
