import os
import tweepy
from openai import OpenAI

# === Load secrets from environment variables ===
TWITTER_API_KEY = os.environ["TWITTER_API_KEY"]
TWITTER_API_SECRET = os.environ["TWITTER_API_SECRET"]
TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
TWITTER_ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# === Set up API clients ===
client_x = tweepy.Client(
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_SECRET
)

client_ai = OpenAI(api_key=OPENAI_API_KEY)

# === Generate a tweet with OpenAI ===
def generate_tweet():
    prompt ="""
    Write a tweet (<240 chars) from a senior data scientist in forecasting/ops research. 
    Randomly choose between (a) share a painful mistake, (b) share a surprising success, (c) share a counterintuitive insight, or (d) draw a parallel with current AI trends.
    Always make it natural, no emojis, include 1–2 hashtags
    """
    response = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.choices[0].message.content.strip()
    return text  # enforce length limit

# === Post the tweet ===
def post_tweet():
    text = generate_tweet()
    resp = client_x.create_tweet(text=text)
    print("Posted tweet:", resp.data["id"])
    print("Content:", text)

# === Entry point ===
if __name__ == "__main__":
    post_tweet()
