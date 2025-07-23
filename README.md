# 🧯 TrumpFactBot

**A Bluesky bot that posts a random false or "pants on fire" claim from Donald Trump — verified by [PolitiFact](https://www.politifact.com/).**  
Because presidential fiction deserves archiving — one lie at a time.

---

## 🤖 What It Does

Every day, `TrumpFactBot`:
- Scrapes a random page from [PolitiFact's Trump fact-check archive](https://www.politifact.com/factchecks/list/?speaker=donald-trump)
- Picks a *"False"* or *"Pants on Fire!"* statement
- Checks that it hasn't posted that claim recently
- Posts it to [Bluesky](https://bsky.app/profile/trumpfactbot.bsky.social)
- If the post is too long, it threads it into two posts (quote + link)

---

## 🧪 Example Post

🔥 Trump Claim: “New York City mayoral candidate Zohran Mamdani is a communist.”
📉 Rated: False
🗓️ stated on June 25, 2025 in a Truth Social post:
🔗 https://www.politifact.com/factchecks/2025/jun/26/donald-trump/Zohran-Mamdani-democratic-socialist-communist-NYC/


---

## 🛠️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/your-username/TrumpFactBot_bsky.git
cd TrumpFactBot_bsky
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a ```.env``` file in the root folder with your bot credentials:

```bash
BSKY_USERNAME=@yourhandle.bsky.social

BSKY_APP_PASSWORD=your-app-password-here
```

# 🚀 Running the Bot
Manually:

```
python trump_bot.py
```

Automatically (Mac/Linux cron job):

```
crontab -e
```

Then add:
```
crontab -e
```

Then add:
```
0 9 * * * /path/to/your/venv/bin/python /path/to/TrumpFactBot_bsky/trump_bot.py
```
This will run it every day at 9am.

⚖️ Disclaimer
This bot is intended for educational and journalistic purposes.
All claims are sourced from publicly available fact-checks by PolitiFact.

# 🧠 Credits

Built with:

🧼 atproto

🍲 beautifulsoup4, requests

📚 PolitiFact's archives

