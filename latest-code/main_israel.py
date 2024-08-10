import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

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

# Define the inverse function for fitting
def inverse_function(x, a, b, c):
    return a + b / (x + c)

# Convert the date range strings to datetime.date
date_range_start = pd.to_datetime('2023-10-08').date()
date_range_end = pd.to_datetime('2024-03-15').date()

# Ensure the index of daily_counts is of type datetime.date
daily_counts.index = pd.to_datetime(daily_counts.index).date

# Filter data for the specified date range
filtered_counts = daily_counts[(daily_counts.index >= date_range_start) & (daily_counts.index <= date_range_end)]

# Convert dates to numerical format for fitting (e.g., days since the start of the range)
date_numerical = (pd.to_datetime(filtered_counts.index) - pd.to_datetime(filtered_counts.index[0])).days

# Fit the inverse function to the data
    params, _ = curve_fit(inverse_function, date_numerical, filtered_counts.values)

# Plotting the daily counts
plt.figure(figsize=(12, 6))
plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-', label='Daily Counts')

# Plot the fitted curve
fit_x = np.linspace(date_numerical.min(), date_numerical.max(), 500)
fit_y = inverse_function(fit_x, *params)
fit_dates = pd.to_datetime(filtered_counts.index[0]) + pd.to_timedelta(fit_x, unit='D')
plt.plot(fit_dates, fit_y, color='red', label='Fitted Curve')

# Set the number of x-ticks (dates) to display
num_ticks = 10
ticks_to_use = daily_counts.index[::max(1, len(daily_counts) // num_ticks)]
plt.xticks(ticks=ticks_to_use, rotation=45)

plt.title('Israel-Gaza War Number of Articles Per Day')
plt.xlabel('Date')
plt.ylabel('Number of Articles')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
