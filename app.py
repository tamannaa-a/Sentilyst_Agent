# app.py
import streamlit as st
from agent import make_agent
from aggregator import load_aggregated
import pandas as pd
import os
from sentiment_model import SentimentModel
from actions import post_slack

st.set_page_config(layout="wide", page_title="Sentilyst Agent")
st.title("Sentilyst — Agentic Sentiment Forecasting")

# left: controls; right: charts and chat
col1, col2 = st.columns([1,2])

with col1:
    st.header("Controls")
    if st.button("Reload aggregated data"):
        st.session_state["agg"] = load_aggregated()
    days = st.slider("Forecast horizon (days)", 7, 90, 30)
    if st.button("Run forecast now"):
        df = load_aggregated()
        if df.empty or len(df) < 5:
            st.warning("Not enough data to forecast")
        else:
            from forecaster import train_prophet, predict_prophet
            m = train_prophet(df)
            fc = predict_prophet(m, periods=days)
            st.session_state["forecast"] = fc

    st.markdown("---")
    st.header("Agent")
    if "agent" not in st.session_state:
        st.session_state["agent"] = make_agent(os.getenv("OPENAI_API_KEY", None))
    query = st.text_input("Ask the agent (e.g., 'Alert me if sentiment < -0.5 next 7 days')")

    if st.button("Send to agent"):
        if query:
            with st.spinner("Agent thinking..."):
                agent = st.session_state["agent"]
                resp = agent.run(query)
            st.session_state.setdefault("agent_history", []).append(("User", query))
            st.session_state["agent_history"].append(("Agent", resp))

with col2:
    st.header("Time Series")
    agg = st.session_state.get("agg", load_aggregated())
    if not agg.empty:
        st.line_chart(agg.set_index("ds")["y"])
    else:
        st.info("No aggregated data available yet. Run the pipeline to collect data.")

    if "forecast" in st.session_state:
        st.header("Forecast (yhat)")
        st.line_chart(st.session_state["forecast"].set_index("ds")["yhat"].tail(days))

    st.header("Agent Chat")
    history = st.session_state.get("agent_history", [])
    for who, text in history[-10:]:
        if who == "User":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(f"**Agent:** {text}")
