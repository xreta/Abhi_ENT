import requests
from bs4 import BeautifulSoup
import csv
import sqlite3
import datetime

class VergeScraper:
    def __init__(self):
        self.url = "https://www.theverge.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.article_data = []

    def get_articles(self):
        page = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(page.content, "html.parser")
        articles = soup.find_all("div", class_="c-entry-box--compact__body")

        for article in articles:
            headline = article.find("a", class_="c-entry-box--compact__title-link").get_text().strip()
            url = article.find("a", class_="c-entry-box--compact__title-link")["href"]
            author = article.find("span", class_="c-byline__item").get_text().strip()
            date = article.find("time")["datetime"][:10]
            self.article_data.append((url, headline, author, date))

    def write_csv(self):
        now = datetime.datetime.now()
        file_name = now.strftime("%d%m%Y") + "_verge.csv"
        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "URL", "headline", "author", "date"])
            for i, article in enumerate(self.article_data):
                writer.writerow([i, article[0], article[1], article[2], article[3]])

    def write_to_db(self):
        conn = sqlite3.connect("verge_articles.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS articles
                    (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date TEXT)''')
        c.execute("SELECT * FROM articles")
        existing_articles = c.fetchall()
        existing_urls = [article[1] for article in existing_articles]

        for article in self.article_data:
            if article[0] not in existing_urls:
                c.execute("INSERT INTO articles (url, headline, author, date) VALUES (?, ?, ?, ?)", article)

        conn.commit()
        conn.close()

if __name__ == "__main__":
    scraper = VergeScraper()
    scraper.get_articles()
    scraper.write_csv()
    scraper.write_to_db()
