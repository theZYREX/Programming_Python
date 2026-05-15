import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import milp, LinearConstraint, Bounds
import pandas as pd

np.random.seed(10)

num_layers = 2
nodes_per_layer = 3
num_sources = 1
num_sinks = 1

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

K = 3
L = 2

p = np.random.randint(20, 50, size=K)
b = np.random.randint(40, 80, size=L)
A = np.random.randint(1, 5, size=(L, K))
Q = np.random.randint(10, 40, size=K)

c = np.random.randint(3, 10, size=E)
d = np.random.randint(20, 60, size=E)

M = max(d)

print("\n================ ПАРАМЕТРЫ  ================\n")

print("K — количество типов товаров =", K)
print("L — количество типов сырья =", L)

print("\np_k — цена реализации товара типа k:")
for k in range(K):
    print(f"p_{k+1} =", p[k])

print("\nb_l — запас сырья типа l:")
for l in range(L):
    print(f"b_{l+1} =", b[l])

print("\nA_lk — норма расхода сырья l на единицу товара k:")
for l in range(L):
    for k in range(K):
        print(f"A_{l+1}{k+1} =", A[l, k])
    print()

print("Q_k — спрос на товар типа k:")
for k in range(K):
    print(f"Q_{k+1} =", Q[k])

print("\nd_ij — пропускная способность дуги i → j:")
for e, (i, j) in enumerate(edges):
    print(f"d_{i}->{j} =", d[e])

print("\nc_ij — тариф перевозки по дуге i → j:")
for e, (i, j) in enumerate(edges):
    print(f"c_{i}->{j} =", c[e])

num_vars = K + E + E

def idx_x(k): return k
def idx_z(e): return K + e
def idx_l(e): return K + E + e

c_obj = np.zeros(num_vars)

for k in range(K):
    c_obj[idx_x(k)] = -p[k]

for e in range(E):
    c_obj[idx_z(e)] = c[e]

A_list = []
lb = []
ub = []

# Ограничение сырья
for l in range(L):
    row = np.zeros(num_vars)
    for k in range(K):
        row[idx_x(k)] = A[l, k]
    A_list.append(row)
    lb.append(-np.inf)
    ub.append(b[l])

# Всё произведённое вывозится
row = np.zeros(num_vars)
for k in range(K):
    row[idx_x(k)] = 1
for e, (i, j) in enumerate(edges):
    if i in I:
        row[idx_z(e)] -= 1
A_list.append(row)
lb.append(0)
ub.append(0)

# Сохранение потока
for v in range(n):
    if v not in I and v not in J:
        row = np.zeros(num_vars)
        for e, (i, j) in enumerate(edges):
            if j == v:
                row[idx_z(e)] += 1
            if i == v:
                row[idx_z(e)] -= 1
        A_list.append(row)
        lb.append(0)
        ub.append(0)

# Ограничение спроса
for k in range(K):
    row = np.zeros(num_vars)
    row[idx_x(k)] = 1
    A_list.append(row)
    lb.append(0)
    ub.append(Q[k])

# Пропускная способность
for e in range(E):
    row = np.zeros(num_vars)
    row[idx_z(e)] = 1
    A_list.append(row)
    lb.append(0)
    ub.append(d[e])

# Логическое ограничение потока
for e in range(E):
    row = np.zeros(num_vars)
    row[idx_z(e)] = 1
    row[idx_l(e)] = -M
    A_list.append(row)
    lb.append(-np.inf)
    ub.append(0)

A_matrix = np.array(A_list)
constraints = LinearConstraint(A_matrix, lb, ub)

lower_bounds = np.zeros(num_vars)
upper_bounds = np.full(num_vars, np.inf)

for k in range(K):
    upper_bounds[idx_x(k)] = Q[k]

for e in range(E):
    upper_bounds[idx_z(e)] = d[e]
    upper_bounds[idx_l(e)] = 1

bounds = Bounds(lower_bounds, upper_bounds)

integrality = np.ones(num_vars)

res = milp(c=c_obj, constraints=constraints,
           bounds=bounds, integrality=integrality)

if not res.success:
    print("Решение не найдено")
    exit()

x_sol = res.x

print("\n================ РЕЗУЛЬТАТ ================\n")
print("Максимальная прибыль =", -res.fun)

print("\nОбъемы производства:")
for k in range(K):
    print(f"x_{k+1} =", int(x_sol[idx_x(k)]))

print("\nОбъемы перевозок (z_ij):")
for e, (i, j) in enumerate(edges):
    flow = int(x_sol[idx_z(e)])
    if flow > 0:
        print(f"z_{i}->{j} =", flow)

Z_matrix = np.zeros((n, n))

for e, (i, j) in enumerate(edges):
    Z_matrix[i, j] = int(x_sol[idx_z(e)])

print("\nМатрица взвешанных сетей z_ij:")
Z_df = pd.DataFrame(Z_matrix,
                    index=[f"V{i}" for i in range(n)],
                    columns=[f"V{i}" for i in range(n)])
print(Z_df)

# ВИЗУАЛИЗАЦИЯ

pos = {}
x_spacing = 2
y_spacing = 1

for layer_idx, layer in enumerate(all_layers):
    for node_idx, node in enumerate(layer):
        pos[node] = (layer_idx * x_spacing,
                     -node_idx * y_spacing)

node_colors = []
for node in G.nodes():
    if node in I:
        node_colors.append("lightgreen")
    elif node in J:
        node_colors.append("lightcoral")
    else:
        node_colors.append("lightblue")

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

nx.draw(G, pos, ax=axes[0],
        with_labels=True,
        node_color=node_colors,
        node_size=900,
        arrows=True)

axes[0].set_title("Исходный транспортный граф")
axes[0].axis("off")

# ---------- Граф решения ----------
G_sol = nx.DiGraph()
G_sol.add_nodes_from(G.nodes())

for e, (i, j) in enumerate(edges):
    flow = x_sol[idx_z(e)]
    if flow > 1e-6:
        G_sol.add_edge(i, j)

nx.draw(G_sol, pos, ax=axes[1],
        with_labels=True,
        node_color=node_colors,
        node_size=900,
        arrows=True)

# Подписи объёмов перевозок
edge_labels_sol = {
    (i, j): int(x_sol[idx_z(e)])
    for e, (i, j) in enumerate(edges)
    if x_sol[idx_z(e)] > 1e-6
}

nx.draw_networkx_edge_labels(G_sol, pos,
                             ax=axes[1],
                             edge_labels=edge_labels_sol)

axes[1].set_title("Транспортный граф решения\n(объемы перевозок z_ij)")
axes[1].axis("off")

plt.tight_layout()
plt.show()

plt.figure(figsize=(6,4))
plt.bar(range(1, K+1), x_sol[:K])
plt.title("Объемы производства всех видов товаров")
plt.xlabel("Тип товара k")
plt.ylabel("x_k")
plt.show()
