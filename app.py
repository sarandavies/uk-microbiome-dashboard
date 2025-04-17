
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide")

# ✅ Load cleaned data
df = pd.read_csv("/Users/saran/uk-microbiome-dashboard/UK_Microbiome_Organisations_CLEANED.csv")

# ✅ Only keep rows with coordinates
df = df[df["Latitude"].notna() & df["Longitude"].notna()].copy()

# ✅ Sidebar filters
relevant_only = st.sidebar.checkbox("Show only Relevant companies", value=False)
if relevant_only:
    df = df[df["Relevant"] == 1]

sector_filter = st.sidebar.multiselect("Filter by Sector", options=df["Sector"].dropna().unique())
target_filter = st.sidebar.multiselect("Filter by Target Area", options=df["Target_Area"].dropna().unique())

# ✅ Apply filters
filtered_df = df.copy()
if sector_filter:
    filtered_df = filtered_df[filtered_df["Sector"].isin(sector_filter)]
if target_filter:
    filtered_df = filtered_df[filtered_df["Target_Area"].isin(target_filter)]

# ✅ Add jitter to coordinates to reduce overlap
np.random.seed(42)
filtered_df["Latitude"] += np.random.uniform(-0.05, 0.05, size=len(filtered_df))
filtered_df["Longitude"] += np.random.uniform(-0.05, 0.05, size=len(filtered_df))

# ✅ Header
st.title("UK Microbiome Landscape Dashboard")
st.markdown("Explore microbiome-related companies across the UK by target area, sector, and funding stage.")

# ✅ Display number of companies
st.metric("Companies displayed", len(filtered_df))

# ✅ Map
st.subheader("Map of UK Microbiome Companies")
fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Organisation",
    hover_data={
        "Town": True,
        "Target_Area": True,
        "Sector": True,
        "Latitude": False,
        "Longitude": False
    },
    color="Target_Area",
    zoom=5,
    height=600
)
fig.update_traces(marker=dict(size=12))
fig.update_layout(mapbox_style="carto-positron", margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# ✅ Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribution by Target Area")
    target_counts = filtered_df["Target_Area"].value_counts()
    fig1 = px.bar(
        x=target_counts.index,
        y=target_counts.values,
        labels={"x": "Target Area", "y": "Count"}
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Funding Stage Breakdown")
    funding_counts = filtered_df["Funding_Stage"].value_counts()
    fig2 = px.pie(
        values=funding_counts.values,
        names=funding_counts.index,
        title="Funding Stage",
        hole=0.3
    )
    st.plotly_chart(fig2, use_container_width=True)

# ✅ Table
st.subheader("Company Summary Table")
st.dataframe(filtered_df[["Organisation", "Town", "Target_Area", "Sector", "Funding_Stage"]].reset_index(drop=True))
# last updated: fixed funding stage pie issue
