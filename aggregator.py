# aggregator.py
import pandas as pd
from sqlalchemy import create_engine
import os

DB_URL = os.getenv("SENTILYST_DB_URL", "sqlite:///sentilyst.db")

def persist_raw(df, table="raw_texts"):
    engine = create_engine(DB_URL)
    df.to_sql(table, engine, if_exists="append", index=False)

def aggregate_daily(df):
    df["date"] = pd.to_datetime(df["date"])
    df["ds"] = df["date"].dt.date
    daily = df.groupby("ds")["sentiment_score"].mean().reset_index().rename(columns={"sentiment_score":"y"})
    daily["ds"] = pd.to_datetime(daily["ds"])
    return daily

def load_aggregated():
    engine = create_engine(DB_URL)
    try:
        df = pd.read_sql_table("daily", engine)
        df["ds"] = pd.to_datetime(df["ds"])
        return df
    except Exception:
        return pd.DataFrame(columns=["ds","y"])

def persist_aggregated(daily_df):
    engine = create_engine(DB_URL)
    daily_df.to_sql("daily", engine, if_exists="replace", index=False)
