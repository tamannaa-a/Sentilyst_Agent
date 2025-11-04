# collector.py
import pandas as pd
from datetime import datetime, timedelta
import snscrape.modules.twitter as sntwitter
import os

def scrape_twitter(query, since=None, until=None, limit=1000):
    # query example: "productX OR #productX since:2025-01-01 until:2025-10-01"
    results = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= limit:
            break
        results.append({
            "id": tweet.id,
            "date": tweet.date,
            "text": tweet.content,
            "username": tweet.user.username,
            "retweetCount": tweet.retweetCount,
            "likeCount": tweet.likeCount
        })
    return pd.DataFrame(results)

def load_csv(path):
    df = pd.read_csv(path)
    if "date" not in df.columns:
        df["date"] = pd.to_datetime("now")
    else:
        df["date"] = pd.to_datetime(df["date"])
    return df

def collect_loop(config):
    """
    config: dict with keys:
      - 'mode': 'twitter' or 'csv'
      - twitter: {query, limit}
      - csv: {path}
    """
    mode = config.get("mode","twitter")
    if mode == "twitter":
        q = config["twitter"]["query"]
        limit = config["twitter"].get("limit", 500)
        df = scrape_twitter(q, limit=limit)
    else:
        df = load_csv(config["csv"]["path"])
    # normalize columns
    df = df.rename(columns={"content":"text"}, errors="ignore")
    df["date"] = pd.to_datetime(df["date"])
    return df
