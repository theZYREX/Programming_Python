import numpy as np
from scipy.optimize import linprog

N = 11
m = 10 * N

num_x = m
num_y = m * m
total_vars = num_x + num_y

def y_index(i, j):
    return num_x + i * m + j

c = np.zeros(total_vars)

for i in range(m):
    c[i] = -1

for i in range(m):
    for j in range(m):
        c[y_index(i, j)] = N


A_ub = []
b_ub = []

for i in range(m - 2):
    row = np.zeros(total_vars)
    row[i] = 1
    row[i + 1] = 2
    row[i + 2] = -1
    A_ub.append(row)
    b_ub.append(100)

for i in range(m):
    for j in range(m):
        row = np.zeros(total_vars)
        row[i] = -1
        row[y_index(i, j)] = 1
        A_ub.append(row)
        b_ub.append(0)

A_ub = np.array(A_ub)
b_ub = np.array(b_ub)


A_eq = np.zeros((1, total_vars))
A_eq[0, :m] = 1
b_eq = np.array([200.0])

bounds = []

for _ in range(m):
    bounds.append((0, None))

for _ in range(m * m):
    bounds.append((0, 1))


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

    x_opt = res.x[:m]
    y_opt = res.x[m:].reshape((m, m))

    print("\nПервые несколько значений x:")
    for i in range(min(10, m)):
        print(f"x{i+1} = {x_opt[i]:.6f}")

    print("\nПервые несколько значений y:")
    for i in range(0, 3):
        for j in range(0, 3):
            print(f"y{i+1}{j+1} = {y_opt[i, j]:.6f}")
else:
    print("Решение не найдено.")
    print(res.message)
