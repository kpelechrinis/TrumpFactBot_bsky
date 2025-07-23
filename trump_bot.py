import os
import requests
import random
from bs4 import BeautifulSoup
from atproto import Client, models
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
USERNAME = os.getenv("BSKY_USERNAME").strip()
APP_PASSWORD = os.getenv("BSKY_APP_PASSWORD").strip()

# Define max pages per ruling
MAX_PAGES_BY_RATING = {
    "false": 50,
    "pants-on-fire": 25
}

def pick_random_weighted_page(max_pages):
    weights = [1 / (i + 1) for i in range(max_pages)]
    total = sum(weights)
    return random.choices(range(1, max_pages + 1), weights=weights, k=1)[0]

def get_recent_quotes(client, limit=50):
    feed = client.get_author_feed(actor=USERNAME, limit=limit)
    quotes = []

    for item in feed.feed:
        if hasattr(item.post.record, "text"):
            text = item.post.record.text
            first_line = text.split("\n")[0].strip()
            if first_line.startswith("🔥 Trump Claim: “"):
                quotes.append(first_line)

    return quotes

def get_random_trump_claim(recent_quotes, max_attempts=5):
    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(max_attempts):
        rating_choice = random.choice(["false", "pants-on-fire"])
        max_pages = MAX_PAGES_BY_RATING[rating_choice]
        page = pick_random_weighted_page(max_pages)

        url = f"https://www.politifact.com/factchecks/list/?ruling={rating_choice}&speaker=donald-trump&page={page}"
        print(f"🎯 Scraping rating: {rating_choice.upper()} — Page {page}")

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        statements = soup.find_all("li", class_="o-listicle__item")

        valid_statements = []
        for s in statements:
            rating_img = s.select_one("div.m-statement__meter img")
            if rating_img:
                rating = rating_img["alt"].strip().lower()
                if rating == rating_choice or (rating_choice == "pants-on-fire" and rating == "pants on fire!"):
                    valid_statements.append(s)

        if not valid_statements:
            print(f"❌ No valid claims on page {page}. Retrying...")
            continue

        s = random.choice(valid_statements)
        quote_tag = s.select_one("div.m-statement__quote a")
        quote = quote_tag.text.strip()
        quote_line = f"🔥 Trump Claim: “{quote}”"

        # Check for duplicates
        if quote_line in recent_quotes:
            print(f"⚠️ Already posted: \"{quote}\" — retrying...")
            continue

        link = "https://www.politifact.com" + quote_tag["href"]
        meta = s.select_one("div.m-statement__desc").text.strip()
        rating_text = rating_img["alt"].strip().capitalize()

        post = (
            f"{quote_line}\n"
            f"📉 Rated: {rating_text}\n"
            f"🗓️  {meta}\n"
            f"🔗 {link}"
        )
        return post

    raise ValueError("🚫 No new, unposted Trump claim found after several attempts.")

def post_to_bluesky(text, client):
    MAX_LENGTH = 300

    if len(text) <= MAX_LENGTH:
        client.send_post(text=text)
        return

    # Create a thread
    lines = text.split('\n')
    quote_line = lines[0]
    rest_lines = lines[1:]

    allowed_quote_len = MAX_LENGTH - len("\n".join(rest_lines)) - 10
    truncated_quote = quote_line[:allowed_quote_len].rstrip("…") + "…”"
    first_post = truncated_quote + "\n" + "\n".join(rest_lines[:-1])
    link = rest_lines[-1].strip()

    # Post first
    root_post = client.send_post(text=first_post)

    # Follow-up with the link
    client.send_post(
        text=f"🔗 Full fact-check: {link}",
        reply_to=models.AppBskyFeedPost.ReplyRef(
            root=models.ComAtprotoRepoStrongRef.Main(
                uri=root_post.uri,
                cid=root_post.cid
            ),
            parent=models.ComAtprotoRepoStrongRef.Main(
                uri=root_post.uri,
                cid=root_post.cid
            )
        )
    )

if __name__ == "__main__":
    client = Client()
    print(f"🔐 Logging in as {USERNAME}")
    client.login(USERNAME, APP_PASSWORD)

    recent_quotes = get_recent_quotes(client)
    post = get_random_trump_claim(recent_quotes)
    print("📢 Posting:\n", post)
    post_to_bluesky(post, client)
