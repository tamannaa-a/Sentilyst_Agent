# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from collector import collect_loop
from sentiment_model import SentimentModel
from aggregator import persist_raw, aggregate_daily, persist_aggregated
import pandas as pd
import os

MODEL = SentimentModel()

def pipeline_run(config):
    print("Pipeline started...")
    df = collect_loop(config)
    if df.empty:
        print("No texts collected.")
        return
    # score
    scored = MODEL.score_texts(df["text"].astype(str).tolist())
    # attach metadata back
    scored["date"] = pd.to_datetime(df["date"]).reset_index(drop=True)
    persist_raw(scored)
    # aggregate
    engine_df = scored[["date","sentiment_score"]]
    daily = aggregate_daily(engine_df)
    persist_aggregated(daily)
    print("Pipeline finished. persisted {} raw rows and {} daily rows".format(len(scored), len(daily)))

def start_scheduler(config, interval_minutes=60):
    sched = BackgroundScheduler()
    sched.add_job(lambda: pipeline_run(config), "interval", minutes=interval_minutes, id="sentilyst_pipeline")
    sched.start()
    print("Scheduler started.")

if __name__ == "__main__":
    # example config
    cfg = {"mode":"twitter", "twitter":{"query":"productX since:2025-07-01 until:2025-10-01","limit":200}}
    start_scheduler(cfg, interval_minutes=60)
    import time
    while True:
        time.sleep(60)
