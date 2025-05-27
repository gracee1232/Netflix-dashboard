import pandas as pd

# Load data
df = pd.read_csv("/Users/atharvpareta/Desktop/dashboard/netflix_titles.csv")

# Drop rows with missing type or title
df.dropna(subset=['type', 'title'], inplace=True)

# Convert 'date_added' to datetime
df['date_added'] = pd.to_datetime(df['date_added'].str.strip(), errors='coerce')


# Extract year, month from date_added
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month

# Clean duration
df[['duration_int', 'duration_type']] = df['duration'].str.extract(r'(\d+)\s*(\w+)')
df['duration_int'] = pd.to_numeric(df['duration_int'], errors='coerce')

# Fill missing country with "Unknown"
df['country'].fillna("Unknown", inplace=True)

# Clean up
df.drop_duplicates(inplace=True)
df.to_csv("netflix_cleaned.csv", index=False)
print("✅ Data cleaned and saved as netflix_cleaned.csv")
