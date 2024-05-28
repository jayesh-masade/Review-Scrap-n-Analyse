import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob

# Function to scrape reviews
def scrape_reviews(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    reviews = soup.find_all('div', class_='text_content')
    review_texts = [review.get_text(strip=True) for review in reviews]
    return review_texts

# Function for sentiment analysis
def analyze_sentiment(reviews):
    sentiments = []
    for review in reviews:
        blob = TextBlob(review)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = 'Positive'
        elif polarity == 0:
            sentiment = 'Neutral'
        else:
            sentiment = 'Negative'
        sentiments.append((review, polarity, sentiment))
    return sentiments

# Streamlit App interface
st.title('Review Sentiment Analyzer')
url = st.text_input("Enter your text here:")
if st.button('Fetch and Analyze Reviews'):
    reviews = scrape_reviews(url)
    if reviews:
        results = analyze_sentiment(reviews)
        df = pd.DataFrame(results, columns=['Review', 'Polarity', 'Sentiment'])
        st.write(df)
    else:
        st.error('No reviews found or there was an error fetching the reviews.')
