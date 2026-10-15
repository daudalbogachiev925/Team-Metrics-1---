import streamlit as st
import pandas as pd
import plotly.express as px
from src.dora import dora_score, classify_dora
from src.velocity import velocity, velocity_trend, predictability, committed_vs_done
from src.code_churn import churn_rate, author_churn, hotspot_analysis
from src.bug_rate import bug_rate, reopened_ratio, bug_by_severity, bug_by_module
from src.load import load_per_developer, unbalanced_load, estimation_accuracy
from src.collector import (
    generate_dora_data, generate_sprints, generate_commits,
    generate_bugs, generate_tasks)

st.set_page_config(page_title="Team Metrics", layout="wide")
st.title("Team Metrics — 1C Team")

@st.cache_data
def load_all():
    deploys, incidents = generate_dora_data()
    return {
        "deployments": deploys,
        "incidents": incidents,
        "sprints": generate_sprints(),
        "commits": generate_commits(),
        "bugs": generate_bugs(),
        "tasks": generate_tasks(),
    }

data = load_all()
tabs = st.tabs(["DORA", "Velocity", "Code Churn", "Bugs", "Load"])

with tabs[0]:
    m = dora_score(data["deployments"], data["incidents"])
    levels = classify_dora(m)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Deploy/day", m["deployment_frequency_per_day"], levels["deployment_frequency"])
    c2.metric("Lead Time (h)", m["lead_time_hours"], levels["lead_time"])
    c3.metric("CFR %", m["change_failure_rate_pct"], levels["change_failure_rate"])
    c4.metric("MTTR (h)", m["mttr_hours"], levels["mttr"])
    st.json(levels)

with tabs[1]:
    sprints = data["sprints"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Velocity", velocity(sprints))
    c2.metric("Trend %", velocity_trend(sprints))
    c3.metric("Predictability %", predictability(sprints))
    df = pd.DataFrame(committed_vs_done(sprints))
    st.dataframe(df)
    fig = px.bar(df, x="sprint", y=["planned", "done"], barmode="group")
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    commits = data["commits"]
    st.metric("Churn Rate %", churn_rate(commits))
    st.subheader("Author churn")
    st.dataframe(pd.DataFrame(author_churn(commits)).T)
    st.subheader("Hotspots")
    st.dataframe(pd.DataFrame(hotspot_analysis(commits)))

with tabs[3]:
    bugs = data["bugs"]
    c1, c2 = st.columns(2)
    c1.metric("Reopened %", reopened_ratio(bugs))
    c2.metric("Bug Rate (per sprint)", bug_rate(bugs, len(data["sprints"])))
    st.subheader("By severity")
    st.bar_chart(pd.Series(bug_by_severity(bugs)))
    st.subheader("By module")
    st.bar_chart(pd.Series(bug_by_module(bugs)))

with tabs[4]:
    tasks = data["tasks"]
    load = load_per_developer(tasks)
    st.dataframe(pd.DataFrame(load).T)
    st.subheader("Unbalanced")
    st.dataframe(pd.DataFrame(unbalanced_load(load)))
    st.metric("Estimation Accuracy %", estimation_accuracy(tasks))
