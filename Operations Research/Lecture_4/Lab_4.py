# tema4_dynamic.py

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import milp, LinearConstraint, Bounds
import pandas as pd

np.random.seed(12)

K = 3      # типов продукции
L = 2      # типов сырья
M_days = 4 # горизонт планирования

# структура графа
num_layers = 2
nodes_per_layer = 3
num_sources = 1
num_sinks = 1

# Граф

current_index = 0
I = list(range(current_index, current_index + num_sources))
current_index += num_sources

layers = []
for _ in range(num_layers):
    layer_nodes = list(range(current_index, current_index + nodes_per_layer))
    layers.append(layer_nodes)
    current_index += nodes_per_layer

J = list(range(current_index, current_index + num_sinks))
current_index += num_sinks

n = current_index

G = nx.DiGraph()
G.add_nodes_from(range(n))

edges = []
all_layers = [I] + layers + [J]

for layer_idx in range(len(all_layers) - 1):
    for u in all_layers[layer_idx]:
        for v in all_layers[layer_idx + 1]:
            if np.random.rand() < 0.8:
                edges.append((u, v))

for layer_idx in range(len(all_layers) - 1):
    u = np.random.choice(all_layers[layer_idx])
    v = np.random.choice(all_layers[layer_idx + 1])
    edges.append((u, v))

G.add_edges_from(edges)
edges = list(G.edges())
E = len(edges)

# Генерация параметров

p = np.random.randint(20, 50, size=(K, M_days))
b0 = np.random.randint(50, 80, size=L)
A = np.random.randint(1, 5, size=(L, K))
gamma = np.random.randint(5, 15, size=(L, M_days))
Q = np.random.randint(10, 40, size=K)

c = np.random.randint(3, 10, size=E)
d = np.random.randint(20, 60, size=E)

M_big = max(d)

print("\n================ ПАРАМЕТРЫ  ================\n")

print("K - количество типов товаров =", K)
print("L - количество типов сырья =", L)
print("m - Горизонт планирования", M_days)

print("\np_k - цена реализации товара типа k:")
for k in range(K):
    print(f"p_{k+1} =", p[k])

print("\nb_l - запас сырья типа l:")
for l in range(L):
    print(f"b_{l+1} =", b0[l])

print("\nA_lk - норма расхода сырья l на единицу товара k:")
for l in range(L):
    for k in range(K):
        print(f"A_{l+1}{k+1} =", A[l, k])
    print()

print("Q_k - спрос на товар типа k:")
for k in range(K):
    print(f"Q_{k+1} =", Q[k])

print("\nd_ij - пропускная способность дуги i → j:")
for e, (i, j) in enumerate(edges):
    print(f"d_{i}->{j} =", d[e])

print("\nc_ij - тариф перевозки по дуге i → j:")
for e, (i, j) in enumerate(edges):
    print(f"c_{i}->{j} =", c[e])

num_vars = K*M_days + E + E + L*M_days

def idx_x(k,m):
    return k*M_days + m

def idx_z(e):
    return K*M_days + e

def idx_l(e):
    return K*M_days + E + e

def idx_b(l,m):
    return K*M_days + 2*E + l*M_days + m

c_obj = np.zeros(num_vars)

for k in range(K):
    for m in range(M_days):
        c_obj[idx_x(k,m)] = -p[k,m]

for e in range(E):
    c_obj[idx_l(e)] = c[e]

A_list = []
lb = []
ub = []

#сырье каждый день
for l in range(L):
    for m in range(M_days):
        row = np.zeros(num_vars)
        for k in range(K):
            row[idx_x(k,m)] = A[l,k]
        row[idx_b(l,m)] = -1
        A_list.append(row)
        lb.append(-np.inf)
        ub.append(0)

#вывоз
row = np.zeros(num_vars)
for k in range(K):
    for m in range(M_days):
        row[idx_x(k,m)] = 1
for e,(i,j) in enumerate(edges):
    if i in I:
        row[idx_z(e)] -= 1
A_list.append(row)
lb.append(0)
ub.append(0)

# (4) сохранение потока
for v in range(n):
    if v not in I and v not in J:
        row = np.zeros(num_vars)
        for e,(i,j) in enumerate(edges):
            if j==v: row[idx_z(e)] += 1
            if i==v: row[idx_z(e)] -= 1
        A_list.append(row)
        lb.append(0)
        ub.append(0)

# (5) спрос
for k in range(K):
    row = np.zeros(num_vars)
    for m in range(M_days):
        row[idx_x(k,m)] = 1
    A_list.append(row)
    lb.append(0)
    ub.append(Q[k])

# (6) пропускная
for e in range(E):
    row = np.zeros(num_vars)
    row[idx_z(e)] = 1
    A_list.append(row)
    lb.append(0)
    ub.append(d[e])

# (7) Big-M
for e in range(E):
    row = np.zeros(num_vars)
    row[idx_z(e)] = 1
    row[idx_l(e)] = -M_big
    A_list.append(row)
    lb.append(-np.inf)
    ub.append(0)

# (12) динамика склада
for l in range(L):
    for m in range(M_days-1):
        row = np.zeros(num_vars)
        row[idx_b(l,m+1)] = 1
        row[idx_b(l,m)] = -1
        for k in range(K):
            row[idx_x(k,m)] = A[l,k]
        A_list.append(row)
        lb.append(gamma[l,m])
        ub.append(gamma[l,m])

A_matrix = np.array(A_list)
constraints = LinearConstraint(A_matrix, lb, ub)

# bounds
lower = np.zeros(num_vars)
upper = np.full(num_vars, np.inf)

for k in range(K):
    for m in range(M_days):
        upper[idx_x(k,m)] = Q[k]

for e in range(E):
    upper[idx_z(e)] = d[e]
    upper[idx_l(e)] = 1

bounds = Bounds(lower, upper)

integrality = np.ones(num_vars)

# ==========================================================
# РЕШЕНИЕ
# ==========================================================

res = milp(c=c_obj, constraints=constraints,
           bounds=bounds, integrality=integrality)

if not res.success:
    print("Нет решения")
    exit()

x_sol = res.x

print("\nМаксимальная прибыль =", -res.fun)

# ==========================================================
# ГРАФИКИ
# ==========================================================

# ==========================================================
# ВИЗУАЛИЗАЦИЯ КАК В ПРЕДЫДУЩЕЙ ЗАДАЧЕ
# ==========================================================

# позиции по долям
pos = {}
x_spacing = 2
y_spacing = 1

for layer_idx, layer in enumerate(all_layers):
    for node_idx, node in enumerate(layer):
        pos[node] = (layer_idx * x_spacing,
                     -node_idx * y_spacing)

# цвета вершин
node_colors = []
for node in G.nodes():
    if node in I:
        node_colors.append("lightgreen")
    elif node in J:
        node_colors.append("lightcoral")
    else:
        node_colors.append("lightblue")

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# ---------- Исходный граф ----------
nx.draw(G, pos,
        ax=axes[0],
        with_labels=True,
        node_color=node_colors,
        node_size=900,
        arrows=True)

edge_labels = {(i, j): d[e] for e, (i, j) in enumerate(edges)}
nx.draw_networkx_edge_labels(G, pos,
                             ax=axes[0],
                             edge_labels=edge_labels)

axes[0].set_title("Исходный транспортный граф\n(пропускные способности d_ij)")
axes[0].axis("off")

# ---------- Граф решения ----------
G_sol = nx.DiGraph()
G_sol.add_nodes_from(G.nodes())

for e, (i, j) in enumerate(edges):
    flow = x_sol[idx_z(e)]
    if flow > 1e-6:
        G_sol.add_edge(i, j)

nx.draw(G_sol, pos,
        ax=axes[1],
        with_labels=True,
        node_color=node_colors,
        node_size=900,
        arrows=True)

edge_labels_sol = {
    (i, j): int(x_sol[idx_z(e)])
    for e, (i, j) in enumerate(edges)
    if x_sol[idx_z(e)] > 1e-6
}

nx.draw_networkx_edge_labels(G_sol, pos,
                             ax=axes[1],
                             edge_labels=edge_labels_sol)

axes[1].set_title("Граф решения\n(объемы перевозок z_ij)")
axes[1].axis("off")

plt.tight_layout()
plt.show()
# 3 b_lm
plt.figure()
for l in range(L):
    b_vals=[x_sol[idx_b(l,m)] for m in range(M_days)]
    plt.plot(range(M_days),b_vals,label=f"b_{l+1}m")
plt.title("b_lm")
plt.legend()
plt.xlabel("m")
plt.ylabel("b_lm")
plt.show()

# 4 Σ b_lm
plt.figure()
sum_b=[sum(x_sol[idx_b(l,m)] for l in range(L)) for m in range(M_days)]
plt.plot(range(M_days),sum_b)
plt.title("Σ b_lm")
plt.xlabel("m")
plt.ylabel("Σ b_lm")
plt.show()

# 5 x_km
plt.figure()
for k in range(K):
    x_vals=[x_sol[idx_x(k,m)] for m in range(M_days)]
    plt.plot(range(M_days),x_vals,label=f"x_{k+1}m")
plt.title("x_km")
plt.legend()
plt.xlabel("m")
plt.ylabel("x_km")
plt.show()

# 6 Σ_m x_km
plt.figure()
sum_x=[sum(x_sol[idx_x(k,m)] for m in range(M_days)) for k in range(K)]
plt.bar(range(K),sum_x)
plt.title("Σ_m x_km")
plt.xlabel("k")
plt.ylabel("Σ x_km")
plt.show()
