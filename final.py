import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re
import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Scraper functions
def scrape_nyt_articles():
    base_url = 'https://www.nytimes.com'
    categories = {
        'Business': 'https://www.nytimes.com/section/business',
        'Politics': 'https://www.nytimes.com/section/politics',
        'Culture': 'https://www.nytimes.com/section/arts',
        'Sports': 'https://www.nytimes.com/topic/subject/soccer'
    }
    articles_data = []

    for category, category_url in categories.items():
        for page_num in range(1, 6):  # Scrape 5 pages for each category
            category_page_url = f"{category_url}?page={page_num}"
            response = requests.get(category_page_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('li', {'class': 'css-18yolpw'})

            for article in articles:
                title = article.find('h3').get_text(strip=True)
                summary = article.find('p').get_text(strip=True)
                link = base_url + article.find('a').get('href')
                articles_data.append({'headline': title, 'summary': summary, 'link': link})

    return articles_data

def scrape_guardian_articles():
    url = 'https://www.theguardian.com/'
    categories = {
        'Business': 'https://www.theguardian.com/business',
        'Politics': 'https://www.theguardian.com/politics',
        'Culture': 'https://www.theguardian.com/culture',
        'Sports': 'https://www.theguardian.com/sport'
    }
    articles_data = []

    for category, category_url in categories.items():
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_='fc-item__content')

        for article in articles:
            title = article.find('span', class_='js-headline-text').text.strip()
            summary = article.find('p', class_='js-item__standfirst').text.strip()
            link = article.find('a')['href']
            articles_data.append({'headline': title, 'summary': summary, 'link': link})

    return articles_data

def scrape_cnn_articles():
    url = 'https://edition.cnn.com/'
    categories = {
        'Business': 'https://edition.cnn.com/business',
        'Politics': 'https://edition.cnn.com/politics',
        'Culture': 'https://edition.cnn.com/entertainment',
        'Sports': 'https://edition.cnn.com/sport'
    }
    articles_data = []

    for category, category_url in categories.items():
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', class_='cd__content')

        for article in articles:
            title = article.find('h3', class_='cd__headline').text.strip()
            summary = article.find('div', class_='cd__description').text.strip()
            link = article.find('a')['href']
            articles_data.append({'headline': title, 'summary': summary, 'link': link})

    return articles_data

def scrape_bbc_articles():
    url = 'https://www.bbc.com/'
    categories = {
        'Sport': 'https://www.bbc.com/sport',
        'Culture': 'https://www.bbc.com/culture',
        'Business': 'https://www.bbc.com/news/business',
        'Politics': 'https://www.bbc.com/news/politics'
    }
    articles_data = []

    for category, category_url in categories.items():
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('div', {'data-testid': 'anchor-inner-wrapper'})

        for article in articles:
            title = article.find('h2', {'data-testid': 'card-headline'})
            summary = article.find('p', {'data-testid': 'card-description'})
            link = article.find('a', {'data-testid': 'internal-link'})

            # Check if title and summary exist
            if title and summary:
                if link == None:
                    continue
                else:
                    articles_data.append({'headline': title.get_text(strip=True), 'summary': summary.get_text(strip=True), 'link': link.get('href')})

    return articles_data

def scrape_washington_post_articles():
    url = 'https://www.washingtonpost.com/'

    categories = {
        'Politics': 'https://www.washingtonpost.com/politics/',
        'Business': 'https://www.washingtonpost.com/business/technology/',
        'Culture': 'https://www.washingtonpost.com/entertainment/art/',
        'Sports': 'https://www.washingtonpost.com/sports/racing-motorsports/'
    }
    
    articles_data = []

    for category, category_url in categories.items():
        response = requests.get(category_url)
        
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('div', {'class': 'pb-md b bb gray-darkest mt-md'})

        for article in articles:
            if category == 'Culture':
                title = article.find('h3').get_text(strip=True)
                summary = article.find('p').get_text(strip=True)
            else:
                title = article.find('h3').get_text(strip=True)
                summary = article.find('p').get_text(strip=True)
            link = article.find('a').get('href')
            articles_data.append({'headline': title, 'summary': summary, 'link': link})

    return articles_data

# Save articles to CSV files
def save_to_csv(articles, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['headline', 'summary', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)

# Scrape articles and save to CSV files
nyt_articles = scrape_nyt_articles()
guardian_articles = scrape_guardian_articles()
cnn_articles = scrape_cnn_articles()
bbc_articles = scrape_bbc_articles()
washington_post_articles = scrape_washington_post_articles()

save_to_csv(nyt_articles, 'nyt_articles.csv')
save_to_csv(guardian_articles, 'guardian_articles.csv')
save_to_csv(cnn_articles, 'cnn_articles.csv')
save_to_csv(bbc_articles, 'bbc_articles.csv')
save_to_csv(washington_post_articles, 'washington_post_articles.csv')

# Concatenate all articles
all_articles = []
all_articles.extend(nyt_articles)
all_articles.extend(guardian_articles)
all_articles.extend(cnn_articles)
all_articles.extend(bbc_articles)
all_articles.extend(washington_post_articles)

# Save to a single CSV file
save_to_csv(all_articles, 'all_articles.csv')

# Load data
data = pd.read_csv('all_articles.csv')

# Clean text
def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    return text

data['clean_summary'] = data['summary'].apply(clean_text)

# Tokenization and stop words removal
stop_words = set(stopwords.words('english'))

def tokenize(text):
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

data['tokenized_summary'] = data['clean_summary'].apply(tokenize)

# Feature extraction using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(data['clean_summary'])

# Determine optimal number of clusters (optional)
# For simplicity, let's choose 4 clusters since we have 4 categories
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
        st.subheader(f'Cluster {cluster_id} - Politics')

    else:
        st.subheader(f'Cluster {cluster_id}')
        cluster_articles = data[data['cluster'] == cluster_id].head(num_display)
        for i, row in cluster_articles.iterrows():
            st.write(f"**Headline:** {row['headline']}")
            st.write(f"**Summary:** {row['summary']}")
            st.write(f"**Link:** {row['link']}")
            st.write("---")

        if len(cluster_articles) > num_display:
            if st.button('View more'):
                st.write(cluster_articles.tail(len(cluster_articles)-num_display))

# Streamlit UI
st.title("Document Clustering App")

# Display articles in each cluster
for i in range(num_clusters):
    show_cluster(i)
