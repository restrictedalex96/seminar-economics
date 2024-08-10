import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from sklearn.metrics import r2_score

# Define the functions for fitting
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

transform_methods = ['none', 'bins', 'log', 'sensitive_bins', 'moving_average', 'difference', 'standardize', 'normalize', 'exp_smoothing']

# Function to load and preprocess the data
def load_and_preprocess(json_file, start_date, end_date):
    # Load the dataset
    df = pd.read_json(json_file)

    # Convert the 'publishedAt' column to datetime
    df['publishedAt'] = pd.to_datetime(df['publishedAt']).dt.tz_localize(None)

    # Create a new column with the date part of 'publishedAt'
    df['date'] = df['publishedAt'].dt.date

    # Filter articles based on keywords
    sudan_keywords = r'\b(?:war|death|kill|killed|fight|gun|civil|janjaweed|Hemedti|Darfur|hamas|jihad|islamic|deif|benjamin|isran|lebanon|hezbollah)\b'
    keywords_china = r'\b(?:war|death|kill|killed|fight|gun|civil|aero|space|invade|invasion|threat|threatens|threatening|foreign|independence|military|missile|china|arm|arms|ukraine|israel|sanctions|sanction|tension|tensions)\b'
    israel_keywords = r'\b(?:war|death|kill|killed|fight|gun|civil|hamas|jihad|islamic|deif|benjamin|iran|lebanon|hezbollah|idf|terror|terrorist|bomb|famine|aid|ship|gun|iran|drone)\b'
    mynamar_keywords = r'\b(?:war|death|kill|killed|fight|gun|civil|hamas|jihad|islamic|deif|benjamin|iran|lebanon|hezbollah|idf|terror|terrorist|bomb|famine|aid|ship|gun|iran|drone|coup|détat|detat|junta)\b'
    ukraine_keywords = r'\b(?:war|death|kill|killed|fight|gun|civil|hamas|jihad|islamic|deif|benjamin|iran|lebanon|hezbollah|idf|terror|terrorist|bomb|famine|aid|ship|gun|iran|drone|invade|invades|russia|)\b'


    keywords = ukraine_keywords
    filtered_df = df[df['title'].str.lower().str.contains(keywords, na=False)]

    # Filter articles within the date range
    filtered_df = filtered_df[(filtered_df['publishedAt'] >= pd.to_datetime(start_date)) & (filtered_df['publishedAt'] <= pd.to_datetime(end_date))]

    return filtered_df

# Function to transform the counts
def transform_counts(daily_counts, method, window=3):
    if method == 'bins':
        bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, np.inf]
        labels = range(len(bins) - 1)
        transformed_counts = pd.cut(daily_counts, bins=bins, labels=labels, right=False)
    elif method == 'log':
        transformed_counts = np.log1p(daily_counts)  # log1p to handle log(0)
    elif method == 'sensitive_bins':
        bins = [0, 8, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, np.inf]
        labels = range(len(bins) - 1)
        transformed_counts = pd.cut(daily_counts, bins=bins, labels=labels, right=False)
    elif method == 'moving_average':
        transformed_counts = daily_counts.rolling(window=window).mean().dropna()
    elif method == 'difference':
        transformed_counts = daily_counts.diff().dropna().abs()
    elif method == 'standardize':
        transformed_counts = (daily_counts - daily_counts.mean()) / daily_counts.std()
    elif method == 'normalize':
        transformed_counts = (daily_counts - daily_counts.min()) / (daily_counts.max() - daily_counts.min())
    elif method == 'exp_smoothing':
        transformed_counts = daily_counts.ewm(span=window, adjust=False).mean()
    else:
        transformed_counts = daily_counts
    return transformed_counts

# Function to fit curves and find the best fit
def find_best_fit(filtered_df, start_date, end_date, transform_method='none', window=3):
    # Count the number of articles per day
    daily_counts = filtered_df.groupby('date').size()

    # Transform the counts
    transformed_counts = transform_counts(daily_counts, transform_method, window)

    # Align transformed counts with original index
    if transform_method in ['moving_average', 'difference', 'rolling_mean']:
        aligned_index = daily_counts.index[-len(transformed_counts):]
        transformed_counts.index = aligned_index

    # Convert the date range strings to datetime.datetime
    date_range_start = pd.to_datetime(start_date)
    date_range_end = pd.to_datetime(end_date)

    # Ensure the index of daily_counts and transformed_counts is of type datetime.datetime
    daily_counts.index = pd.to_datetime(daily_counts.index)
    transformed_counts.index = pd.to_datetime(transformed_counts.index)

    # Filter data for the specified date range
    filtered_counts = daily_counts[(daily_counts.index >= date_range_start) & (daily_counts.index <= date_range_end)]
    transformed_filtered_counts = transformed_counts[(transformed_counts.index >= date_range_start) & (transformed_counts.index <= date_range_end)]

    # Ensure the lengths of date_numerical and transformed_filtered_counts are the same
    date_numerical = (filtered_counts.index - filtered_counts.index[0]).days
    min_len = min(len(date_numerical), len(transformed_filtered_counts))
    date_numerical = date_numerical[:min_len]
    transformed_filtered_counts = transformed_filtered_counts.iloc[:min_len]

    # Fit each function and calculate R²
    results = []
    x_values = np.linspace(date_numerical.min(), date_numerical.max(), 500)

    for name, func in functions.items():
        try:
            params, _ = curve_fit(func, date_numerical, transformed_filtered_counts.values, maxfev=10000)
            r2 = r2_score(transformed_filtered_counts.values, func(date_numerical, *params))
            results.append((name, r2, params))
        except Exception as e:
            print(f"Could not fit {name}: {e}")

    # Check if there are any valid results
    if not results:
        print("No valid fitting results.")
        return None, None, None, None

    # Identify the best fit based on R²
    best_fit = max(results, key=lambda x: x[1])
    best_name, best_r2, best_params = best_fit

    # Return the best fit details
    return best_name, best_r2, best_params, (daily_counts, transformed_counts, date_numerical, transformed_filtered_counts, filtered_counts)

# Function to fit the inverse function without transformation
def fit_inverse(filtered_df, start_date, end_date):
    # Count the number of articles per day
    daily_counts = filtered_df.groupby('date').size()

    # Convert the date range strings to datetime.datetime
    date_range_start = pd.to_datetime(start_date)
    date_range_end = pd.to_datetime(end_date)

    # Ensure the index of daily_counts is of type datetime.datetime
    daily_counts.index = pd.to_datetime(daily_counts.index)

    # Filter data for the specified date range
    filtered_counts = daily_counts[(daily_counts.index >= date_range_start) & (daily_counts.index <= date_range_end)]

    # Ensure the lengths of date_numerical and filtered_counts are the same
    date_numerical = (filtered_counts.index - filtered_counts.index[0]).days

    # Fit the inverse function and calculate R²
    try:
        params, _ = curve_fit(inverse, date_numerical, filtered_counts.values, maxfev=1000000)
        r2 = r2_score(filtered_counts.values, inverse(date_numerical, *params))
        best_name = 'Inverse'
        best_r2 = r2
        best_params = params
        return best_name, best_r2, best_params, (daily_counts, filtered_counts, date_numerical, filtered_counts, filtered_counts)
    except Exception as e:
        print(f"Could not fit Inverse: {e}")
        return None, None, None, None

# Function to plot the results
def plot_results(daily_counts, filtered_counts, fit_x, fit_y, best_name, best_r2, best_params, title):
    plt.figure(figsize=(12, 8))
    plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-', label='Daily Counts')
    plt.plot(fit_x, fit_y, color='red', label=f'Best Fit: {best_name} (R²={best_r2:.2f})')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Print the best fitting function's details
    if best_name == 'Cubic':
        equation = f"{best_params[0]:.3f}x^3 + {best_params[1]:.3f}x^2 + {best_params[2]:.3f}x + {best_params[3]:.3f}"
    elif best_name == 'Quadratic':
        equation = f"{best_params[0]:.3f}x^2 + {best_params[1]:.3f}x + {best_params[2]:.3f}"
    elif best_name == 'Exponential':
        equation = f"{best_params[0]:.3f} * exp({best_params[1]:.3f} * x) + {best_params[2]:.3f}"
    elif best_name == 'Inverse':
        equation = f"{best_params[0]:.3f} + {best_params[1]:.3f} / (x + {best_params[2]:.3f})"
    elif best_name == 'Quartic':
        equation = f"{best_params[0]:.3f}x^4 + {best_params[1]:.3f}x^3 + {best_params[2]:.3f}x^2 + {best_params[3]:.3f}x + {best_params[4]:.3f}"
    elif best_name == 'Rational':
        equation = f"({best_params[0]:.3f}x + {best_params[1]:.3f}) / ({best_params[2]:.3f}x + {best_params[3]:.3f})"
    else:
        equation = f" + ".join([f"{p:.3f}x^{i}" for i, p in enumerate(best_params)])

    print(f"\nBest fitting function: {best_name}")
    print(f"R²: {best_r2}")
    print(f"Parameters: {best_params}")
    print(f"Function: f(x) = {equation}")

# Main function
def main(json_file, start_date, end_date):
    filtered_df = load_and_preprocess(json_file, start_date, end_date)

    # Plotting without transformation
    print("\nPlotting without transformation...")
    best_name_none, best_r2_none, best_params_none, plot_data_none = find_best_fit(filtered_df, start_date, end_date, 'none')

    if plot_data_none:
        daily_counts, transformed_counts, date_numerical, transformed_filtered_counts, filtered_counts = plot_data_none
        fit_x = np.linspace(date_numerical.min(), date_numerical.max(), 500)
        fit_y = functions[best_name_none](fit_x, *best_params_none)
        fit_dates = filtered_counts.index[0] + pd.to_timedelta(fit_x, unit='D')
        plot_results(daily_counts, filtered_counts, fit_dates, fit_y, best_name_none, best_r2_none, best_params_none, 'Number of Articles Per Day with Best Fitting Curve (No Transformation)')

    # Plotting always with the inverse function without transformation
    print("\nPlotting with inverse function without transformation...")
    best_name_inverse, best_r2_inverse, best_params_inverse, plot_data_inverse = fit_inverse(filtered_df, start_date, end_date)

    if plot_data_inverse:
        daily_counts, transformed_counts, date_numerical, transformed_filtered_counts, filtered_counts = plot_data_inverse
        fit_x = np.linspace(date_numerical.min(), date_numerical.max(), 500)
        fit_y = inverse(fit_x, *best_params_inverse)
        fit_dates = filtered_counts.index[0] + pd.to_timedelta(fit_x, unit='D')
        plot_results(daily_counts, filtered_counts, fit_dates, fit_y, best_name_inverse, best_r2_inverse, best_params_inverse, 'Number of Articles Per Day with Inverse Function (No Transformation)')

    # Finding the best transformation method
    best_overall_fit = None
    best_overall_name = None
    best_overall_r2 = -1
    best_overall_params = None
    best_overall_transform_method = None

    for method in transform_methods:
        if method != 'none':  # Skip 'none' as it is already plotted
            best_name, best_r2, best_params, plot_data = find_best_fit(filtered_df, start_date, end_date, method)
            if best_r2 and best_r2 > best_overall_r2:
                best_overall_r2 = best_r2
                best_overall_name = best_name
                best_overall_params = best_params
                best_overall_transform_method = method
                best_overall_plot_data = plot_data

    if best_overall_transform_method:
        print(f"\nBest overall transformation method: {best_overall_transform_method}")

    # Plotting the best transformation method
    if best_overall_plot_data:
        daily_counts, transformed_counts, date_numerical, transformed_filtered_counts, filtered_counts = best_overall_plot_data
        fit_x = np.linspace(date_numerical.min(), date_numerical.max(), 500)
        fit_y = functions[best_overall_name](fit_x, *best_overall_params)
        fit_dates = filtered_counts.index[0] + pd.to_timedelta(fit_x, unit='D')
        plot_results(daily_counts, filtered_counts, fit_dates, fit_y, best_overall_name, best_overall_r2, best_overall_params, f'Number of Articles Per Day with Best Fitting Curve ({best_overall_transform_method.capitalize()} Method)')

# Example usage
json_file = "../data/ethiopia.json"
start_date = '2022-01-01'
end_date = '2023-01-01'
main(json_file, start_date, end_date)
