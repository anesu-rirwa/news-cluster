import pandas as pd
import re
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load NLTK resources
nltk_data_path = "./nltk_data"  # Update this with your NLTK data directory path
stopwords.ensure_loaded()

# Load data
data = pd.read_csv('all_articles.csv')

# Clean text (keep named entities for better topic identification)
def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove punctuation but keep alphanumeric characters and spaces
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text

data['clean_summary'] = data['summary'].apply(clean_text)

# Tokenization and stop words removal (add domain-specific stopwords)
stop_words = set(stopwords.words('english'))
business_stopwords = ['company', 'market', 'revenue', 'stock']  # Add more as needed
culture_stopwords = ['art', 'film', 'music', 'entertainment']  # Add more as needed
sport_stopwords = ['game', 'player', 'team', 'league']  # Add more as needed
politics_stopwords = ['government', 'election', 'law', 'policy']  # Add more as needed

def tokenize(text, category):
    tokens = word_tokenize(text)
    # Add category-specific stopwords based on the article category (replace with actual logic)
    if category == "Business":
        stop_words_combined = stop_words.union(business_stopwords)
    elif category == "Culture":
        stop_words_combined = stop_words.union(culture_stopwords)
    elif category == "Sport":
        stop_words_combined = stop_words.union(sport_stopwords)
    elif category == "Politics":
        stop_words_combined = stop_words.union(politics_stopwords)
    else:
        stop_words_combined = stop_words
    tokens = [token for token in tokens if token not in stop_words_combined]
    return tokens

# Include a category column in your data (replace with actual logic to assign categories)
# Define a function to assign categories based on keywords or other criteria
def assign_category(row):
    if 'business' in row['link'].lower() or 'business' in row['headline'].lower():
        return 'Business'
    elif 'politics' in row['link'].lower() or 'politics' in row['headline'].lower():
        return 'Politics'
    elif 'culture' in row['link'].lower() or 'culture' in row['headline'].lower():
        return 'Culture'
    elif 'sports' in row['link'].lower() or 'sports' in row['headline'].lower():
        return 'Sports'
    else:
        return 'Other'

# Apply the function to create the 'category' column
data['category'] = data.apply(assign_category, axis=1)

# Preprocess text based on category
data['tokenized_summary'] = data.apply(lambda row: tokenize(row['clean_summary'], row['category']), axis=1)

# Feature extraction using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['clean_summary'])

# Determine optimal number of clusters (ideally use elbow method)
# For simplicity, let's choose 4 clusters
num_clusters = 4

# Train K-means model
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(tfidf_matrix)

# Assign clusters to documents
data['cluster'] = kmeans.labels_

# Function to show articles in each cluster
def show_cluster(cluster_id, num_display=10):
    if cluster_id == -1:
        st.write("No articles in this cluster")
    elif cluster_id == 0:
        st.subheader(f'Cluster {cluster_id} - Business')
    elif cluster_id == 1:
        st.subheader(f'Cluster {cluster_id} - Politics')
    elif cluster_id == 2:
        st.subheader(f'Cluster {cluster_id} - Culture')
    else:
        st.subheader(f'Cluster {cluster_id} - Sports')

    cluster_articles = data[data['cluster'] == cluster_id]
    for i, row in cluster_articles.head(num_display).iterrows():
        st.write(f"**Headline:** {row['headline']}")
        st.write(f"**Summary:** {row['summary']}")
        st.write(f"**Link:** {row['link']}")
        st.write("---")

# Streamlit UI
st.title("Document Clustering App")
st.write("This application clusters news articles into categories.")

# Slider to select number of articles to show per cluster
num_display = st.slider('Select number of articles per cluster:', 1, 20, 10)

# Display articles in each cluster
for i in range(num_clusters):
    show_cluster(i, num_display)
