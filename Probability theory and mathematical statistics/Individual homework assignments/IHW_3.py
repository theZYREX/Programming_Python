import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

# Индивидуальное домашнее задание №3 по теме "Обработка одномерной выборки"
#Вариант 9

# Дана выборка значений признака Х.
# 1. Построить статистическую совокупность
# 2. Построить гистограмму относительных частот
# 3. Вычислить точечные характеристики
# 4. Найти доверительный интервал для оценки математического ожидания нормального распределения
# 5. •Проверить гипотезу о нормальном распределении при уровне значимости 0,05

data = [
    56, 76, 65, 66, 76, 62, 89, 48, 62, 50, 47, 80, 67, 87, 78,
    55, 67, 51, 73, 75, 61, 88, 46, 57, 65, 60, 72, 28, 75, 51,
    69, 68, 65, 34, 77, 63, 57, 61, 42, 85, 49, 41, 62, 63, 80,
    62, 65, 75, 56, 66, 92, 60, 43, 52, 80, 68, 70, 76, 62, 55,
    42, 87, 81, 67, 65, 81, 90, 38, 58, 60, 79, 79, 50, 64, 70,
    58, 77, 73, 54, 58, 77, 86, 52, 61, 42, 70, 93, 54, 65, 51,
    53, 64, 65, 76, 88, 59, 62, 67, 62, 90, 88, 69, 61, 81, 65,
    72, 58, 68, 94, 54, 58, 58, 81, 57, 70, 71, 78, 52, 93, 89,
    57, 68, 70, 58, 72, 57, 62, 63, 87, 61, 91, 57, 57, 66, 68,
    40, 63, 86, 48, 75, 66, 83, 64, 55, 75, 65, 67, 54, 70, 44,
    51, 86, 67, 58, 73, 71, 46, 86, 68, 79, 50, 58, 66, 69, 61,
    64, 78, 78, 60, 46, 71, 71, 74, 79, 65, 61, 62, 84, 53, 67,
    83, 43, 64, 67, 50, 60, 83, 61, 83, 67, 67, 58, 46, 73, 58,
    47, 76, 81, 72, 66, 83, 73, 71, 70, 60, 68, 52, 51, 63, 63,
    75, 61, 80, 51, 63, 62, 46
]

data = np.array(data)
n = len(data)

# --- ПУНКТ 1: Построить статистическую совокупность ---
# Определяем количество интервалов по формуле Стерджеса: k = 1 + 3.322 * log10(n)
k = int(1 + 3.322 * np.log10(n))
x_min = data.min()
x_max = data.max()
range_val = x_max - x_min
h = range_val / k  # Шаг интервала

bins = np.linspace(x_min, x_max, k + 1)
counts, bin_edges = np.histogram(data, bins=bins)

intervals = [f"[{bin_edges[i]:.1f}; {bin_edges[i + 1]:.1f})" for i in range(len(bin_edges) - 1)]
intervals[-1] = f"[{bin_edges[-2]:.1f}; {bin_edges[-1]:.1f}]"

df_stat = pd.DataFrame({
    'Интервал': intervals,
    'Частота (ni)': counts,
    'Относит. частота (wi)': counts / n
})

print("--- 1. Статистическая совокупность (Интервальный ряд) ---")
print(f"Объем выборки n = {n}")
print(f"Количество интервалов k = {k}")
print(df_stat)
print("\n")

# --- ПУНКТ 2: Гистограмма относительных частот ---
plt.figure(figsize=(10, 6))
plt.hist(data, bins=bins, density=True, alpha=0.7, edgecolor='black', label='Эмпирическая плотность')

mu = data.mean()
sigma = data.std(ddof=1)
x = np.linspace(x_min, x_max, 100)
p = stats.norm.pdf(x, mu, sigma)
plt.plot(x, p, 'r-', linewidth=2, label='Теоретическая кривая (Normal)')

plt.title('Гистограмма относительных частот и кривая нормального распределения')
plt.xlabel('Значение признака X')
plt.ylabel('Плотность частоты (wi / h)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# --- ПУНКТ 3: Точечные характеристики ---
mean_val = np.mean(data)
var_bias = np.var(data)  # Смещенная дисперсия (Dв)
var_unbias = np.var(data, ddof=1)  # Несмещенная дисперсия (S^2)
std_unbias = np.std(data, ddof=1)  # Исправленное среднее квадратическое отклонение (S)

print("--- 3. Точечные характеристики ---")
print(f"Выборочная средняя (x̄): {mean_val:.4f}")
print(f"Выборочная дисперсия (Dв, смещенная): {var_bias:.4f}")
print(f"Исправленная дисперсия (S²): {var_unbias:.4f}")
print(f"Исправленное среднее квадратическое отклонение (S): {std_unbias:.4f}")
print("\n")

# --- ПУНКТ 4: Доверительный интервал для мат. ожидания ---
gamma = 0.95
alpha = 1 - gamma
# Используем распределение Стьюдента, так как дисперсия неизвестна
t_crit = stats.t.ppf(1 - alpha / 2, n - 1)
margin_error = t_crit * (std_unbias / np.sqrt(n))
conf_interval = (mean_val - margin_error, mean_val + margin_error)

print("--- 4. Доверительный интервал ---")
print(f"Уровень доверия: {gamma}")
print(f"Критическое значение t (Стьюдент): {t_crit:.4f}")
print(f"Доверительный интервал: ({conf_interval[0]:.4f}; {conf_interval[1]:.4f})")
print("\n")

# --- ПУНКТ 5: Проверка гипотезы о нормальном распределении (Критерий Пирсона) ---
# H0: Распределение нормальное
# H1: Распределение не нормальное
# Уровень значимости alpha = 0.05

alpha = 0.05

theoretical_probs = []
for i in range(len(bin_edges) - 1):
    p = stats.norm.cdf(bin_edges[i + 1], mean_val, std_unbias) - stats.norm.cdf(bin_edges[i], mean_val, std_unbias)
    theoretical_probs.append(p)

theoretical_counts = np.array(theoretical_probs) * n

theoretical_counts = theoretical_counts * (n / theoretical_counts.sum())

print("Наблюдаемые частоты:", counts)
print("Ожидаемые частоты:", theoretical_counts)
print("Сумма наблюдаемых:", counts.sum())
print("Сумма ожидаемых:", theoretical_counts.sum())

obs_combined = []
exp_combined = []

i = 0
while i < len(counts):
    obs_temp = counts[i]
    exp_temp = theoretical_counts[i]

    while exp_temp < 5 and i < len(counts) - 1:
        i += 1
        obs_temp += counts[i]
        exp_temp += theoretical_counts[i]

    obs_combined.append(obs_temp)
    exp_combined.append(exp_temp)
    i += 1

obs_combined = np.array(obs_combined)
exp_combined = np.array(exp_combined)

print("\nПосле объединения интервалов:")
print("Наблюдаемые частоты:", obs_combined)
print("Ожидаемые частоты:", exp_combined)

k_combined = len(obs_combined)

chi2_stat = ((obs_combined - exp_combined) ** 2 / exp_combined).sum()

df = k_combined - 1 - 2
chi2_crit = stats.chi2.ppf(1 - alpha, df)

p_value = 1 - stats.chi2.cdf(chi2_stat, df)

print("\n--- 5. Проверка гипотезы (Критерий Пирсона χ²) ---")
print(f"Количество интервалов после объединения: {k_combined}")
print(f"Наблюдаемое значение χ²: {chi2_stat:.4f}")
print(f"Критическое значение χ² (крит) при df={df}: {chi2_crit:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Уровень значимости α: {alpha}")

if chi2_stat < chi2_crit:
    print("\n✓ ВЫВОД: Гипотеза о нормальном распределении НЕ ОТВЕРГАЕТСЯ (принимается).")
    print("  Выборка согласуется с нормальным законом распределения.")
else:
    print("\n✗ ВЫВОД: Гипотеза о нормальном распределении ОТВЕРГАЕТСЯ.")
    print("  Распределение отличается от нормального.")
