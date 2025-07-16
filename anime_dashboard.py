import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Setup
st.set_page_config(page_title="Anime Dashboard", layout="wide")
st.title("🎬 Anime Data Dashboard")

# Load dataset
path = 'anime.csv'  # Path assumes file is in the repo
df = pd.read_csv(path)

# Clean rating and episodes
df = df.dropna(subset=['rating'])
df = df[df['episodes'].apply(lambda x: str(x).isdigit())]
df['episodes'] = df['episodes'].astype(int)

# Sidebar Filters
st.sidebar.header("🔎 Filters")
genre_filter = st.sidebar.text_input("Filter by Genre (e.g. Action)")
search_query = st.sidebar.text_input("Search Anime by Name")

# === SECTION 1: Top 10 Rated Anime ===
st.subheader(" Top 10 Rated Anime")
top_rated = df.sort_values(by='rating', ascending=False).head(10)
st.bar_chart(top_rated.set_index('name')['rating'])

# === SECTION 2: Most Popular Genres ===
st.subheader(" Most Popular Anime Genres")
df_genres = df.dropna(subset=['genre'])
all_genres = ','.join(df_genres['genre'].tolist()).split(',')
genre_counts = Counter([g.strip() for g in all_genres])
genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count']).sort_values(by='Count', ascending=False)
st.bar_chart(genre_df.set_index('Genre').head(10))

# === SECTION 3: Rating vs Episode Count ===
st.subheader(" Rating vs Episode Count")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=df, x='episodes', y='rating', hue='rating', size='rating',
                palette='viridis', alpha=0.6, sizes=(20, 200), legend=False, ax=ax1)
ax1.set_xlabel('Episodes')
ax1.set_ylabel('Rating')
st.pyplot(fig1)

# === SECTION 4: Top Anime by Members ===
st.subheader(" Top Anime by Members")
df_fav = df[df['members'].apply(lambda x: str(x).isdigit())].copy()
df_fav['members'] = df_fav['members'].astype(int)
top_fav = df_fav.sort_values(by='members', ascending=False).head(15)
fig2, ax2 = plt.subplots()
sns.barplot(data=top_fav, x='members', y='name', palette='flare', ax=ax2)
ax2.set_xlabel('Members')
ax2.set_ylabel('Anime Name')
st.pyplot(fig2)

# === SECTION 5: Average Rating by Type ===
st.subheader(" Average Rating by Anime Type")
df_type = df.dropna(subset=['type'])
type_avg = df_type.groupby('type')['rating'].mean().reset_index().sort_values(by='rating', ascending=False)
fig3, ax3 = plt.subplots()
sns.barplot(data=type_avg, x='type', y='rating', palette='pastel', ax=ax3)
ax3.set_xlabel('Type')
ax3.set_ylabel('Average Rating')
st.pyplot(fig3)

# === SECTION 6: Filter by Genre (if any) ===
if genre_filter:
    st.subheader(f" Top Anime in Genre: {genre_filter}")
    df_filtered = df[df['genre'].str.contains(genre_filter, case=False, na=False)]
    st.dataframe(df_filtered[['name', 'genre', 'rating', 'episodes']].sort_values(by='rating', ascending=False).head(10))

# === SECTION 7: Search Anime by Name ===
if search_query:
    st.subheader(f" Search Results for: {search_query}")
    matches = df[df['name'].str.lower().str.contains(search_query.lower())]
    st.dataframe(matches[['name', 'episodes', 'rating', 'genre']].sort_values(by='episodes', ascending=False))
