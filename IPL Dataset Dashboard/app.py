import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Page Configuration
st.set_page_config(
    page_title="IPL Dashboard",
    page_icon="🏏",
    layout="wide"
)


# Custom CSS Styling
st.markdown("""
<style>

/* Main App Background */
.stApp {
    background-color: #eef4ff;
}

/* Main Title */
h1 {
    color: #1e3a8a;
    text-align: center;
    font-weight: 800;
}

/* Section Headings */
h2, h3 {
    color: #2563eb;
}

/* KPI Cards */
div[data-testid="metric-container"] {
    background: white;
    border: 2px solid #dbeafe;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    transition: 0.3s ease;
}

div[data-testid="metric-container"] label {
    color: #2563eb !important;
    font-weight: bold;
}

div[data-testid="metric-container"] > div {
    color: #111827 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #2563eb 0%,
        #60a5fa 100%
    );
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* Footer */
.footer {
    text-align:center;
    color:#64748b;
    font-size:16px;
    margin-top:20px;
    padding:20px;
}

/* Main Title */
h1 {
    color: black !important;
    text-align: center;
    font-weight: 800;
}

/* All Headings */
h2, h3, h4, h5, h6 {
    color: black !important;
}

/* Normal Text */
p, label, span, div {
    color: black;
}
            
            
p, label, span, div {
    color: black;
}
            
/* Sidebar text white */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] div {
    color: white !important;
}

/* Force white text in sidebar dropdown */
[data-baseweb="popover"] * {
    color: white !important;
    background-color: #0E1117 !important;
}

/* Search box inside dropdown */
[data-baseweb="popover"] input {
    color: white !important;
    background-color: #1E1E2F !important;
}
            
/* Download button */
div[data-testid="stDownloadButton"] button {
    background-color: #87CEEB !important;
    color: black !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
}

/* Hover effect */
div[data-testid="stDownloadButton"] button:hover {
    background-color: #5dade2 !important;
    color: white !important;
}

            
</style>
""", unsafe_allow_html=True)


# Dashboard Title                                                                                                    
st.markdown("""
<h1>🏏 IPL Analytics Dashboard</h1>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center;
font-size:18px;
color:black;'>

</p>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center;
font-size:18px;
color:#475569;'>

</p>
""", unsafe_allow_html=True)


# Load Dataset
df = pd.read_csv("IPL_Dataset_Cleaned.csv")


# Sidebar Filters
st.sidebar.markdown("""
# 🎯 Dashboard Filters

Select Team and Venue
to explore IPL statistics.
""")

team = st.sidebar.selectbox(
    "🏏 Select Team",
    ["All"] + sorted(df["Team"].unique().tolist())
)

venue = st.sidebar.selectbox(
    "📍 Select Venue",
    ["All"] + sorted(df["Venue"].unique().tolist())
)

filtered_df = df.copy()

if team != "All":
    filtered_df = filtered_df[
        filtered_df["Team"] == team
    ]

if venue != "All":
    filtered_df = filtered_df[
        filtered_df["Venue"] == venue
    ]


# KPI Section
st.markdown("## 📊 Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Matches",
    filtered_df["Match_ID"].nunique()
)

col2.metric(
    "Average Runs",
    round(filtered_df["Runs"].mean(), 2)
)

col3.metric(
    "Average Strike Rate",
    round(filtered_df["Strike_Rate"].mean(), 2)
)

col4.metric(
    "Average Wickets",
    round(filtered_df["Wickets"].mean(), 2)
)

st.divider()


# Dataset Preview
st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)

st.divider()


# Team-wise Total Runs
st.subheader("🏏 Team-wise Total Runs")

team_runs = (
    filtered_df
    .groupby("Team")["Runs"]
    .sum()
)

fig, ax = plt.subplots(figsize=(9, 5))

colors = sns.color_palette(
    "viridis",
    len(team_runs)
)

team_runs.plot(
    kind="bar",
    color=colors,
    ax=ax
)

ax.set_title("Total Runs by Team")
ax.set_xlabel("Team")
ax.set_ylabel("Runs")

plt.xticks(rotation=45)

st.pyplot(fig)

 
# Winner Distribution
st.subheader("🏆 Winner Distribution")

winner = (
    filtered_df["Winner"]
    .value_counts()
)

fig, ax = plt.subplots(figsize=(7, 7))

colors = sns.color_palette(
    "Set3",
    len(winner)
)

ax.pie(
    winner,
    labels=winner.index,
    autopct="%1.1f%%",
    colors=colors,
    startangle=90,
    wedgeprops={
        "edgecolor": "white"
    }
)

ax.set_title(
    "Winner Distribution"
)

st.pyplot(fig)


# Strike Rate Distribution
st.subheader("⚡ Strike Rate Distribution")

fig, ax = plt.subplots(
    figsize=(8, 4)
)

sns.histplot(
    filtered_df["Strike_Rate"],
    bins=10,
    kde=True,
    color="orange",
    ax=ax
)

ax.set_title(
    "Strike Rate Distribution"
)

st.pyplot(fig)


# Runs vs Strike Rate
st.subheader(
    "📈 Runs vs Strike Rate"
)

fig, ax = plt.subplots(
    figsize=(9, 5)
)

sns.scatterplot(
    data=filtered_df,
    x="Runs",
    y="Strike_Rate",
    hue="Team",
    palette="tab10",
    s=120,
    ax=ax
)

ax.set_title(
    "Runs vs Strike Rate"
)

st.pyplot(fig)


# Runs Trend by Match
st.subheader(
    "📉 Runs Trend by Match ID"
)

fig, ax = plt.subplots(
    figsize=(10, 5)
)

sns.lineplot(
    data=filtered_df,
    x="Match_ID",
    y="Runs",
    marker="o",
    color="crimson",
    linewidth=3,
    ax=ax
)

ax.set_title(
    "Runs Trend by Match"
)

ax.set_xlabel(
    "Match ID"
)

ax.set_ylabel(
    "Runs"
)

st.pyplot(fig)


# Download Dataset Section
st.divider()

st.subheader("📥 Download Dataset")

st.write(
    "Download the filtered IPL dataset for further analysis."
)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv,
    file_name="IPL_Filtered_Dataset.csv",
    mime="text/csv"
)

st.info(
    "The downloaded file will contain data based on the selected filters."
)
