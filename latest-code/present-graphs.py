import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table


# Function definitions for each event
def sudan_event_1(x):
    return (0.636 * x + 14.686) / (0.184 * x + 0.782)


def sudan_event_2(x):
    return (14.696 * x + 34.549) / (4.082 * x + 1.016)


def china_taiwan_event_1(x):
    return 10.386 + 107.664 / (x + 2.369)


def israel_palestine_event_1(x):
    return -0.000 * x ** 4 + 0.000 * x ** 3 + 0.002 * x ** 2 - 0.697 * x + 64.095


def israel_palestine_event_2(x):
    return 0.000 * x ** 4 - 0.003 * x ** 3 + 0.229 * x ** 2 - 6.160 * x + 73.581


def myanmar_event_1(x):
    return 2.426 + 150.638 / (x + 3.356)


def russia_ukraine_event_1(x):
    return 42.537 + 1115.860 / (x + 5.671)


def yemen_event_1(x):
    return 6.587 + 114.932 / (x + 8.657)


# Data for the tables
best_fitting_no_transform = [
    [r"$\frac{0.636x + 14.686}{0.184x + 0.782}$", "Best Fitting No Transform", r"$R^2 = 0.2354$"],
    [r"$\frac{14.696x + 34.549}{4.082x + 1.016}$", "Best Fitting No Transform", r"$R^2 = 0.7369$"],
    [r"$10.386 + \frac{107.664}{x + 2.369}$", "Best Fitting No Transform", r"$R^2 = 0.5379$"],
    [r"$-0.000x^4 + 0.000x^3 + 0.002x^2 - 0.697x + 64.095$", "Best Fitting No Transform", r"$R^2 = 0.7593$"],
    [r"$0.000x^4 - 0.003x^3 + 0.229x^2 - 6.160x + 73.581$", "Best Fitting No Transform", r"$R^2 = 0.6044$"],
    [r"$2.426 + \frac{150.638}{x + 3.356}$", "Best Fitting No Transform", r"$R^2 = 0.7292$"],
    [r"$42.537 + \frac{1115.860}{x + 5.671}$", "Best Fitting No Transform", r"$R^2 = 0.6243$"],
    [r"$6.587 + \frac{114.932}{x + 8.657}$", "Best Fitting No Transform", r"$R^2 = 0.1203$"]
]

inverse_no_transform = [
    [r"$3.465 + \frac{65.233}{x + 4.258}$", "Inverse No Transform", r"$R^2 = 0.2354$"],
    [r"$4.512 + \frac{0.320}{x - 31.196}$", "Inverse No Transform", r"$R^2 = 0.0024$"],
    [r"$10.386 + \frac{107.664}{x + 2.369}$", "Inverse No Transform", r"$R^2 = 0.5379$"],
    [r"$80754.405 + \frac{27792507764.382}{x - 344378.151}$", "Inverse No Transform", r"$R^2 = 0.6349$"],
    [r"$19.811 + \frac{145.131}{x + 2.093}$", "Inverse No Transform", r"$R^2 = 0.5448$"],
    [r"$2.426 + \frac{150.638}{x + 3.356}$", "Inverse No Transform", r"$R^2 = 0.7292$"],
    [r"$42.537 + \frac{1115.860}{x + 5.671}$", "Inverse No Transform", r"$R^2 = 0.6243$"],
    [r"$6.587 + \frac{114.932}{x + 8.657}$", "Inverse No Transform", r"$R^2 = 0.1203$"]
]

best_transform_and_function = [
    [r"$\frac{0.565x + 5.846}{0.260x + 0.172}$", "Difference", r"$R^2 = 0.4600$"],
    [r"$\frac{0.175x + 1.874}{0.060x + 0.054}$", "Exp. Smoothing", r"$R^2 = 0.8927$"],
    [r"$9.704 + \frac{145.551}{x + 3.003}$", "Exp. Smoothing", r"$R^2 = 0.7527$"],
    [r"$-0.000x^4 + 0.000x^3 + 0.003x^2 - 0.785x + 66.148$", "Exp. Smoothing", r"$R^2 = 0.8690$"],
    [r"$0.000x^4 - 0.004x^3 + 0.243x^2 - 6.651x + 79.891$", "Exp. Smoothing", r"$R^2 = 0.8286$"],
    [r"$2.158 + \frac{183.187}{x + 3.718}$", "Exp. Smoothing", r"$R^2 = 0.8941$"],
    [r"$42.227 + \frac{1209.292}{x + 5.822}$", "Exp. Smoothing", r"$R^2 = 0.7533$"],
    [r"$6.629 + \frac{102.216}{x + 6.730}$", "Moving Average", r"$R^2 = 0.3038$"]
]

rows_updated = [
    "Sudan Event 1", "Sudan Event 2", "China Taiwan Event 1",
    "Israel-Palestine Event 1", "Israel-Palestine Event 2",
    "Myanmar Event 1", "Russia-Ukraine Event 1", "Yemen Event 1"
]

columns = ["Function", "Transformation", r"$R^2$"]


# Function to render a table
def render_table_updated(data):
    fig, ax = plt.subplots(figsize=(12, 8))

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    tbl = Table(ax, bbox=[0, 0, 1, 1])

    for i, row_data in enumerate(data):
        tbl.add_cell(i, 0, width=0.4, height=0.1, text=row_data[0], loc='center')
        tbl.add_cell(i, 1, width=0.3, height=0.1, text=row_data[1], loc='center')
        tbl.add_cell(i, 2, width=0.3, height=0.1, text=row_data[2], loc='center')

    for i, column_name in enumerate(columns):
        tbl.add_cell(-1, i, width=0.4 if i == 0 else 0.3, height=0.1, text=column_name, loc='center', facecolor='gray')

    for i, row_name in enumerate(rows_updated):
        tbl.add_cell(i, -1, width=0.2, height=0.1, text=row_name, loc='center', facecolor='lightgray')

    ax.add_table(tbl)
    plt.show()


# Render the tables with updated event names
render_table_updated(best_fitting_no_transform)
render_table_updated(inverse_no_transform)
render_table_updated(best_transform_and_function)

# X values for plotting
x_values = np.linspace(0.1, 100, 400)

# Plot each function with different colors and only show positive Y values
plt.figure(figsize=(14, 8))

plt.plot(x_values, np.maximum(0, sudan_event_1(x_values)), label="Sudan Event 1, $R^2 = 0.2354$", color="blue")
plt.plot(x_values, np.maximum(0, sudan_event_2(x_values)), label="Sudan Event 2, $R^2 = 0.7369$", color="green")
plt.plot(x_values, np.maximum(0, china_taiwan_event_1(x_values)), label="China Taiwan Event 1, $R^2 = 0.5379$",
         color="red")
plt.plot
