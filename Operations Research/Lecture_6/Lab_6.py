import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import milp, LinearConstraint, Bounds

def draw_sudoku(grid, title):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)

    for i in range(10):
        lw = 3 if i % 3 == 0 else 1
        ax.plot([i, i], [0, 9], color='black', linewidth=lw)
        ax.plot([0, 9], [i, i], color='black', linewidth=lw)

    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                ax.text(j + 0.5, 8.5 - i,
                        str(grid[i][j]),
                        ha='center', va='center',
                        fontsize=16)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=14)
    plt.gca().set_aspect('equal')
    plt.show()


def draw_double_6x6(s1, s2):
    board = np.zeros((12, 12), dtype=int)
    board[0:9, 0:9] = s1
    board[3:12, 3:12] = s2

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)

    for i in range(13):
        lw = 3 if i % 3 == 0 else 1
        ax.plot([i, i], [0, 12], color='black', linewidth=lw)
        ax.plot([0, 12], [i, i], color='black', linewidth=lw)

    for i in range(12):
        for j in range(12):
            if board[i][j] != 0:
                ax.text(j + 0.5, 11.5 - i,
                        str(board[i][j]),
                        ha='center', va='center',
                        fontsize=12)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("DOUBLE SUDOKU (6x6)", fontsize=14)
    plt.gca().set_aspect('equal')
    plt.show()


def draw_double_3x3(s1, s2):
    board = np.zeros((15, 15), dtype=int)
    board[0:9, 0:9] = s1
    board[6:15, 6:15] = s2

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 15)

    for i in range(16):
        lw = 3 if i % 3 == 0 else 1
        ax.plot([i, i], [0, 15], color='black', linewidth=lw)
        ax.plot([0, 15], [i, i], color='black', linewidth=lw)

    for i in range(15):
        for j in range(15):
            if board[i][j] != 0:
                ax.text(j + 0.5, 14.5 - i,
                        str(board[i][j]),
                        ha='center', va='center',
                        fontsize=12)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("DOUBLE SUDOKU (3x3)", fontsize=14)
    plt.gca().set_aspect('equal')
    plt.show()


def draw_triple(s1, s2, s3):
    board = np.full((15, 21), -1)

    # S1
    board[0:9, 0:9] = s1

    # S2
    board[0:9, 12:21] = s2

    # S3
    board[6:15, 6:15] = s3

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 15)

    for i in range(15):
        for j in range(21):
            if board[i, j] != -1:
                ax.add_patch(
                    plt.Rectangle(
                        (j, 14 - i),
                        1, 1,
                        fill=False,
                        edgecolor='black',
                        linewidth=1
                    )
                )

    def draw_blocks(x0, y0):
        for k in range(0, 10, 3):
            ax.plot([x0 + k, x0 + k], [y0, y0 + 9],
                    linewidth=3, color='black')
            ax.plot([x0, x0 + 9], [y0 + k, y0 + k],
                    linewidth=3, color='black')

    draw_blocks(0, 6)     # S1
    draw_blocks(12, 6)    # S2
    draw_blocks(6, 0)     # S3

    for i in range(15):
        for j in range(21):
            if board[i, j] != -1:
                ax.text(j + 0.5,
                        14.5 - i,
                        str(board[i, j]),
                        ha='center',
                        va='center',
                        fontsize=10)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("TRIPLE SUDOKU",
                 fontsize=14)
    plt.gca().set_aspect('equal')
    plt.show()

def solve_sudoku_milp(grid):
    N = 9
    total_vars = 729

    def idx(i, j, k):
        return i * 81 + j * 9 + k

    c = np.zeros(total_vars)
    A = []
    b = []

    for i in range(N):
        for j in range(N):
            row = np.zeros(total_vars)
            for k in range(N):
                row[idx(i, j, k)] = 1
            A.append(row)
            b.append(1)

    for i in range(N):
        for k in range(N):
            row = np.zeros(total_vars)
            for j in range(N):
                row[idx(i, j, k)] = 1
            A.append(row)
            b.append(1)

    for j in range(N):
        for k in range(N):
            row = np.zeros(total_vars)
            for i in range(N):
                row[idx(i, j, k)] = 1
            A.append(row)
            b.append(1)

    for bi in range(3):
        for bj in range(3):
            for k in range(N):
                row = np.zeros(total_vars)
                for i in range(3):
                    for j in range(3):
                        row[idx(3 * bi + i, 3 * bj + j, k)] = 1
                A.append(row)
                b.append(1)

    for i in range(N):
        for j in range(N):
            if grid[i][j] != 0:
                row = np.zeros(total_vars)
                row[idx(i, j, grid[i][j] - 1)] = 1
                A.append(row)
                b.append(1)

    A = np.array(A)
    b = np.array(b)

    constraints = LinearConstraint(A, b, b)
    bounds = Bounds(0, 1)
    integrality = np.ones(total_vars)

    res = milp(c=c, constraints=constraints,
               bounds=bounds, integrality=integrality)

    sol = np.zeros((9, 9), dtype=int)
    for i in range(N):
        for j in range(N):
            for k in range(N):
                if res.x[idx(i, j, k)] > 0.5:
                    sol[i][j] = k + 1
    return sol


def solve_double_milp(g1, g2, mode):
    N = 9
    total_vars = 2 * 729

    def idx(n, i, j, k):
        return n * 729 + i * 81 + j * 9 + k

    c = np.zeros(total_vars)
    A = []
    b = []

    for n in range(2):
        for i in range(N):
            for j in range(N):
                row = np.zeros(total_vars)
                for k in range(N):
                    row[idx(n, i, j, k)] = 1
                A.append(row)
                b.append(1)

        for i in range(N):
            for k in range(N):
                row = np.zeros(total_vars)
                for j in range(N):
                    row[idx(n, i, j, k)] = 1
                A.append(row)
                b.append(1)

        for j in range(N):
            for k in range(N):
                row = np.zeros(total_vars)
                for i in range(N):
                    row[idx(n, i, j, k)] = 1
                A.append(row)
                b.append(1)

        for bi in range(3):
            for bj in range(3):
                for k in range(N):
                    row = np.zeros(total_vars)
                    for i in range(3):
                        for j in range(3):
                            row[idx(n, 3 * bi + i, 3 * bj + j, k)] = 1
                    A.append(row)
                    b.append(1)

    if mode == "6x6":
        for i in range(6):
            for j in range(6):
                for k in range(N):
                    row = np.zeros(total_vars)
                    row[idx(0, 3 + i, 3 + j, k)] = 1
                    row[idx(1, i, j, k)] = -1
                    A.append(row)
                    b.append(0)

    if mode == "3x3":
        for i in range(3):
            for j in range(3):
                for k in range(N):
                    row = np.zeros(total_vars)
                    row[idx(0, 6 + i, 6 + j, k)] = 1
                    row[idx(1, i, j, k)] = -1
                    A.append(row)
                    b.append(0)

    for i in range(N):
        for j in range(N):
            if g1[i][j] != 0:
                row = np.zeros(total_vars)
                row[idx(0, i, j, g1[i][j] - 1)] = 1
                A.append(row)
                b.append(1)
            if g2[i][j] != 0:
                row = np.zeros(total_vars)
                row[idx(1, i, j, g2[i][j] - 1)] = 1
                A.append(row)
                b.append(1)

    A = np.array(A)
    b = np.array(b)

    constraints = LinearConstraint(A, b, b)
    bounds = Bounds(0, 1)
    integrality = np.ones(total_vars)

    res = milp(c=c, constraints=constraints,
               bounds=bounds, integrality=integrality)

    s1 = np.zeros((9, 9), dtype=int)
    s2 = np.zeros((9, 9), dtype=int)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                if res.x[idx(0, i, j, k)] > 0.5:
                    s1[i][j] = k + 1
                if res.x[idx(1, i, j, k)] > 0.5:
                    s2[i][j] = k + 1
    return s1, s2


def solve_triple_milp(g1, g2, g3):
    N = 9
    total_vars = 3 * 729

    def idx(n, i, j, k):
        return n * 729 + i * 81 + j * 9 + k

    c = np.zeros(total_vars)
    A = []
    b = []

    for n in range(3):
        for i in range(N):
            for j in range(N):
                row = np.zeros(total_vars)
                for k in range(N):
                    row[idx(n, i, j, k)] = 1
                A.append(row)
                b.append(1)

        for i in range(N):
            for k in range(N):
                row = np.zeros(total_vars)
                for j in range(N):
                    row[idx(n, i, j, k)] = 1
                A.append(row)
                b.append(1)

        for j in range(N):
            for k in range(N):
                row = np.zeros(total_vars)
                for i in range(N):
                    row[idx(n, i, j, k)] = 1
                A.append(row)
                b.append(1)

        for bi in range(3):
            for bj in range(3):
                for k in range(N):
                    row = np.zeros(total_vars)
                    for i in range(3):
                        for j in range(3):
                            row[idx(n, 3 * bi + i, 3 * bj + j, k)] = 1
                    A.append(row)
                    b.append(1)

    for i in range(3):
        for j in range(3):
            for k in range(N):
                row = np.zeros(total_vars)
                row[idx(0, 6 + i, 6 + j, k)] = 1
                row[idx(2, i, j, k)] = -1
                A.append(row)
                b.append(0)

    for i in range(3):
        for j in range(3):
            for k in range(N):
                row = np.zeros(total_vars)
                row[idx(2, i, 6 + j, k)] = 1
                row[idx(1, 6 + i, j, k)] = -1
                A.append(row)
                b.append(0)

    for n, grid in enumerate([g1, g2, g3]):
        for i in range(N):
            for j in range(N):
                if grid[i][j] != 0:
                    row = np.zeros(total_vars)
                    row[idx(n, i, j, grid[i][j] - 1)] = 1
                    A.append(row)
                    b.append(1)

    A = np.array(A)
    b = np.array(b)

    constraints = LinearConstraint(A, b, b)
    bounds = Bounds(0, 1)
    integrality = np.ones(total_vars)

    res = milp(c=c, constraints=constraints,
               bounds=bounds, integrality=integrality)

    s1 = np.zeros((9, 9), dtype=int)
    s2 = np.zeros((9, 9), dtype=int)
    s3 = np.zeros((9, 9), dtype=int)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                if res.x[idx(0, i, j, k)] > 0.5:
                    s1[i][j] = k + 1
                if res.x[idx(1, i, j, k)] > 0.5:
                    s2[i][j] = k + 1
                if res.x[idx(2, i, j, k)] > 0.5:
                    s3[i][j] = k + 1
    return s1, s2, s3


easy = [
[2,0,5,0,0,9,0,0,4],
[0,0,0,0,0,0,3,0,7],
[7,0,0,8,5,6,0,1,0],
[4,5,0,7,0,0,0,0,0],
[0,0,9,0,0,0,1,0,0],
[0,0,0,0,0,2,0,8,5],
[0,2,0,4,1,8,0,0,6],
[6,0,8,0,0,0,0,0,0],
[1,0,0,2,0,0,7,0,8]
]

medium = [
[0,0,6,0,9,0,2,0,0],
[0,0,0,7,0,2,0,0,0],
[0,9,0,5,0,8,0,7,0],
[9,0,0,0,3,0,0,0,6],
[7,5,0,0,0,0,0,1,9],
[1,0,0,0,4,0,0,0,5],
[0,1,0,3,0,9,0,8,0],
[0,0,0,2,0,1,0,0,0],
[0,0,9,0,8,0,1,0,0]
]
hard = [
[0,0,0,8,0,0,0,0,0],
[7,8,9,0,1,0,0,0,6],
[0,0,0,0,0,6,1,0,0],
[0,0,7,0,0,0,0,5,0],
[5,0,8,7,0,9,3,0,4],
[0,4,0,0,0,0,2,0,0],
[0,0,3,2,0,0,0,0,0],
[8,0,0,0,7,0,4,3,9],
[0,0,0,0,0,1,0,0,0]
]

double_6_1 = [
[0,0,0,0,0,2,5,0,6],
[7,1,0,0,0,0,0,8,0],
[0,0,0,0,0,0,0,0,0],
[0,0,9,0,0,0,4,0,0],
[0,7,0,0,0,0,0,0,0],
[0,0,5,0,8,0,0,0,3],
[0,0,0,2,0,0,0,5,0],
[0,9,0,0,0,0,0,0,0],
[5,0,2,0,0,9,0,0,0]
]
double_6_2 = [
[0,0,0,4,0,0,8,0,1],
[0,0,0,0,0,0,0,3,0],
[0,8,0,0,0,3,0,0,0],
[2,0,0,0,5,0,4,0,0],
[0,0,0,0,0,0,0,1,0],
[0,0,9,0,0,0,5,0,0],
[0,0,0,0,0,0,0,0,0],
[0,6,0,0,0,0,0,2,9],
[8,0,7,3,0,0,0,0,0]
]
double_3_1 = [
[4,0,8,3,0,0,0,0,2],
[7,6,0,0,0,0,0,9,0],
[0,0,5,0,0,0,8,7,1],
[0,0,0,2,0,0,0,0,0],
[0,5,0,9,7,4,0,6,0],
[0,7,0,0,0,6,0,0,0],
[0,4,1,0,0,0,0,0,0],
[8,0,0,0,0,0,1,0,4],
[5,0,0,0,0,1,9,0,0]
]

double_3_2 = [
[0,0,0,6,9,0,0,4,2],
[1,0,4,8,0,0,0,0,0],
[9,0,0,0,0,0,8,0,1],
[8,6,0,2,0,7,0,0,4],
[0,0,0,3,8,6,0,0,0],
[3,0,0,9,4,5,0,2,8],
[2,0,8,0,0,0,1,0,5],
[7,0,0,0,0,0,4,0,3],
[6,1,0,0,5,9,0,0,0]
]
triple_1 = [
[6,0,8,0,1,0,0,0,0],
[0,0,7,0,4,0,8,0,1],
[0,0,0,0,0,0,0,0,9],
[0,6,0,7,0,0,0,3,0],
[0,7,0,5,0,4,0,0,0],
[0,0,0,8,0,0,9,5,0],
[0,0,0,0,7,8,0,0,0],
[5,0,1,0,0,0,0,0,0],
[0,0,4,0,0,6,0,0,0]
]
triple_2 = [
[0,0,0,0,6,0,3,0,9],
[7,0,3,0,4,0,1,0,0],
[6,0,0,0,0,0,0,0,0],
[0,7,0,0,0,6,0,9,0],
[0,0,0,7,0,4,0,8,0],
[0,5,4,0,0,9,0,0,0],
[0,0,0,4,9,0,0,0,0],
[0,0,0,0,0,0,9,0,5],
[0,0,0,3,0,0,4,0,0]
]

triple_3 = [
[0,0,0,1,0,8,0,0,0],
[0,0,0,0,3,0,0,0,0],
[0,0,0,0,7,0,0,0,0],
[4,0,0,0,0,0,0,0,6],
[0,0,0,6,5,2,0,0,0],
[0,0,1,0,0,0,2,0,0],
[0,0,0,5,0,3,0,0,0],
[0,8,7,0,0,0,6,5,0],
[0,4,0,0,0,0,0,8,0]
]

draw_sudoku(solve_sudoku_milp(easy), "EASY")
draw_sudoku(solve_sudoku_milp(medium), "MEDIUM")
draw_sudoku(solve_sudoku_milp(hard), "HARD")

s1, s2 = solve_double_milp(double_6_1, double_6_2, "6x6")
draw_double_6x6(s1, s2)

s3, s4 = solve_double_milp(double_3_1, double_3_2, "3x3")
draw_double_3x3(s3, s4)

t1, t2, t3 = solve_triple_milp(triple_1, triple_2, triple_3)
draw_triple(t1, t2, t3)
