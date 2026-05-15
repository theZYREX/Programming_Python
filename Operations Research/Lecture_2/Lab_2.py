import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import pandas as pd

np.random.seed(7)


num_sources = 2          # количество начальных вершин
num_sinks = 2            # количество конечных вершин
num_layers = 10         # количество промежуточных долей
nodes_per_layer = 3      # вершин в каждой промежуточной доле


current_index = 0

I = list(range(current_index, current_index + num_sources))
current_index += num_sources

layers = []
for i in range(num_layers):
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
            if np.random.rand() < 0.7:
                edges.append((u, v))

for layer_idx in range(len(all_layers) - 1):
    u = np.random.choice(all_layers[layer_idx])
    v = np.random.choice(all_layers[layer_idx + 1])
    edges.append((u, v))

G.add_edges_from(edges)

edges = list(G.edges())
m = len(edges)

d = np.random.randint(5, 20, size=m)

num_vars = m

c = np.zeros(num_vars)
for k, (i, j) in enumerate(edges):
    if j in J:
        c[k] = -1

A_eq = []
b_eq = []

for v in range(n):
    if v not in I and v not in J:
        row = np.zeros(num_vars)
        for k, (i, j) in enumerate(edges):
            if j == v:
                row[k] = 1
            if i == v:
                row[k] -= 1
        A_eq.append(row)
        b_eq.append(0)

A_eq = np.array(A_eq, dtype=float) if A_eq else None
b_eq = np.array(b_eq, dtype=float) if b_eq else None

bounds = [(0, d[k]) for k in range(num_vars)]

res = linprog(
    c=c,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method="highs"
)

if res.success:
    x = res.x
    print("Максимальный поток:", -res.fun)

    if x is not None:
        X_matrix = np.zeros((n, n))
        for k, (i, j) in enumerate(edges):
            X_matrix[i, j] = round(x[k], 4)

        labels = [f"V{i}" for i in range(n)]

        X_df = pd.DataFrame(X_matrix, index=labels, columns=labels)

        print("\nМатрица взвешенных сетей:")
        print(X_df)
else:
    print("Решение не найдено")
    x = None

#Визуализация

# ---------- Позиции вершин по долям ----------
pos = {}

x_spacing = 2
y_spacing = 1

all_layers = [I] + layers + [J]

for layer_idx, layer in enumerate(all_layers):
    x_coord = layer_idx * x_spacing
    for node_idx, node in enumerate(layer):
        y_coord = -node_idx * y_spacing
        pos[node] = (x_coord, y_coord)

#Цвета
node_colors = []
for node in G.nodes():
    if node in I:
        node_colors.append("lightgreen")
    elif node in J:
        node_colors.append("lightcoral")
    else:
        node_colors.append("lightblue")


fig, axes = plt.subplots(1, 2, figsize=(18, 7))

#Исходный граф
nx.draw(
    G,
    pos,
    ax=axes[0],
    with_labels=True,
    node_color=node_colors,
    node_size=900,
    arrows=True
)

edge_labels = {(i, j): d[k] for k, (i, j) in enumerate(edges)}
nx.draw_networkx_edge_labels(G, pos, ax=axes[0], edge_labels=edge_labels)

axes[0].set_title("Исходный граф\n(пропускные способности)")
axes[0].axis("off")


#Граф решения
if x is not None:
    G_sol = nx.DiGraph()
    G_sol.add_nodes_from(G.nodes())

    for k, (i, j) in enumerate(edges):
        if x[k] > 1e-6:
            if G.has_edge(i, j):
                G_sol.add_edge(i, j)

    nx.draw(
        G_sol,
        pos,
        ax=axes[1],
        with_labels=True,
        node_color=node_colors,
        node_size=900,
        arrows=True
    )

    edge_labels_sol = {
        (i, j): round(x[k], 2)
        for k, (i, j) in enumerate(edges)
        if x[k] > 1e-6
    }

    nx.draw_networkx_edge_labels(G_sol, pos, ax=axes[1], edge_labels=edge_labels_sol)

    axes[1].set_title("Граф решения\n(объемы потоков)")
else:
    axes[1].text(0.5, 0.5, "Решение не найдено", ha="center", va="center")
    axes[1].set_title("Подграф решения")

axes[1].axis("off")

plt.tight_layout()
plt.show()
