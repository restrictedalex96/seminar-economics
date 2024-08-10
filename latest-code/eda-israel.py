import pandas as pd

# Load your JSON data
df = pd.read_json("../title-data/israel.json")

# Convert publishedAt to datetime
df['publishedAt'] = pd.to_datetime(df['publishedAt'])

# Define the filter date and make it timezone-aware
filter_date = pd.to_datetime("2023-10-07").tz_localize('UTC')

# Filter the DataFrame
filtered_df = df[df['publishedAt'] > filter_date]

# Count unique sources
sources = filtered_df['source'].unique()
print(len(sources))
print(len(filtered_df))

# Show top 100 most common words in titles
from collections import Counter
import re

# Combine all titles into a single string
all_titles = ' '.join(filtered_df['title'].str.lower())

# Use regex to find all words
words = re.findall(r'\b\w+\b', all_titles)

# Count the frequency of each word

word_counts = Counter(words)
print(word_counts.most_common(100))

# print the most common sources
source_counts = filtered_df['source'].value_counts()
print(source_counts.head(10))


