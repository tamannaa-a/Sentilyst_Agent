# agent.py
import os
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.agents import load_tools
from actions import post_slack, send_email, save_report_text
from aggregator import load_aggregated, persist_aggregated
from forecaster import train_prophet, predict_prophet
import pandas as pd

# Minimal tool wrappers for LangChain
def tool_get_latest_trend(limit=30):
    df = load_aggregated()
    return df.tail(limit).to_json(orient="records", date_format="iso")

def tool_forecast(days=14):
    df = load_aggregated()
    if df.empty or len(df) < 5:
        return "Not enough data for forecasting (need >=5 daily points)."
    m = train_prophet(df)
    fc = predict_prophet(m, periods=days)
    out = fc[["ds","yhat","yhat_lower","yhat_upper"]].tail(days)
    return out.to_json(orient="records", date_format="iso")

# wrap external actions
def tool_post_slack(msg):
    r = post_slack(msg)
    return str(r)

def tool_send_email(args_json):
    # args_json must contain to, subject, body
    import json
    args = json.loads(args_json)
    return str(send_email(args["to"], args["subject"], args["body"]))

def tool_save_report(text):
    r = save_report_text(text)
    return str(r)

TOOLS = [
    Tool(name="latest_trend", func=tool_get_latest_trend, description="Return latest daily sentiment trend as JSON"),
    Tool(name="forecast", func=tool_forecast, description="Forecast future sentiment, input days as integer"),
    Tool(name="post_slack", func=tool_post_slack, description="Post a slack message"),
    Tool(name="send_email", func=tool_send_email, description="Send an email; input a JSON string with to, subject, body"),
    Tool(name="save_report", func=tool_save_report, description="Save plain-text report"),
]

def make_agent(openai_api_key=None):
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    llm = OpenAI(temperature=0, max_tokens=400)
    agent = initialize_agent(TOOLS, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
    return agent
