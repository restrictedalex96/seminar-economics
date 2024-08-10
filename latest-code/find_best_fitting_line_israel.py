import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from sklearn.metrics import r2_score

# Load the dataset
df_israel = pd.read_json("../data/israel.json")

# Convert the 'publishedAt' column to datetime
df_israel['publishedAt'] = pd.to_datetime(df_israel['publishedAt'])

# Filter articles starting from October 7th, 2023
df_filtered = df_israel[df_israel['publishedAt'] >= '2023-10-07']

# Extract the date (without time) from 'publishedAt'
df_filtered = df_filtered.assign(date=df_filtered['publishedAt'].dt.date)

# Count the number of articles per day
daily_counts = df_filtered.groupby('date').size()

# Define a set of candidate functions
def cubic(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

def exponential(x, a, b, c):
    return a * np.exp(b * x) + c

def inverse(x, a, b, c):
    return a + b / (x + c + 1e-9)  # small constant to avoid division by zero

def quartic(x, a, b, c, d, e):
    return a * x**4 + b * x**3 + c * x**2 + d * x + e

def rational(x, a, b, c, d):
    return (a * x + b) / (c * x + d)

functions = {
    "Cubic": cubic,
    "Quadratic": quadratic,
    "Exponential": exponential,
    "Inverse": inverse,
    "Quartic": quartic,
    "Rational": rational,
}

# Convert the date range strings to datetime.datetime
date_range_start = pd.to_datetime('2023-10-08')
date_range_end = pd.to_datetime('2024-07-01')

# Ensure the index of daily_counts is of type datetime.datetime
daily_counts.index = pd.to_datetime(daily_counts.index)

# Filter data for the specified date range
filtered_counts = daily_counts[(daily_counts.index >= date_range_start) & (daily_counts.index <= date_range_end)]

# Convert dates to numerical format for fitting (days since the start of the range)
date_numerical = (filtered_counts.index - filtered_counts.index[0]).days

# Fit each function and calculate R²
results = []
x_values = np.linspace(date_numerical.min(), date_numerical.max(), 500)

for name, func in functions.items():
    try:
        params, _ = curve_fit(func, date_numerical, filtered_counts.values, maxfev=10000)
        r2 = r2_score(filtered_counts.values, func(date_numerical, *params))
        results.append((name, r2, params))
    except Exception as e:
        print(f"Could not fit {name}: {e}")

# Identify the best fit based on R²
best_fit = max(results, key=lambda x: x[1])
best_name, best_r2, best_params = best_fit

# Plotting the daily counts and the best fitting function
plt.figure(figsize=(12, 8))
plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-', label='Daily Counts')

# Plot the best fitting curve
fit_x = np.linspace(date_numerical.min(), date_numerical.max(), 500)
fit_y = functions[best_name](fit_x, *best_params)
fit_dates = filtered_counts.index[0] + pd.to_timedelta(fit_x, unit='D')
plt.plot(fit_dates, fit_y, color='red', label=f'Best Fit: {best_name} (R²={best_r2:.2f})')

plt.title('Number of Articles Per Day with Best Fitting Curve')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Print the best fitting function's parameters
print(f"\nBest fitting function: {best_name}")
print(f"R²: {best_r2}")
print(f"Parameters: {best_params}")
