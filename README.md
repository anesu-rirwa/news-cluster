# Document Clustering App

## Rirwa Anesu R204432D HAI 

This Streamlit application clusters news articles into categories based on their content. It uses K-means clustering to group similar articles together.

## How to Use

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your_username/your_repository.git
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the App:**
    ```bash
    streamlit run app.py
    ```

4. **Open Browser:**
   Go to [http://localhost:8501](http://localhost:8501) in your browser to view the app.

5. **Explore Clusters:**
   - Use the slider to select the number of articles to display per cluster.
   - Each cluster represents a category (e.g., Business, Politics, Culture, Sports).
   - Click 'View more' to see additional articles in each cluster.

## Dependencies

- pandas
- re
- streamlit
- nltk
- scikit-learn

## Files

- `app.py`: The main Streamlit application.
- `all_articles.csv`: CSV file containing scraped news articles.
- `requirements.txt`: List of Python dependencies.

## Credits

- This app was created by [Your Name].
- Data scraped from various news websites using Python and BeautifulSoup.

