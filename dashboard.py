import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide")

# Load data from GitHub raw URL
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/prediction.csv"
    df = pd.read_csv(url)
    # Ensure Attrition is string for filtering
    df["Attrition"] = df["Attrition"].astype(str).replace({"1.0": "Attrited", "0.0": "Retained", "nan": "Unknown"})
    return df

df = load_data()

# Sidebar filter: attrition status
attrition_filter = st.sidebar.selectbox(
    "Filter by Attrition Status",
    options=["All", "Attrited", "Retained"]
)

if attrition_filter != "All":
    df = df[df["Attrition"] == attrition_filter]

# ----- Main Dashboard -----
st.title("📊 Employee Attrition Dashboard")
st.markdown("Data-driven insights on key attrition drivers")

# Top metrics
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Employees", f"{len(df):,}")
with col2:
    attrition_count = len(df[df["Attrition"] == "Attrited"])
    st.metric("Attrited", attrition_count)
with col3:
    retention_count = len(df[df["Attrition"] == "Retained"])
    st.metric("Retained", retention_count)
with col4:
    attrition_rate = (attrition_count / len(df)) * 100 if len(df) > 0 else 0
    st.metric("Attrition Rate", f"{attrition_rate:.1f}%")
with col5:
    avg_age = df["Age"].mean()
    st.metric("Avg Age", f"{avg_age:.1f}")

# Row 1: Monthly Income & Age
st.subheader("1. Monthly Income & Age")
col1, col2 = st.columns(2)

with col1:
    # Monthly Income distribution by attrition
    fig_income = px.box(df, x="Attrition", y="MonthlyIncome", 
                        title="Monthly Income by Attrition Status",
                        color="Attrition", 
                        color_discrete_map={"Attrited": "red", "Retained": "blue"})
    st.plotly_chart(fig_income, use_container_width=True)

with col2:
    # Age group attrition
    df["Age Group"] = pd.cut(df["Age"], bins=[0, 24, 29, 39, 49, 100], 
                             labels=["<25", "25-29", "30-39", "40-49", "50+"])
    age_group_attrition = df.groupby("Age Group")["Attrition"].value_counts(normalize=True).unstack().fillna(0) * 100
    fig_age = px.bar(age_group_attrition, x=age_group_attrition.index, y=["Attrited", "Retained"],
                     title="Attrition Rate by Age Group",
                     labels={"value": "Percentage", "Age Group": "Age Group"},
                     barmode="group",
                     color_discrete_map={"Attrited": "red", "Retained": "blue"})
    st.plotly_chart(fig_age, use_container_width=True)

# Row 2: Overtime
st.subheader("2. Overtime Impact")
col1, col2 = st.columns(2)

with col1:
    ot_attrition = df.groupby("Overtime")["Attrition"].value_counts(normalize=True).unstack().fillna(0) * 100
    fig_ot = px.bar(ot_attrition, x=ot_attrition.index, y=["Attrited", "Retained"],
                    title="Attrition Rate by Overtime",
                    labels={"value": "Percentage", "Overtime": "Overtime"},
                    barmode="group",
                    color_discrete_map={"Attrited": "red", "Retained": "blue"})
    st.plotly_chart(fig_ot, use_container_width=True)

with col2:
    # Overtime by department
    ot_dept = df.groupby(["Department", "Overtime"]).size().unstack().fillna(0)
    fig_ot_dept = px.bar(ot_dept, x=ot_dept.index, y=["Yes", "No"],
                         title="Overtime Count by Department",
                         labels={"value": "Employee Count", "Department": "Department"},
                         barmode="group",
                         color_discrete_map={"Yes": "orange", "No": "green"})
    st.plotly_chart(fig_ot_dept, use_container_width=True)

# Row 3: Monthly Rate & Daily Rate
st.subheader("3. Variable Compensation (Monthly Rate) & Hourly Equity (Daily Rate)")
col1, col2 = st.columns(2)

with col1:
    fig_mrate = px.box(df, x="Attrition", y="MonthlyRate",
                       title="Monthly Rate Distribution by Attrition Status",
                       color="Attrition",
                       color_discrete_map={"Attrited": "red", "Retained": "blue"})
    st.plotly_chart(fig_mrate, use_container_width=True)

with col2:
    # Daily Rate vs Job Satisfaction
    fig_drate = px.scatter(df, x="DailyRate", y="JobSatisfaction", 
                           color="Attrition", 
                           title="Daily Rate vs Job Satisfaction",
                           labels={"DailyRate": "Daily Rate ($)", "JobSatisfaction": "Job Satisfaction (1-4)"},
                           color_discrete_map={"Attrited": "red", "Retained": "blue"},
                           opacity=0.6)
    st.plotly_chart(fig_drate, use_container_width=True)

# Additional: Key insights table (optional)
st.subheader("4. Key Statistics by Attrition Status")
grouped = df.groupby("Attrition").agg({
    "MonthlyIncome": "mean",
    "Age": "mean",
    "MonthlyRate": "mean",
    "DailyRate": "mean",
    "Overtime": lambda x: (x == "Yes").mean() * 100
}).round(1)
grouped.columns = ["Avg Monthly Income", "Avg Age", "Avg Monthly Rate", "Avg Daily Rate", "% Overtime"]
st.dataframe(grouped)

# Footer
st.markdown("---")
st.caption("Data source: prediction.csv | Dashboard created with Streamlit")