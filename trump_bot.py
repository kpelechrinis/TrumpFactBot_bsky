import os
import requests
import random
from bs4 import BeautifulSoup
from atproto import Client
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
USERNAME = os.getenv("BSKY_USERNAME")
APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD")

def get_random_false_trump_claim():
    url = "https://www.politifact.com/factchecks/list/?ruling=false&speaker=donald-trump"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    statements = soup.find_all("li", class_="o-listicle__item")

    s = random.choice(statements)

    quote_tag = s.select_one("div.m-statement__quote a")
    quote = quote_tag.text.strip()
    link = "https://www.politifact.com" + quote_tag["href"]
    meta = s.select_one("div.m-statement__desc").text.strip()
    rating_img = s.select_one("div.m-statement__meter img")
    rating = rating_img["alt"].strip().capitalize() if rating_img else "Unknown"

    post = (
        f"🧯 Trump Claim: “{quote}”\n"
        f"🧪 Rated: {rating}\n"
        f"🗓️ {meta}\n"
        f"🔗 {link}"
    )
    return post

def post_to_bluesky(text):
    client = Client()
    client.login(USERNAME, APP_PASSWORD)
    client.send_post(text=text)

if __name__ == "__main__":
    post = get_random_false_trump_claim()
    print("Posting to Bluesky:\n", post)
    post_to_bluesky(post)

