import numpy as np
import random
from scipy.optimize import linprog
import networkx as nx
import matplotlib.pyplot as plt

random.seed(9)

N = 10


def generate_random_graph(n, density=0.6, weight_range=(1, 10)):
    while True:
        vertices = list(range(n))
        edges = []
        costs = {}

        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < density:
                    edges.append((i, j))
                    costs[(i, j)] = random.randint(*weight_range)

        G = nx.Graph()
        G.add_nodes_from(vertices)
        G.add_edges_from(edges)

        if nx.is_connected(G):
            return vertices, edges, costs


def solve_model(vertices, edges, costs):
    V = vertices
    E = edges
    N = len(V)
    M = len(E)

    idx = 0

    x_idx = {e: idx + k for k, e in enumerate(E)}
    idx += M

    lambda_idx = {i: idx + k for k, i in enumerate(V)}
    idx += N

    y_idx = {i: idx + k for k, i in enumerate(V)}
    idx += N

    z_idx = {i: idx + k for k, i in enumerate(V)}
    idx += N

    f_idx = {}
    for (i, j) in E:
        f_idx[(i, j)] = idx
        f_idx[(j, i)] = idx + 1
        idx += 2

    f0_idx = {i: idx + k for k, i in enumerate(V)}
    idx += N

    total_vars = idx

    c = np.zeros(total_vars)
    for e in E:
        c[x_idx[e]] = costs[e]

    A_eq = []
    b_eq = []
    A_ub = []
    b_ub = []

    # (1) Степени
    for i in V:
        row = np.zeros(total_vars)

        for (u, v) in E:
            if u == i or v == i:
                row[x_idx[(u, v)]] += 1

        row[y_idx[i]] += 1
        row[z_idx[i]] -= 1

        A_eq.append(row)
        b_eq.append(2)

    # (2) Связь с корнем
    for i in V:
        row = np.zeros(total_vars)
        row[z_idx[i]] = 1
        row[lambda_idx[i]] = -N
        A_ub.append(row)
        b_ub.append(0)

    # (3) Количество ребер N-1
    row = np.zeros(total_vars)
    for e in E:
        row[x_idx[e]] = 1
    A_eq.append(row)
    b_eq.append(N - 1)

    # (4) Исходный поток от фиктивного источника
    row = np.zeros(total_vars)
    for i in V:
        row[f0_idx[i]] = 1
    A_eq.append(row)
    b_eq.append(N)

    # (5) Баланс потока
    for i in V:
        row = np.zeros(total_vars)

        for (u, v) in E:
            if v == i:
                row[f_idx[(u, v)]] += 1
            if u == i:
                row[f_idx[(v, u)]] += 1

        row[f0_idx[i]] += 1

        for (u, v) in E:
            if u == i:
                row[f_idx[(u, v)]] -= 1
            if v == i:
                row[f_idx[(v, u)]] -= 1

        A_eq.append(row)
        b_eq.append(1)

    # (6) Поток только по выбранным рёбрам
    for (i, j) in E:
        row = np.zeros(total_vars)
        row[f_idx[(i, j)]] = 1
        row[x_idx[(i, j)]] = -N
        A_ub.append(row)
        b_ub.append(0)

        row = np.zeros(total_vars)
        row[f_idx[(j, i)]] = 1
        row[x_idx[(i, j)]] = -N
        A_ub.append(row)
        b_ub.append(0)

    # (7) Поток от источника только в корни
    for i in V:
        row = np.zeros(total_vars)
        row[f0_idx[i]] = 1
        row[lambda_idx[i]] = -N
        A_ub.append(row)
        b_ub.append(0)

    bounds = []

    for _ in range(M):
        bounds.append((0, 1))

    for _ in range(N):
        bounds.append((0, 1))

    for _ in range(N):
        bounds.append((0, 1))

    for _ in range(N):
        bounds.append((0, None))

    for _ in range(2 * M):
        bounds.append((0, None))

    for _ in range(N):
        bounds.append((0, None))

    res = linprog(
        c,
        A_ub=np.array(A_ub),
        b_ub=np.array(b_ub),
        A_eq=np.array(A_eq),
        b_eq=np.array(b_eq),
        bounds=bounds,
        method="highs"
    )

    if not res.success:
        print("Решение не найдено")
        return None

    x_solution = res.x[:M]
    chosen_edges = [E[k] for k in range(M) if x_solution[k] > 0.5]

    lambda_values = res.x[M:M + N]
    y_values = res.x[M + N:M + 2 * N]

    roots = [V[i] for i in range(N) if lambda_values[i] > 0.5]
    leaves = [V[i] for i in range(N) if y_values[i] > 0.5]

    return chosen_edges, res.fun, roots, leaves


# Визуализация

def visualize_side_by_side(vertices, edges, costs,
                           chosen_edges, total_cost,
                           roots, leaves):

    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(15, 7))

    node_colors = []
    for v in vertices:
        if v in roots:
            node_colors.append("green")
        elif v in leaves:
            node_colors.append("skyblue")
        else:
            node_colors.append("lightgray")

    # Исходный граф
    plt.subplot(1, 2, 1)
    nx.draw(G, pos,
            with_labels=True,
            node_color=node_colors,
            edge_color="black",
            node_size=900)

    edge_labels = {(i, j): costs[(i, j)] for (i, j) in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Исходный граф")

    # Найденное дерево
    plt.subplot(1, 2, 2)
    nx.draw(G, pos,
            with_labels=True,
            node_color=node_colors,
            edge_color="lightgray",
            node_size=900)

    nx.draw_networkx_edges(G, pos,
                           edgelist=chosen_edges,
                           width=4,
                           edge_color="red")

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(f"Найденное дерево\nСтоимость = {round(total_cost, 2)}")

    from matplotlib.lines import Line2D

    legend_elements = [
        Line2D([0], [0], color='black', lw=2, label='Исходные рёбра'),
        Line2D([0], [0], color='red', lw=3, label='Рёбра дерева'),
        Line2D([0], [0], marker='o', color='w',
               markerfacecolor='green', markersize=12,
               label='Корни')
    ]

    plt.legend(handles=legend_elements,
               loc='lower center',
               bbox_to_anchor=(-0.05, -0.15),
               ncol=3)

    plt.tight_layout()
    plt.show()


vertices, edges, costs = generate_random_graph(N)

result = solve_model(vertices, edges, costs)

if result:
    chosen_edges, value, roots, leaves = result
    print("Выбранные рёбра:", chosen_edges)
    print("Минимальная стоимость:", value)

    visualize_side_by_side(vertices, edges, costs,
                           chosen_edges, value,
                           roots, leaves)
