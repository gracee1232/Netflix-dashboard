import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("netflix_cleaned.csv")

st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.title("🎬 Netflix Data Dashboard")

# Filters
year = st.sidebar.selectbox("Select Year Added", sorted(df['year_added'].dropna().unique(), reverse=True))
content_type = st.sidebar.selectbox("Select Type", ["All", "Movie", "TV Show"])

filtered_df = df[df['year_added'] == year]
if content_type != "All":
    filtered_df = filtered_df[filtered_df['type'] == content_type]

st.markdown(f"### Showing content added in **{year}** ({content_type})")

# Chart 1: Content Type Distribution
type_count = df['type'].value_counts()
fig1 = px.pie(values=type_count.values, names=type_count.index, title="Content Type Distribution")

# Chart 2: Content by Country
top_countries = df['country'].value_counts().nlargest(10)
fig2 = px.bar(x=top_countries.index, y=top_countries.values, title="Top 10 Countries by Content")

# Chart 3: Genre Word Cloud
genre_series = df['listed_in'].dropna().str.split(', ')
from collections import Counter
flat_genres = [genre for sublist in genre_series for genre in sublist]
genre_counts = Counter(flat_genres).most_common(10)
genre_df = pd.DataFrame(genre_counts, columns=['Genre', 'Count'])
fig3 = px.bar(genre_df, x='Genre', y='Count', title="Top Genres")

# Layout
col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig1)
col2.plotly_chart(fig2)
col3.plotly_chart(fig3)

# Data table
st.markdown("### 🎞️ Raw Netflix Titles")
st.dataframe(filtered_df[['title', 'type', 'country', 'release_year', 'rating', 'duration']])
