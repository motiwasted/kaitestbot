import os
import requests
import nltk
from bs4 import BeautifulSoup
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize
from transformers import TFAutoModel, AutoTokenizer

# Load pre-trained SciBERT model and tokenizer
model_name = 'allenai/scibert_scivocab_uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModel.from_pretrained(model_name, from_pt=True)

# Set Google Scholar API endpoint
GS_API = 'https://scholar.google.com/scholar'

# Example sentence
sentence = "The neural network is a form of artificial intelligence."

# Tokenize sentence and get parts of speech
words = word_tokenize(sentence)
pos_tags = nltk.pos_tag(words)

# Define list of popular bigrams
popular_bigrams = []
for i in range(len(pos_tags)-1):
    word1, tag1 = pos_tags[i]
    word2, tag2 = pos_tags[i+1]
    # Check if both words have allowed parts of speech and are not common words
    if tag1 in ['NN', 'NNS', 'JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] and \
       tag2 in ['NN', 'NNS', 'JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] and \
       word1.lower() not in ['is', 'are', 'was', 'were', 'am', 'form'] and \
       word2.lower() not in ['is', 'are', 'was', 'were', 'am', 'form']:
        bigram = f"{word1} {word2}"
        popular_bigrams.append(bigram)

# Select words based on parts of speech and bigrams
allowed_tags = ['NN', 'NNS', 'JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
selected_words = []
for i, (word, tag) in enumerate(pos_tags):
    # Check if word is a bigram
    if i < len(pos_tags) - 1:
        bigram = f"{word} {pos_tags[i+1][0]}"
        if bigram in popular_bigrams:
            selected_words.append(bigram)
            continue
    # Check if word has an allowed part of speech and is not a common word
    if tag in allowed_tags and word.lower() not in ['is', 'are', 'was', 'were', 'am', 'form']:
        selected_words.append(word)

# Get articles for selected words from Google Scholar
for word in selected_words:
    print(f"Searching for articles on Google Scholar for '{word}':")
    params = {'q': word, 'sort': 'date'}
    response = requests.get(GS_API, params=params)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', {'class': 'gs_ri'})
        if articles:
            for article in articles[:7]:
                title = article.find('h3', {'class': 'gs_rt'})
                link = article.find('a', href=True)
                if title and link:
                    print(f"Title: {title.text}")
                    print(f"Link: {link['href']}")
                    print()
        else:
            print("No articles found.")
    else:
        print(f"Error retrieving articles for '{word}': {response.status_code}")
