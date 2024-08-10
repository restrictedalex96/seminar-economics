import pandas as pd
import matplotlib.pyplot as plt


# Function to load and preprocess the data
def load_data(json_file, start_date=None, end_date=None):
    # Load the dataset
    df = pd.read_json(json_file)

    # Convert the 'publishedAt' column to datetime (timezone-naive)
    df['publishedAt'] = pd.to_datetime(df['publishedAt']).dt.tz_localize(None)

    # Create a new column with the date part of 'publishedAt'
    df['date'] = df['publishedAt'].dt.date

    #keywords_sudan = r'\b(?:war|death|kill|killed|fight|gun|civil|janjaweed|Hemedti|Darfur|hamas|jihad|islamic|deif|benjamin|isran|lebanon|hezbollah)\b'
    keywords_china = r'\b(?:war|death|kill|killed|fight|gun|civil|aero|space|invade|invasion|threat|threatens|threatening|foreign|independence|military|missile|china|arm|arms|ukraine|israel|sanctions|sanction|tension|tensions)\b'

    filtered_df = df[df['title'].str.lower().str.contains(keywords_china, na=False)]
    df = filtered_df

    # Filter by start and end date if provided
    if start_date:
        df = df[df['publishedAt'] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df['publishedAt'] <= pd.to_datetime(end_date)]

    return df


# Function to plot the data and highlight top 10 maximums
def plot_top_maximums(json_file, start_date=None, end_date=None):
    df = load_data(json_file, start_date, end_date)

    # Count the number of articles per day
    daily_counts = df.groupby('date').size()

    # Find the top 10 maximum values
    top_10_max = daily_counts.nlargest(5)

    # Plotting the daily counts
    plt.figure(figsize=(12, 8))
    plt.plot(daily_counts.index, daily_counts.values, marker='o', linestyle='-', label='Daily Counts')

    # Highlight the top 10 maximum values with red dots
    plt.scatter(top_10_max.index, top_10_max.values, color='red', label='Top 10 Maximums')

    # Annotate the top 10 maximum values with their dates
    for date, value in top_10_max.items():
        plt.annotate(f'{date}', (date, value), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.title('Number of Articles Per Day with Top 10 Maximums Highlighted')
    plt.xlabel('Date')
    plt.ylabel('Number of Articles')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Main function
def main(json_file, start_date=None, end_date=None):
    plot_top_maximums(json_file, start_date, end_date)


# Example usage
json_file = "../data/myanmar.json"
start_date = '2020-03-07'
end_date = '2024-07-01'
end_date=None
main(json_file, start_date, end_date)
