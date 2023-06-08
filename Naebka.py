import requests
from bs4 import BeautifulSoup

def show_articles():
    search_words = ["neural network", "Network", "Artificial", "Artificial intelligence"]
    base_url = "https://scholar.google.com/scholar"
    
    for word in search_words:
        query_params = {"q": word, "as_ylo": 2023}
        response = requests.get(base_url, params=query_params)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("h3", class_="gs_rt")
        
        print(f"Articles for '{word}':")
        for article in articles:
            article_title = article.text
            article_link = article.a["href"]
            print(f"{article_title}\n{article_link}")
        print()

# Вызов функции для показа статей
show_articles()
