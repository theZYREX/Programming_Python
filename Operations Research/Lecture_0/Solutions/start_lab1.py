import numpy as np
from scipy.optimize import linprog

c = [4, -1, 1]

A_ub = [[2, 3, -3]]
b_ub = [1]

A_eq = [
    [-4, 1, -2],
    [5, 2, 4]
]
b_eq = [-3, 2]

bounds = [(0, None), (0, None), (0, None)]

result = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

if result.success:
    print(f"Оптимальное решение найдено")
    print(f"\nЗначения переменных:")
    print(f"  x1 = {result.x[0]:.6f}")
    print(f"  x2 = {result.x[1]:.6f}")
    print(f"  x3 = {result.x[2]:.6f}")
    print(f"\nМинимальное значение целевой функции: z = {result.fun:.6f}")
else:
    print(f"Решение не найдено!")
