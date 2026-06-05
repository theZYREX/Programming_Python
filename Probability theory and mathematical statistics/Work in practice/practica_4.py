import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

y = np.array([41297, 52590, 46544, 45232, 54631, 40883, 44764, 52848, 51285, 48919,
              50274, 41642, 50177, 46686, 50345, 50716, 52667, 58601, 57783, 55977,
              51048, 47186, 52671, 49173, 45165, 47916, 56973, 49653, 51517, 61008,
              54545, 47336, 50359, 53628, 50921, 52349, 55566, 51991, 45626, 50225,
              53831, 51844, 47875, 52580, 46927, 48627, 49845, 53135, 49120, 46504,
              53495, 45268, 49267, 51172, 54450, 43393, 52845, 47224, 54481, 53709,
              49315, 43439, 44357, 44456, 51700, 41783, 50753, 50901, 45108, 49820,
              43961, 44733, 40927, 48849, 46776, 50668, 45229, 48209, 48601, 55571,
              48546, 46198, 51246, 51929, 50670, 51863, 50175, 52175, 55591, 44315,
              49984, 51235, 46169, 55284, 50424, 58105, 42819, 50144, 51887, 44935,
              52704, 51525, 46113, 50273, 46626, 59149, 51617, 41118, 48532, 51986,
              40323, 40880, 51722, 50774, 50771, 46065, 46523, 50644, 47623, 46600,
              52689, 45402, 48394, 46748, 53314, 50568, 46603, 49685, 55887, 46811,
              59098, 56520, 54275, 49173, 51418, 43798, 47280, 51174, 48149, 50608,
              50355, 57404, 44132, 51524, 42911, 46183, 46304, 57014, 49560, 51118,
              47430, 47207, 45545, 39238, 41272, 50951, 51669, 53061, 49566, 47821,
              45936, 47143, 42660, 46524, 48358, 49212, 39627, 54645, 52576, 50258,
              48630, 47996, 58388, 50053, 49604, 47877, 47566, 55072, 49065, 48040,
              47510, 53379, 51173, 51564, 42957, 50980, 53749, 45165, 46496, 48558,
              46814, 47542, 49975, 47537, 52731, 40579, 53367, 47294, 46723, 45842,
              47219, 55393, 47932, 49802, 44450])

x = np.array([30756, 38140, 36067, 33731, 38094, 30380, 33316, 37466, 39360, 35895,
              37881, 31915, 38037, 35973, 35643, 37604, 35204, 40942, 42933, 39541,
              39236, 32710, 36061, 33646, 32825, 36824, 40732, 38122, 36674, 41580,
              36389, 36155, 33900, 37776, 37008, 38953, 38269, 35743, 35536, 36102,
              37600, 36712, 33838, 39062, 35624, 34654, 36018, 35886, 34246, 34956,
              35981, 35897, 35556, 37548, 39774, 31234, 39157, 35263, 39195, 35840,
              38735, 32631, 34056, 32420, 36918, 31726, 35702, 36226, 31510, 36508,
              32149, 34625, 30040, 34354, 35821, 36183, 33447, 35964, 34606, 36702,
              34933, 35256, 37062, 38137, 34490, 37711, 35022, 35564, 37500, 34804,
              37517, 34702, 33868, 40883, 36324, 39325, 32506, 36437, 36400, 32549,
              37468, 35513, 33146, 36317, 33748, 41565, 36425, 31747, 34022, 35294,
              32146, 32420, 36275, 35259, 36245, 33827, 34818, 34602, 34043, 32778,
              36240, 34598, 35771, 33115, 35513, 35479, 33649, 34868, 39849, 34206,
              41194, 36746, 38275, 34378, 37018, 32555, 36546, 34492, 35952, 34461,
              36788, 40380, 32245, 35751, 31747, 34549, 32408, 40553, 33619, 36643,
              35188, 34748, 33332, 29644, 31616, 34037, 34033, 37405, 36592, 34777,
              35051, 33277, 32101, 34867, 34348, 36712, 29621, 38637, 35646, 35194,
              35962, 34239, 40530, 36560, 33530, 35115, 33424, 38043, 34475, 34311,
              33842, 38094, 35710, 37257, 32846, 35867, 40129, 32396, 35234, 35171,
              34322, 36065, 37184, 33980, 36007, 30044, 35764, 34241, 35225, 33483,
              35059, 39043, 35131, 35913, 32743])

# ==============================
# 1. ПРОВЕРКА НА НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ (УЛУЧШЕННАЯ)
# ==============================
print("="*80)
print("1. ПРОВЕРКА ДВУХ ВЫБОРОК НА НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ")
print("="*80)

shapiro_x = stats.shapiro(x)
shapiro_y = stats.shapiro(y)
ks_x = stats.kstest(x, 'norm', args=(x.mean(), x.std(ddof=1)))
ks_y = stats.kstest(y, 'norm', args=(y.mean(), y.std(ddof=1)))

skew_x, skew_y = stats.skew(x), stats.skew(y)
kurt_x, kurt_y = stats.kurtosis(x), stats.kurtosis(y)

print("\n▶ Критерий Шапиро-Уилка:")
print(f"   X: статистика = {shapiro_x.statistic:.4f}, p-value = {shapiro_x.pvalue:.6f} → {'НЕ НОРМАЛЬНО' if shapiro_x.pvalue < 0.05 else 'НОРМАЛЬНО'}")
print(f"   Y: статистика = {shapiro_y.statistic:.4f}, p-value = {shapiro_y.pvalue:.6f} → {'НЕ НОРМАЛЬНО' if shapiro_y.pvalue < 0.05 else 'НОРМАЛЬНО'}")

print("\n▶ Критерий Колмогорова-Смирнова:")
print(f"   X: статистика = {ks_x.statistic:.4f}, p-value = {ks_x.pvalue:.6f} → {'НЕ НОРМАЛЬНО' if ks_x.pvalue < 0.05 else 'НОРМАЛЬНО'}")
print(f"   Y: статистика = {ks_y.statistic:.4f}, p-value = {ks_y.pvalue:.6f} → {'НЕ НОРМАЛЬНО' if ks_y.pvalue < 0.05 else 'НОРМАЛЬНО'}")

print("\n▶ Асимметрия и эксцесс:")
print(f"   X: асимметрия = {skew_x:.4f}, эксцесс = {kurt_x:.4f}")
print(f"   Y: асимметрия = {skew_y:.4f}, эксцесс = {kurt_y:.4f}")
print(f"   → Для нормального распределения: асимметрия ≈ 0, эксцесс ≈ 0")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

stats.probplot(x, dist="norm", plot=axes[0, 0])
axes[0, 0].set_title('QQ-plot для признака X', fontsize=12)

stats.probplot(y, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title('QQ-plot для признака Y', fontsize=12)

axes[1, 0].hist(x, bins=30, edgecolor='black', alpha=0.7, density=True)
x_range = np.linspace(x.min(), x.max(), 100)
axes[1, 0].plot(x_range, stats.norm.pdf(x_range, x.mean(), x.std()), 'r-', lw=2, label='Нормальное распределение')
axes[1, 0].set_xlabel('X')
axes[1, 0].set_ylabel('Плотность')
axes[1, 0].set_title('Гистограмма признака X')
axes[1, 0].legend()

axes[1, 1].hist(y, bins=30, edgecolor='black', alpha=0.7, density=True)
y_range = np.linspace(y.min(), y.max(), 100)
axes[1, 1].plot(y_range, stats.norm.pdf(y_range, y.mean(), y.std()), 'r-', lw=2, label='Нормальное распределение')
axes[1, 1].set_xlabel('Y')
axes[1, 1].set_ylabel('Плотность')
axes[1, 1].set_title('Гистограмма признака Y')
axes[1, 1].legend()

plt.tight_layout()
plt.show()

# ==============================
# 2. ПОЛЕ КОРРЕЛЯЦИИ И ГИПОТЕЗА О ФОРМЕ СВЯЗИ
# ==============================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(x, y, alpha=0.6, edgecolors='k', linewidth=0.5, s=50)
axes[0].set_xlabel('Признак X', fontsize=12)
axes[0].set_ylabel('Признак Y', fontsize=12)
axes[0].set_title('Поле корреляции', fontsize=14)
axes[0].grid(True, alpha=0.3)

from scipy.interpolate import UnivariateSpline
sorted_idx = np.argsort(x)
spline = UnivariateSpline(x[sorted_idx], y[sorted_idx], s=1e6)
axes[0].plot(x[sorted_idx], spline(x[sorted_idx]), 'g-', linewidth=2, label='Сглаженная кривая')
axes[0].legend()

box_data = [x, y]
bp = axes[1].boxplot(box_data, labels=['X', 'Y'], patch_artist=True)
bp['boxes'][0].set_facecolor('lightblue')
bp['boxes'][1].set_facecolor('lightgreen')
axes[1].set_title('Ящики с усами для выявления выбросов', fontsize=14)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "="*80)
print("2. ПОЛЕ КОРРЕЛЯЦИИ И ГИПОТЕЗА О ФОРМЕ СВЯЗИ")
print("="*80)
print("✓ На поле корреляции наблюдается прямая линейная зависимость")
print("✓ Сглаженная кривая подтверждает линейный характер связи")
print("✓ Гипотеза: форма связи - линейная (Y = a + b·X)")

# ==============================
# 3. ПАРАМЕТРЫ УРАВНЕНИЯ ПАРНОЙ РЕГРЕССИИ
# ==============================
X_with_const = sm.add_constant(x)
model = sm.OLS(y, X_with_const).fit()

b0, b1 = model.params
y_pred = model.predict(X_with_const)
residuals = model.resid

print("\n" + "="*80)
print("3. УРАВНЕНИЕ ПАРНОЙ РЕГРЕССИИ")
print("="*80)
print(f"Уравнение в явном виде: ŷ = {b0:.2f} + {b1:.8f}·x")
print(f"Экономическая интерпретация:")
print(f"  • При увеличении X на 1 единицу, Y увеличивается в среднем на {b1:.4f} единиц")
print(f"  • Свободный член {b0:.2f} - значение Y при X=0 (может не иметь экономического смысла)")

# ==============================
# 4. ПОКАЗАТЕЛИ КОРРЕЛЯЦИИ И ДЕТЕРМИНАЦИИ
# ==============================
r_pearson = np.corrcoef(x, y)[0, 1]
r_squared = r_pearson ** 2
r_adj = model.rsquared_adj

print("\n" + "="*80)
print("4. ПОКАЗАТЕЛИ ТЕСНОТЫ СВЯЗИ")
print("="*80)
print(f"Коэффициент корреляции Пирсона: r = {r_pearson:.6f}")
print(f"Коэффициент детерминации: R² = {r_squared:.6f}")
print(f"Скорректированный R² = {r_adj:.6f}")

if abs(r_pearson) >= 0.9:
    strength = "очень сильная"
elif abs(r_pearson) >= 0.7:
    strength = "сильная"
elif abs(r_pearson) >= 0.5:
    strength = "умеренная"
elif abs(r_pearson) >= 0.3:
    strength = "слабая"
else:
    strength = "очень слабая"

print(f"Характеристика связи (шкала Чеддока): {strength}")
print(f"Вариация Y на {r_squared*100:.2f}% объясняется вариацией X")

# ==============================
# 5. ЗНАЧИМОСТЬ КОЭФФИЦИЕНТОВ РЕГРЕССИИ
# ==============================
t_stats = model.tvalues
p_values = model.pvalues
conf_int = model.conf_int()

print("\n" + "="*80)
print("5. ЗНАЧИМОСТЬ КОЭФФИЦИЕНТОВ РЕГРЕССИИ (t-критерий Стьюдента)")
print("="*80)
print(f"{'Параметр':<12} {'Значение':<14} {'t-статистика':<14} {'p-value':<12} {'95% Доверительный интервал'}")
print("-"*80)
print(f"{'const':<12} {b0:>12.2f}   {t_stats[0]:>11.4f}   {p_values[0]:>10.6f}   [{conf_int[0][0]:>9.2f}, {conf_int[0][1]:>9.2f}]")
print(f"{'x':<12} {b1:>12.8f}   {t_stats[1]:>11.4f}   {p_values[1]:>10.6f}   [{conf_int[1][0]:>9.8f}, {conf_int[1][1]:>9.8f}]")

alpha = 0.05
print(f"\n▶ Вывод при уровне значимости α = {alpha}:")
if p_values[0] < alpha:
    print("  ✓ Свободный член (const) СТАТИСТИЧЕСКИ ЗНАЧИМ")
else:
    print("  ✗ Свободный член (const) СТАТИСТИЧЕСКИ НЕЗНАЧИМ")

if p_values[1] < alpha:
    print("  ✓ Коэффициент регрессии (x) СТАТИСТИЧЕСКИ ЗНАЧИМ → фактор X значимо влияет на Y")
else:
    print("  ✗ Коэффициент регрессии (x) СТАТИСТИЧЕСКИ НЕЗНАЧИМ → фактор X не влияет на Y")

# ==============================
# 6. F-КРИТЕРИЙ ФИШЕРА
# ==============================
f_statistic = model.fvalue
f_pvalue = model.f_pvalue
n = len(y)
k = 1
f_critical = stats.f.ppf(1 - alpha, k, n - k - 1)

print("\n" + "="*80)
print("6. СТАТИСТИЧЕСКАЯ НАДЁЖНОСТЬ МОДЕЛИ (F-критерий Фишера)")
print("="*80)
print(f"F-статистика (расчётная): {f_statistic:.6f}")
print(f"F-критическое (табличное): {f_critical:.6f}")
print(f"p-value: {f_pvalue:.6e}")

if f_statistic > f_critical:
    print(f"\n▶ Вывод: Fрасч ({f_statistic:.2f}) > Fкрит ({f_critical:.2f})")
    print("  ✓ Модель СТАТИСТИЧЕСКИ НАДЁЖНА (регрессия значима в целом)")
    print(f"  ✓ Вероятность ошибки: {f_pvalue:.4%}")
else:
    print(f"\n▶ Вывод: Fрасч ({f_statistic:.2f}) ≤ Fкрит ({f_critical:.2f})")
    print("  ✗ Модель СТАТИСТИЧЕСКИ НЕНАДЁЖНА")

# ==============================
# 7. ПРОГНОЗ
# ==============================
x_mean = np.mean(x)
x_pred = x_mean * 1.03
y_pred_val = b0 + b1 * x_pred

print("\n" + "="*80)
print("7. ПРОГНОЗНОЕ ЗНАЧЕНИЕ РЕЗУЛЬТАТА")
print("="*80)
print(f"Среднее значение фактора X: {x_mean:.2f}")
print(f"Увеличение на 3% от среднего: {x_mean * 0.03:.2f}")
print(f"Прогнозное значение фактора X: {x_pred:.2f}")
print(f"\n▶ Точечный прогноз Y: {y_pred_val:.2f}")

x_pred_matrix = np.array([1, x_pred]).reshape(1, -1)

y_pred_se_mean = np.sqrt(model.mse_resid * (x_pred_matrix @ np.linalg.inv(X_with_const.T @ X_with_const) @ x_pred_matrix.T))[0, 0]

y_pred_se_ind = np.sqrt(model.mse_resid * (1 + x_pred_matrix @ np.linalg.inv(X_with_const.T @ X_with_const) @ x_pred_matrix.T))[0, 0]

t_crit = stats.t.ppf(1 - alpha/2, n - k - 1)

y_pred_mean_lower = y_pred_val - t_crit * y_pred_se_mean
y_pred_mean_upper = y_pred_val + t_crit * y_pred_se_mean
y_pred_ind_lower = y_pred_val - t_crit * y_pred_se_ind
y_pred_ind_upper = y_pred_val + t_crit * y_pred_se_ind

print(f"\n95% доверительный интервал для СРЕДНЕГО прогноза:")
print(f"[{y_pred_mean_lower:.2f}; {y_pred_mean_upper:.2f}]")
print(f"\n95% доверительный интервал для ИНДИВИДУАЛЬНОГО прогноза:")
print(f"[{y_pred_ind_lower:.2f}; {y_pred_ind_upper:.2f}]")

# ==============================
# ДИАГНОСТИКА МОДЕЛИ
# ==============================
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# График регрессии
axes[0, 0].scatter(x, y, alpha=0.6, edgecolors='k', linewidth=0.5, s=50, label='Фактические данные')
x_line = np.linspace(x.min(), x.max(), 100)
y_line = b0 + b1 * x_line
axes[0, 0].plot(x_line, y_line, 'r-', linewidth=2, label='Линия регрессии')
axes[0, 0].scatter([x_pred], [y_pred_val], color='green', s=200, zorder=5, marker='*',
                   label=f'Прогноз: X={x_pred:.0f}, Y={y_pred_val:.0f}')
axes[0, 0].fill_between(x_line,
                         b0 + b1 * x_line - t_crit * np.sqrt(model.mse_resid),
                         b0 + b1 * x_line + t_crit * np.sqrt(model.mse_resid),
                         alpha=0.2, color='red', label='95% доверительная полоса')
axes[0, 0].set_xlabel('Признак X', fontsize=11)
axes[0, 0].set_ylabel('Признак Y', fontsize=11)
axes[0, 0].set_title('Парная линейная регрессия с прогнозом', fontsize=12)
axes[0, 0].legend(loc='upper left')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].scatter(y_pred, residuals, alpha=0.6, edgecolors='k', linewidth=0.5)
axes[0, 1].axhline(y=0, color='r', linestyle='--', linewidth=1.5)
axes[0, 1].set_xlabel('Предсказанные значения ŷ', fontsize=11)
axes[0, 1].set_ylabel('Остатки e', fontsize=11)
axes[0, 1].set_title('График остатков (гомоскедастичность)', fontsize=12)
axes[0, 1].grid(True, alpha=0.3)

stats.probplot(residuals, dist="norm", plot=axes[1, 0])
axes[1, 0].set_title('Q-Q plot остатков', fontsize=12)

axes[1, 1].hist(residuals, bins=30, edgecolor='black', alpha=0.7, density=True)
x_range = np.linspace(residuals.min(), residuals.max(), 100)
axes[1, 1].plot(x_range, stats.norm.pdf(x_range, residuals.mean(), residuals.std()), 'r-', lw=2, label='Нормальное распределение')
axes[1, 1].set_xlabel('Остатки')
axes[1, 1].set_ylabel('Плотность')
axes[1, 1].set_title('Гистограмма остатков')
axes[1, 1].legend()

plt.tight_layout()
plt.show()

# ==============================
# ДОПОЛНИТЕЛЬНАЯ ДИАГНОСТИКА
# ==============================
print("\n" + "="*80)
print("ДОПОЛНИТЕЛЬНЫЕ ХАРАКТЕРИСТИКИ МОДЕЛИ")
print("="*80)

# Стандартная ошибка регрессии
std_error = np.sqrt(model.mse_resid)
print(f"Стандартная ошибка регрессии (SEE): {std_error:.2f}")

# Средняя абсолютная ошибка
mae = np.mean(np.abs(residuals))
print(f"Средняя абсолютная ошибка (MAE): {mae:.2f}")

# Относительные ошибки
mpe = np.mean(100 * residuals / y)  # Mean Percentage Error
print(f"Средняя процентная ошибка (MPE): {mpe:.4f}%")

# Информационный критерий Акаике
aic = model.aic
print(f"AIC (Akaike Information Criterion): {aic:.2f}")

# Тест Бройша-Пагана на гетероскедастичность
bp_test = het_breuschpagan(residuals, X_with_const)
print(f"\nТест Бройша-Пагана на гетероскедастичность:")
print(f"  LM-статистика: {bp_test[0]:.4f}")
print(f"  p-value: {bp_test[1]:.6f}")
print(f"  → {'Гетероскедастичность присутствует' if bp_test[1] < 0.05 else 'Гомоскедастичность (нет гетероскедастичности)'}")

# Проверка на выбросы (z-оценка остатков)
z_scores = np.abs(stats.zscore(residuals))
outliers = np.where(z_scores > 3)[0]
print(f"\nКоличество потенциальных выбросов (|z| > 3): {len(outliers)} из {n} наблюдений")
if len(outliers) > 0:
    print(f"  Индексы выбросов: {outliers[:10]}..." if len(outliers) > 10 else f"  Индексы выбросов: {outliers}")

print(f"\nКоличество наблюдений: {n}")
print(f"Степени свободы: {n - k - 1}")
