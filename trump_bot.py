import os
import requests
import random
from bs4 import BeautifulSoup
from atproto import Client
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
USERNAME = "@trumpfactbot.bsky.social"
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
    print(f"USERNAME: {repr(USERNAME)}")
    print(f"APP_PASSWORD: {repr(APP_PASSWORD)}")
    print(f"LENGTHS: {len(USERNAME)} chars, {len(APP_PASSWORD)} chars")
    client.login(USERNAME, APP_PASSWORD)

    MAX_LENGTH = 300

    if len(text) <= MAX_LENGTH:
        # Simple case — just post
        client.send_post(text=text)
        return

    print(f"⚠️ Post is too long ({len(text)} characters). Creating thread...")

    # Split text: pull out quote and details separately
    lines = text.split('\n')
    quote_line = lines[0]
    rest_lines = lines[1:]

    # Shrink quote if needed
    allowed_quote_len = MAX_LENGTH - len("\n".join(rest_lines)) - 10
    truncated_quote = quote_line[:allowed_quote_len].rstrip("…") + "…”"
    first_post = truncated_quote + "\n" + "\n".join(rest_lines[:-1])

    # Extract just the link
    link = rest_lines[-1].strip()

    # Post first part
    root_post = client.send_post(text=first_post)

    # Follow-up post with the link
    client.send_post(
        text=f"🔗 Full fact-check: {link}",
        reply_to={
            "uri": root_post.uri,
            "cid": root_post.cid,
        }
    )

if __name__ == "__main__":
    post = get_random_false_trump_claim()
    print("Posting to Bluesky:\n", post)
    post_to_bluesky(post)

