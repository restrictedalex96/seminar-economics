import json
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

with open("data_old/israel_big.json", "r") as f:
    json_data = json.load(f)


# Filter records after October 1, 2023
start_date = datetime(2023, 10, 1, tzinfo=timezone.utc)

# Filtering records that are after the start_date
filtered_records = [record for record in json_data if datetime.fromisoformat(record['publishedAt'].replace('Z', '+00:00')) > start_date]

# Aggregate records by date
dates = [datetime.fromisoformat(record['publishedAt'].replace('Z', '+00:00')).date() for record in filtered_records]
date_counts = Counter(dates)

# Sort the dates for plotting
sorted_dates = sorted(date_counts.keys())
counts = [date_counts[date] for date in sorted_dates]

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(sorted_dates, counts, label='Events')

import json
from datetime import datetime, timezone
import matplotlib.pyplot as plt
from collections import Counter
import matplotlib.dates as mdates
import numpy as np
from scipy.optimize import curve_fit

# Function for exponential decay fitting
def exp_decay(x, a, r):
    return a * np.exp(-r * x)


# Calculate and plot the trendline
z = np.polyfit(mdates.date2num(sorted_dates), counts, 1)  # Fit the trendline
p = np.polyval(z, mdates.date2num(sorted_dates))  # Evaluate the polynomial
plt.plot(sorted_dates, p, "r-", label='Trendline')  # Plot the trendline in red

# Basic statistics
mean = np.mean(counts)
median = np.median(counts)
std_dev = np.std(counts)
data_range = np.ptp(counts)

# Exponential decay rate analysis
x_data = np.arange(len(counts))
params, _ = curve_fit(exp_decay, x_data, counts, p0=[max(counts), 0.1])
r = params[1]  # Decay rate

plt.title('Sudan Number of Events per Day')
plt.xlabel('Date')
plt.ylabel('Number of Events')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()  # Adjust plot to fit labels
plt.savefig('israel.png', dpi=300)  # Save as PNG with high resolution
plt.show()  # Show the plot in the output as well

# Print the statistics and decay rate


print(f"Mean: {mean}, Median: {median}, Standard Deviation: {std_dev}, Range: {data_range}")
print(f"Decay Rate (r): {r}")
