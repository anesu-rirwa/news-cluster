import requests
from bs4 import BeautifulSoup
import csv

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
                articles_data.append({'category': category, 'headline': title, 'summary': summary, 'link': link})

    return articles_data

def scrape_cnn_articles():
    url = 'https://edition.cnn.com/'
    categories = {
        'Business': 'https://edition.cnn.com/business/tech',
        'Politics': 'https://edition.cnn.com/politics',
        'Culture': 'https://edition.cnn.com/entertainment',
        'Sports': 'https://edition.cnn.com/sport'
    }
    articles_data = []

    for category, category_url in categories.items():
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('a', {'class': 'container__link--type-article'})
        print(articles)

        for article in articles:
            title = article.find('span', {'class': 'container__headline-text'})
            summary = ('span', {'class': 'container__headline-text'})
            link = article.find('a')
            articles_data.append({'category': category, 'headline': title, 'summary': summary, 'link': link})

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
                    articles_data.append({'category': category, 'headline': title.get_text(strip=True), 'summary': summary.get_text(strip=True), 'link': link.get('href')})

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
            articles_data.append({'category': category, 'headline': title, 'summary': summary, 'link': link})

    return articles_data


# Save articles to CSV files
def save_to_csv(articles, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['category', 'headline', 'summary', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)

# Scrape articles and save to CSV files
nyt_articles = scrape_nyt_articles()
cnn_articles = scrape_cnn_articles()
bbc_articles = scrape_bbc_articles()
washington_post_articles = scrape_washington_post_articles()

save_to_csv(nyt_articles, 'nyt_articles.csv')
save_to_csv(cnn_articles, 'cnn_articles.csv')
save_to_csv(bbc_articles, 'bbc_articles.csv')
save_to_csv(washington_post_articles, 'washington_post_articles.csv')

# Concatenate all articles
all_articles = []
all_articles.extend(nyt_articles)
all_articles.extend(bbc_articles)
all_articles.extend(washington_post_articles)

# Save to a single CSV file
save_to_csv(all_articles, 'all_articles.csv')