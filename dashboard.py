import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(page_title="HR Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv('prediction.csv')
    # Clean Attrition column: replace 1.0/0.0 with labels, fill NaN with 'Retained'
    df['Attrition'] = df['Attrition'].astype(str).replace({'1.0': 'Attrited', '0.0': 'Retained'})
    df['Attrition'] = df['Attrition'].fillna('Retained')
    return df

df = load_data()

# Define probability categories (adjusted thresholds)
def prob_category(p):
    if p < 0.3:
        return 'Low'
    elif p <= 0.7:
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

# Color mapping (green for Retained, red for Attrited)
color_map = {'Retained': '#2E8B57', 'Attrited': '#E63946'}

# Helper function to create stacked bar with Retained first in legend
def stacked_bar(data, x_col, title):
    if data.empty:
        fig = px.bar(title=title)
        fig.update_layout(xaxis_title=x_col, yaxis_title='Number of Employees')
        return fig
    grouped = data.groupby([x_col, 'Attrition']).size().reset_index(name='count')
    grouped['Attrition'] = pd.Categorical(grouped['Attrition'], categories=['Retained', 'Attrited'], ordered=True)
    grouped = grouped.sort_values(['Attrition'])
    fig = px.bar(grouped, x=x_col, y='count', color='Attrition',
                 title=title,
                 color_discrete_map=color_map,
                 barmode='stack',
                 category_orders={'Attrition': ['Retained', 'Attrited']})
    fig.update_layout(xaxis_title=x_col, yaxis_title='Number of Employees', legend_title='')
    return fig

# Helper for binned stacked bars (same order)
def binned_stacked_bar(data, col, bins, labels, title):
    if data.empty:
        fig = px.bar(title=title)
        fig.update_layout(xaxis_title=col, yaxis_title='Number of Employees')
        return fig
    data_copy = data.copy()
    data_copy['bin'] = pd.cut(data_copy[col], bins=bins, labels=labels, include_lowest=True)
    grouped = data_copy.groupby(['bin', 'Attrition']).size().reset_index(name='count')
    grouped['Attrition'] = pd.Categorical(grouped['Attrition'], categories=['Retained', 'Attrited'], ordered=True)
    grouped = grouped.sort_values(['Attrition'])
    fig = px.bar(grouped, x='bin', y='count', color='Attrition',
                 title=title,
                 color_discrete_map=color_map,
                 barmode='stack',
                 category_orders={'Attrition': ['Retained', 'Attrited']})
    fig.update_layout(xaxis_title=col, yaxis_title='Number of Employees', legend_title='')
    return fig

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

# ---------- Row 2: Three Stacked Bar Charts ----------
st.markdown("## Attrition by Key Dimensions")
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(stacked_bar(filtered_df, 'Department', 'Department'), use_container_width=True)
with col2:
    st.plotly_chart(stacked_bar(filtered_df, 'OverTime', 'OverTime'), use_container_width=True)
with col3:
    st.plotly_chart(stacked_bar(filtered_df, 'Gender', 'Gender'), use_container_width=True)

# ---------- Row 3: Heatmap of Average Predicted Probability ----------
st.markdown("## Predicted Attrition Probability by Survey Factor and Score")
if filtered_df.empty:
    st.info("No data available with the current filters.")
else:
    factors = ['JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance', 'RelationshipSatisfaction']
    heatmap_data = []
    for factor in factors:
        grouped = filtered_df.groupby(factor)['Probability_Attrition'].mean().reset_index()
        for _, row in grouped.iterrows():
            heatmap_data.append({
                'Factor': factor,
                'Score': row[factor],
                'Avg Probability': row['Probability_Attrition']
            })
    heatmap_df = pd.DataFrame(heatmap_data)
    if heatmap_df.empty:
        st.info("No survey data available.")
    else:
        heatmap_pivot = heatmap_df.pivot(index='Factor', columns='Score', values='Avg Probability')
        heatmap_pivot = heatmap_pivot.reindex(columns=[1,2,3,4], fill_value=0)
        fig_heat = px.imshow(heatmap_pivot,
                             text_auto='.2f',
                             color_continuous_scale=['#2E8B57', '#FFD700', '#E63946'],
                             labels=dict(x="Score", y="Factor", color="Avg Probability"),
                             title="Average Predicted Probability of Attrition")
        fig_heat.update_layout(xaxis=dict(tickmode='linear', tickvals=[1,2,3,4]),
                               yaxis=dict(tickmode='linear', tickvals=list(range(len(factors))), ticktext=factors),
                               coloraxis_colorbar=dict(title="Prob."))
        st.plotly_chart(fig_heat, use_container_width=True)

# ---------- Row 4: Additional Correlation Visuals ----------
st.markdown("## Additional Factors & Attrition")
if not filtered_df.empty:
    age_bins = [0, 25, 35, 45, 55, 100]
    age_labels = ['<25', '25-34', '35-44', '45-54', '55+']
    tenure_bins = [0, 2, 5, 10, 20, 50]
    tenure_labels = ['<2', '2-4', '5-9', '10-19', '20+']
    distance_bins = [0, 5, 10, 20, 50]
    distance_labels = ['<5', '5-9', '10-19', '20+']
    income_bins = [0, 3000, 6000, 10000, 20000, 50000]
    income_labels = ['<3k', '3k-6k', '6k-10k', '10k-20k', '>20k']

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(binned_stacked_bar(filtered_df, 'Age', age_bins, age_labels, 'Age Distribution'), use_container_width=True)
        st.plotly_chart(binned_stacked_bar(filtered_df, 'YearsAtCompany', tenure_bins, tenure_labels, 'Years at Company'), use_container_width=True)
    with col2:
        st.plotly_chart(binned_stacked_bar(filtered_df, 'DistanceFromHome', distance_bins, distance_labels, 'Distance from Home (miles)'), use_container_width=True)
        st.plotly_chart(binned_stacked_bar(filtered_df, 'MonthlyIncome', income_bins, income_labels, 'Monthly Income'), use_container_width=True)
else:
    st.info("No data available to display additional factors.")

# ---------- Row 5: Employee Table ----------
st.markdown("## Employee Details")
if not filtered_df.empty:
    table_df = filtered_df[['EmployeeId', 'JobRole', 'Prob_Category', 'Attrition']].copy()
    # Sort by probability category (Low, Medium, High) but within that maybe by probability descending
    # To sort by category order, we can map to numeric
    cat_order = {'Low': 1, 'Medium': 2, 'High': 3}
    table_df['sort_order'] = table_df['Prob_Category'].map(cat_order)
    table_df = table_df.sort_values(['sort_order', 'EmployeeId'], ascending=[False, True])
    table_df = table_df.drop(columns='sort_order')
    st.dataframe(table_df, use_container_width=True)
else:
    st.info("No employee data with current filters.")

# Footer
st.markdown("---")
st.caption("Data source: prediction.csv | Dashboard built with Streamlit")