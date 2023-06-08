import os
import requests
import tensorflow as tf
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize
from transformers import TFAutoModel, AutoTokenizer

# Load pre-trained SciBERT model and tokenizer
model_name = 'allenai/scibert_scivocab_uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModel.from_pretrained(model_name, from_pt=True)

# Set S2ORC API endpoint
S2ORC_API = 'https://api.semanticscholar.org/graph/v1/paper/search'

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
    # Check if both words have allowed parts of speech
    if tag1 in ['NN', 'NNS', 'JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] and \
       tag2 in ['NN', 'NNS', 'JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
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
    # Check if word has an allowed part of speech
    if tag in allowed_tags:
        selected_words.append(word)

# Get frequency count for each selected word in S2ORC dataset
total_counts = {}
for word in selected_words:
    response = requests.get(S2ORC_API, params={'query': word, 'total': True})
    if response.ok:
        total_count = response.json().get('total', 0)
        total_counts[word] = total_count
    else:
        print(f"Error retrieving articles for '{word}': {response.json().get('error')}")

# Sort words by total count in descending order
sorted_words = sorted(total_counts.items(), key=lambda x: x[1], reverse=True)

# Print selected words and their total counts
if len(sorted_words) > 0:
    print(f"Total counts for selected words in S2ORC dataset:")
    for word, count in sorted_words[:5]:
        print(f"{word}: {count}")
        # Search for top 10 results on Google Scholar
        query = word.replace('"', '')
        url = GS_URL.format(query)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        for result in soup.find_all("h3", class_="gs_rt")[:10]:
            title = result.text
            link = result.a["href"]
            print(f"{title} - {link}")
        print()
else:
    print("No articles found for selected words.")
