import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(page_title="Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('prediction.csv')
    # Attrition: treat NaN/empty as Retained
    df['Attrition'] = df['Attrition'].astype(str).replace({'1.0': 'Attrited', '0.0': 'Retained'})
    df['Attrition'] = df['Attrition'].fillna('Retained')
    return df

df = load_data()

# Create probability category
def prob_category(p):
    if p < 0.4:
        return 'Low'
    elif p < 0.7:
        return 'Medium'
    else:
        return 'High'

df['Prob_Category'] = df['Probability_Attrition'].apply(prob_category)

# Sidebar filters
st.sidebar.header("Filters")
attrition_filter = st.sidebar.selectbox(
    "Attrition Status",
    options=['All', 'Attrited', 'Retained']
)
prob_filter = st.sidebar.multiselect(
    "Predicted Probability Category",
    options=['Low', 'Medium', 'High'],
    default=['Low', 'Medium', 'High']
)

# Apply filters
filtered_df = df.copy()
if attrition_filter != 'All':
    filtered_df = filtered_df[filtered_df['Attrition'] == attrition_filter]
filtered_df = filtered_df[filtered_df['Prob_Category'].isin(prob_filter)]

# ---------- Row 1: KPI ----------
st.markdown("## Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Employees", len(filtered_df))
with col2:
    attrited = len(filtered_df[filtered_df['Attrition'] == 'Attrited'])
    st.metric("Attrited", attrited)
with col3:
    retained = len(filtered_df[filtered_df['Attrition'] == 'Retained'])
    st.metric("Retained", retained)
with col4:
    rate = (attrited / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric("Attrition Rate", f"{rate:.1f}%")
with col5:
    avg_prob = filtered_df['Probability_Attrition'].mean()
    st.metric("Avg Predicted Probability", f"{avg_prob:.3f}")

# ---------- Row 2: Salary metrics with stacked bar (by Attrition) ----------
st.markdown("## Salary Metrics by Attrition")
col1, col2, col3 = st.columns(3)

# Helper to create stacked bar for a salary column
def salary_stacked_bar(df, col_name, title, bin_labels, bin_edges):
    df_copy = df.copy()
    df_copy['bin'] = pd.cut(df_copy[col_name], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Count per bin and attrition
    grouped = df_copy.groupby(['bin', 'Attrition']).size().reset_index(name='count')
    fig = px.bar(grouped, x='bin', y='count', color='Attrition',
                 title=title,
                 color_discrete_map={'Attrited': '#E63946', 'Retained': '#1E6091'},
                 barmode='stack')
    fig.update_layout(xaxis_title='Income Bracket', yaxis_title='Number of Employees', legend_title='')
    return fig

# Define bins (adjust as needed based on data distribution)
# Monthly Income bins
income_bins = [0, 3000, 6000, 10000, 20000, 50000]
income_labels = ['<3k', '3k-6k', '6k-10k', '10k-20k', '>20k']
# Monthly Rate bins
rate_bins = [0, 10000, 20000, 30000, 50000]
rate_labels = ['<10k', '10k-20k', '20k-30k', '>30k']
# Daily Rate bins
daily_bins = [0, 500, 1000, 1500, 2000]
daily_labels = ['<500', '500-1000', '1000-1500', '>1500']

with col1:
    fig_income = salary_stacked_bar(filtered_df, 'MonthlyIncome', 'Monthly Income', income_labels, income_bins)
    st.plotly_chart(fig_income, use_container_width=True)
with col2:
    fig_rate = salary_stacked_bar(filtered_df, 'MonthlyRate', 'Monthly Rate', rate_labels, rate_bins)
    st.plotly_chart(fig_rate, use_container_width=True)
with col3:
    fig_daily = salary_stacked_bar(filtered_df, 'DailyRate', 'Daily Rate', daily_labels, daily_bins)
    st.plotly_chart(fig_daily, use_container_width=True)

# ---------- Row 3: Heatmap of predicted probability by survey factor and score ----------
st.markdown("## Predicted Probability by Survey Factor and Score")
factors = ['JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance', 'RelationshipSatisfaction']
# Prepare a list to hold data
heatmap_data = []
for factor in factors:
    # Group by factor score, compute mean probability
    grouped = filtered_df.groupby(factor)['Probability_Attrition'].mean().reset_index()
    grouped['Factor'] = factor
    grouped.columns = ['Score', 'Avg_Probability', 'Factor']
    heatmap_data.append(grouped)
if heatmap_data:
    heatmap_df = pd.concat(heatmap_data, ignore_index=True)
    # Pivot to get factor as rows, score as columns, values = avg probability
    heatmap_pivot = heatmap_df.pivot(index='Factor', columns='Score', values='Avg_Probability')
    # Ensure all scores 1-4 are present
    all_scores = [1,2,3,4]
    heatmap_pivot = heatmap_pivot.reindex(columns=all_scores, fill_value=0)
    # Create heatmap
    fig_heat = px.imshow(heatmap_pivot,
                         text_auto='.2f',
                         color_continuous_scale=['#FDE2E2', '#E63946'],
                         labels=dict(x="Score", y="Factor", color="Avg Predicted Probability"),
                         title="Average Predicted Probability by Survey Factor and Score")
    fig_heat.update_layout(xaxis=dict(tickmode='linear', tickvals=all_scores),
                           yaxis=dict(tickmode='linear', tickvals=list(range(len(factors))), ticktext=factors),
                           coloraxis_colorbar=dict(title="Probability"))
    st.plotly_chart(fig_heat, use_container_width=True)
else:
    st.warning("No data available for the selected filters.")

# ---------- Row 4: Employee Table with Filters ----------
st.markdown("## Employee Details")
# Prepare table columns
table_df = filtered_df[['EmployeeId', 'Age', 'JobRole', 'MonthlyIncome', 'Probability_Attrition', 'Prob_Category', 'Attrition']].copy()
table_df = table_df.sort_values('Probability_Attrition', ascending=False)
st.dataframe(table_df, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Data source: prediction.csv | Dashboard created with Streamlit")