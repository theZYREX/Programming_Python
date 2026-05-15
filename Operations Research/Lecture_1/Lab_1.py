import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from scipy.optimize import linprog

np.random.seed(9)

m = 4
n = 5

def generate_connected_bipartite_graph(m, n, edge_prob=0.4):
    while True:
        adjacency = np.zeros((m, n), dtype=int)

        for i in range(m):
            for j in range(n):
                if np.random.rand() < edge_prob:
                    adjacency[i, j] = 1

        for i in range(m):
            if adjacency[i].sum() == 0:
                j = np.random.randint(0, n)
                adjacency[i, j] = 1

        for j in range(n):
            if adjacency[:, j].sum() == 0:
                i = np.random.randint(0, m)
                adjacency[i, j] = 1

        G = nx.Graph()
        left_nodes = [f"A{i+1}" for i in range(m)]
        right_nodes = [f"B{j+1}" for j in range(n)]
        G.add_nodes_from(left_nodes)
        G.add_nodes_from(right_nodes)

        for i in range(m):
            for j in range(n):
                if adjacency[i, j] == 1:
                    G.add_edge(f"A{i+1}", f"B{j+1}")

        if nx.is_connected(G):
            return adjacency

adjacency = generate_connected_bipartite_graph(m, n)

supply = np.random.randint(20, 50, size=m)
demand = np.random.randint(15, 45, size=n)

cost = np.zeros((m, n), dtype=int)
for i in range(m):
    for j in range(n):
        if adjacency[i, j] == 1:
            cost[i, j] = np.random.randint(1, 20)

print("Предложение:", supply)
print("Спрос:", demand)
print("Матрица смежности:")
print(adjacency)
print("Матрица стоимостей:")
print(cost)

total_supply = supply.sum()
total_demand = demand.sum()

print("\nСуммарное предложение:", total_supply)
print("Суммарный спрос:", total_demand)

num_vars = m * n

def var_index(i, j):
    return i * n + j

var_names = [f"x{i+1}{j+1}" for i in range(m) for j in range(n)]

c = np.array([cost[i, j] for i in range(m) for j in range(n)], dtype=float)

A_eq = []
b_eq = []
A_ub = []
b_ub = []
constraint_names_eq = []
constraint_names_ub = []

if total_supply <= total_demand:
    print("\nСлучай 1: суммарное предложение <= суммарного спроса")

    for i in range(m):
        row = np.zeros(num_vars)
        for j in range(n):
            row[var_index(i, j)] = 1
        A_eq.append(row)
        b_eq.append(supply[i])
        constraint_names_eq.append(f"A{i+1}")

    for j in range(n):
        row = np.zeros(num_vars)
        for i in range(m):
            row[var_index(i, j)] = 1
        A_ub.append(row)
        b_ub.append(demand[j])
        constraint_names_ub.append(f"B{j+1}")

else:
    print("\nСлучай 2: суммарное предложение > суммарного спроса")

    for j in range(n):
        row = np.zeros(num_vars)
        for i in range(m):
            row[var_index(i, j)] = 1
        A_eq.append(row)
        b_eq.append(demand[j])
        constraint_names_eq.append(f"B{j+1}")

    for i in range(m):
        row = np.zeros(num_vars)
        for j in range(n):
            row[var_index(i, j)] = 1
        A_ub.append(row)
        b_ub.append(supply[i])
        constraint_names_ub.append(f"A{i+1}")

A_eq = np.array(A_eq, dtype=float) if A_eq else None
b_eq = np.array(b_eq, dtype=float) if b_eq else None
A_ub = np.array(A_ub, dtype=float) if A_ub else None
b_ub = np.array(b_ub, dtype=float) if b_ub else None

bounds = []
for i in range(m):
    for j in range(n):
        if adjacency[i, j] == 1:
            bounds.append((0, None))
        else:
            bounds.append((0, 0))


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
    x = res.x.reshape(m, n)
    x[np.abs(x) < 1e-9] = 0

    print("\nРешение найдено")
    print("Минимальная стоимость:", res.fun)

    solution_df = pd.DataFrame(
        x,
        index=[f"A{i+1}" for i in range(m)],
        columns=[f"B{j+1}" for j in range(n)]
    )
    print("\nТаблица решения x_ij:")
    print(solution_df)
    print("\n")

else:
    print("\nРешение не найдено")
    print(res.message)
    x = None

# Визуализация

consumer_rows = []
consumer_names = []
for j in range(n):
    row = np.zeros(num_vars, dtype=int)
    for i in range(m):
        row[var_index(i, j)] = 1
    consumer_rows.append(row)
    consumer_names.append(f"j={j+1}")

consumer_table = pd.DataFrame(consumer_rows, index=consumer_names, columns=var_names)

print(consumer_table)


# ---------- Суммы по потребителям ----------
print("\nСуммы по потребителям (j):")

for j in range(n):
    terms = []
    for i in range(m):
        terms.append(f"x{i+1}{j+1}")
    expression = " + ".join(terms)
    print(f"j{j+1}: {expression}")


# ---------- Суммы по поставщикам ----------
print("\nСуммы по поставщикам (i):")

for i in range(m):
    terms = []
    for j in range(n):
        terms.append(f"x{i+1}{j+1}")
    expression = " + ".join(terms)
    print(f"i{i+1}: {expression}")

def draw_graph(ax, adjacency_matrix, labels_matrix, title, supply_vals=None, demand_vals=None):
    G = nx.DiGraph()

    m_g, n_g = adjacency_matrix.shape
    left_nodes = [f"A{i+1}" for i in range(m_g)]
    right_nodes = [f"B{j+1}" for j in range(n_g)]

    G.add_nodes_from(left_nodes, bipartite=0)
    G.add_nodes_from(right_nodes, bipartite=1)

    for i in range(m_g):
        for j in range(n_g):
            if adjacency_matrix[i, j] == 1:
                G.add_edge(f"A{i+1}", f"B{j+1}", label=labels_matrix[i, j])

    pos = {}
    for i, node in enumerate(left_nodes):
        pos[node] = (0, -i)
    for j, node in enumerate(right_nodes):
        pos[node] = (1, -j)

    node_labels = {}
    for i, node in enumerate(left_nodes):
        if supply_vals is not None:
            node_labels[node] = f"{node}\nпредл.={supply_vals[i]}"
        else:
            node_labels[node] = node

    for j, node in enumerate(right_nodes):
        if demand_vals is not None:
            node_labels[node] = f"{node}\nспрос={demand_vals[j]}"
        else:
            node_labels[node] = node

    nx.draw(
        G, pos, ax=ax,
        with_labels=False,
        node_size=2200,
        node_color="lightblue",
        edge_color="black",
        arrows=True
    )

    nx.draw_networkx_labels(G, pos, ax=ax, labels=node_labels, font_size=12)

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=edge_labels, font_size=11)

    ax.set_title(title, fontsize=14)
    ax.axis("off")

if x is not None:
    adjacency_solution = (x > 1e-9).astype(int)
    labels_solution = np.empty_like(x, dtype=object)

    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] > 1e-9:
                labels_solution[i, j] = round(x[i, j], 2)
            else:
                labels_solution[i, j] = ""
else:
    adjacency_solution = np.zeros_like(adjacency)
    labels_solution = np.empty_like(adjacency, dtype=object)
    labels_solution[:] = ""

labels_cost = np.empty_like(cost, dtype=object)
for i in range(cost.shape[0]):
    for j in range(cost.shape[1]):
        if adjacency[i, j] == 1:
            labels_cost[i, j] = int(cost[i, j])
        else:
            labels_cost[i, j] = ""

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

draw_graph(
    axes[0],
    adjacency,
    labels_cost,
    "Исходный граф (стоимости перевозки)",
    supply_vals=supply,
    demand_vals=demand
)

if x is not None:
    draw_graph(
        axes[1],
        adjacency_solution,
        labels_solution,
        "Граф решения (объемы перевозки)",
        supply_vals=supply,
        demand_vals=demand
    )
else:
    axes[1].set_title("Граф решения")
    axes[1].text(0.5, 0.5, "Решение не найдено", ha="center", va="center")
    axes[1].axis("off")

plt.tight_layout()
plt.show()
