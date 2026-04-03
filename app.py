import streamlit as st
import pandas as pd
import plotly.express as px

# === CONFIG ===
st.set_page_config(
    page_title="Pittsburgh Restaurant Health Score",
    page_icon="🍽️",
    layout="wide"
)

# === LOAD DATA ===
@st.cache_data
def load_data():
    df = pd.read_csv("pittsburgh_independents_final.csv")
    return df

df = load_data()

# === SIDEBAR ===
st.sidebar.title("🍽️ Filters")
neighborhoods = ["All"] + sorted(df["neighborhood"].unique().tolist())
selected_neighborhood = st.sidebar.selectbox("Neighborhood", neighborhoods)

categories = ["All"] + ["Thriving", "Stable", "At Risk", "Critical"]
selected_category = st.sidebar.selectbox("Health Category", categories)
show_chains = st.sidebar.checkbox("Include chain restaurants", value=False)

# === FILTER DATA ===
filtered = df.copy()
if selected_neighborhood != "All":
    filtered = filtered[filtered["neighborhood"] == selected_neighborhood]
if selected_category != "All":
    filtered = filtered[filtered["health_category"] == selected_category]
if not show_chains:
    filtered = filtered[filtered["is_chain"] == False]

# === HEADER ===
st.header("🎯 Business Insights for Restaurant Tech Platforms")
st.markdown("*Supporting acquisition targeting and customer retention "
            "strategies for restaurant technology companies*")
st.divider()

# === KPI METRICS ===
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Restaurants", len(df))
col2.metric("🟢 Thriving", len(df[df["health_category"]=="Thriving"]))
col3.metric("🟡 Stable", len(df[df["health_category"]=="Stable"]))
col4.metric("🟠 At Risk", len(df[df["health_category"]=="At Risk"]))
col5.metric("🔴 Critical", len(df[df["health_category"]=="Critical"]))

st.divider()

# === TWO COLUMNS LAYOUT ===
left, right = st.columns(2)

with left:
    st.subheader("Health Distribution by Neighborhood")
    neighborhood_dist = df.groupby(
        ["neighborhood","health_category"]).size().reset_index(name="count")
    color_map = {
        "Thriving": "#2ecc71",
        "Stable": "#f1c40f", 
        "At Risk": "#e67e22",
        "Critical": "#e74c3c"
    }
    fig1 = px.bar(
        neighborhood_dist,
        x="neighborhood", y="count",
        color="health_category",
        color_discrete_map=color_map,
        title="Restaurant Health by Neighborhood"
    )
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with right:
    st.subheader("Overall Health Distribution")
    dist = df["health_category"].value_counts().reset_index()
    dist.columns = ["category", "count"]
    fig2 = px.pie(
        dist, values="count", names="category",
        color="category",
        color_discrete_map=color_map,
        title="Pittsburgh Independent Restaurants"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# === RESTAURANT TABLE ===
st.subheader(f"Restaurant Explorer ({len(filtered)} restaurants)")
display_cols = ["name","neighborhood","rating","review_count",
                "recency_score","health_score","health_category"]
st.dataframe(
    filtered[display_cols].sort_values("health_score", ascending=False),
    use_container_width=True,
    hide_index=True
)
st.divider()
st.header("🎯 Business Insights for Restaurant Tech Platforms")
st.markdown("*Supporting acquisition targeting and customer retention "
            "strategies for restaurant technology companies*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 At-Risk Restaurants — Retention Priority")
    st.markdown("These restaurants show declining health signals — "
                "**high churn risk** for any restaurant technology platform. "
                "Ideal candidates for proactive outreach and support.")
    at_risk = df[
        df["health_category"].isin(["At Risk","Critical"])
    ][["name","neighborhood","health_score","recency_score","rating"]]\
    .sort_values("health_score").head(10)
    st.dataframe(at_risk, hide_index=True, use_container_width=True)

with col2:
    st.subheader("🟢 Thriving Restaurants — Acquisition Priority")
    st.markdown("Healthy, active, and growing restaurants — "
                "**prime acquisition targets** for restaurant technology platforms "
                "seeking stable, expansion-minded customers.")
    thriving = df[
        df["health_category"] == "Thriving"
    ][["name","neighborhood","health_score","recency_score","rating"]]\
    .sort_values("health_score", ascending=False).head(10)
    st.dataframe(thriving, hide_index=True, use_container_width=True)

st.divider()
st.subheader("📍 Neighborhood Opportunity Map")
neighborhood_summary = df.groupby("neighborhood").agg(
    total=("name","count"),
    thriving=("health_category", lambda x: (x=="Thriving").sum()),
    at_risk=("health_category", lambda x: 
             (x.isin(["At Risk","Critical"])).sum()),
    avg_score=("health_score","mean")
).reset_index()
neighborhood_summary["pct_thriving"] = (
    neighborhood_summary["thriving"] / 
    neighborhood_summary["total"] * 100
).round(1)
neighborhood_summary.columns = [
    "Neighborhood","Total","Thriving","At Risk/Critical",
    "Avg Health Score","% Thriving"
]
st.dataframe(
    neighborhood_summary.sort_values("% Thriving", ascending=False),
    hide_index=True,
    use_container_width=True
)
st.caption("High % Thriving = strong acquisition market. "
           "High At Risk/Critical = retention and support opportunity.")