import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
URL = "https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets"
OUTPUT_FILE = "data.csv"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to fetch page content
def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return BeautifulSoup(response.text, "lxml")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        exit()

# Generic function to extract data based on tag and class
def extract_data(soup, tag, class_name):
    return [element.text for element in soup.find_all(tag, class_=class_name)]

# Create DataFrame from extracted data
def create_dataframe(titles, descriptions, ratings, prices):
    return pd.DataFrame({
        "Titles": titles,
        "Description": descriptions,
        "Review": ratings,
        "Price": prices
    })

# Save DataFrame to CSV file
def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
    logging.info(f"Data saved to {filename}")

if __name__ == "__main__":
    logging.info("Starting the web scraping process...")

    # Fetch and parse page content
    soup = fetch_page_content(URL)

    # Extract data
    titles = extract_data(soup, 'a', 'title')
    descriptions = extract_data(soup, 'p', 'description card-text')
    ratings = extract_data(soup, 'p', 'review-count float-end')
    prices = extract_data(soup, 'h4', 'price float-end card-title pull-right')

    # Create DataFrame
    df = create_dataframe(titles, descriptions, ratings, prices)
    print(df)

    # Save DataFrame to CSV with dynamic filename
    filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    save_to_csv(df, filename)
