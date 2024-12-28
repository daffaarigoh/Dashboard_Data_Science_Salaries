import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# Set Streamlit page config
st.set_page_config(
    page_title="Data Scientist Salary Insights",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the look
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .stPlotlyChart {
        background-color: #ffffff;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('./DataScience_salaries_2024.csv')
    return df

data = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Experience level filter
exp_level = st.sidebar.multiselect(
    "Select Experience Level",
    options=sorted(data['experience_level'].unique()),
    default=sorted(data['experience_level'].unique())
)

# Remote ratio filter
remote_options = st.sidebar.multiselect(
    "Select Remote Work Ratio",
    options=sorted(data['remote_ratio'].unique()),
    default=sorted(data['remote_ratio'].unique())
)

# Filter data based on selections
filtered_data = data[
    (data['experience_level'].isin(exp_level)) &
    (data['remote_ratio'].isin(remote_options))
]

# Main content
st.title("🔍 Data Scientist Salary Insights Dashboard")

# Key metrics in columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Average Salary",
        f"${filtered_data['salary_in_usd'].mean():,.0f}",
        f"{filtered_data['salary_in_usd'].mean() / data['salary_in_usd'].mean() * 100 - 100:.1f}% vs Overall"
    )
with col2:
    st.metric(
        "Highest Salary",
        f"${filtered_data['salary_in_usd'].max():,.0f}"
    )
with col3:
    st.metric(
        "Number of Positions",
        f"{len(filtered_data):,}"
    )

# Tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["📊 Salary Analysis", "🌍 Geographic Insights", "📈 Trends"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Interactive Experience Level Plot using Plotly
        fig_exp = px.box(
            filtered_data,
            x='experience_level',
            y='salary_in_usd',
            title='Salary Distribution by Experience Level',
            color='experience_level'
        )
        fig_exp.update_layout(showlegend=False)
        st.plotly_chart(fig_exp, use_container_width=True)
    
    with col2:
        # Interactive Remote Ratio Plot
        fig_remote = px.violin(
            filtered_data,
            x='remote_ratio',
            y='salary_in_usd',
            title='Salary Distribution by Remote Work Ratio',
            color='remote_ratio'
        )
        fig_remote.update_layout(showlegend=False)
        st.plotly_chart(fig_remote, use_container_width=True)

with tab2:
    # World map of salaries
    avg_salary_by_country = filtered_data.groupby('company_location')['salary_in_usd'].mean().reset_index()
    fig_map = px.choropleth(
        avg_salary_by_country,
        locations='company_location',
        locationmode='ISO-3',
        color='salary_in_usd',
        title='Average Salaries Around the World',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Top 10 countries bar chart
    top_countries = avg_salary_by_country.nlargest(10, 'salary_in_usd')
    fig_top = px.bar(
        top_countries,
        x='company_location',
        y='salary_in_usd',
        title='Top 10 Countries by Average Salary',
        color='salary_in_usd',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_top, use_container_width=True)

with tab3:
    # Add year-over-year trend if your dataset includes this information
    if 'work_year' in filtered_data.columns:
        yearly_trend = filtered_data.groupby('work_year')['salary_in_usd'].agg(['mean', 'median']).reset_index()
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=yearly_trend['work_year'],
            y=yearly_trend['mean'],
            name='Mean Salary',
            line=dict(color='#1f77b4')
        ))
        fig_trend.add_trace(go.Scatter(
            x=yearly_trend['work_year'],
            y=yearly_trend['median'],
            name='Median Salary',
            line=dict(color='#ff7f0e')
        ))
        fig_trend.update_layout(
            title='Salary Trends Over Time',
            xaxis_title='Year',
            yaxis_title='Salary (USD)'
        )
        st.plotly_chart(fig_trend, use_container_width=True)

# Additional insights
st.subheader("📊 Detailed Salary Analysis")
if st.checkbox("Show Detailed Statistics"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Summary Statistics")
        st.dataframe(filtered_data['salary_in_usd'].describe())
    
    with col2:
        st.write("Salary Distribution")
        fig_hist = px.histogram(
            filtered_data,
            x='salary_in_usd',
            nbins=50,
            title='Salary Distribution'
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# Add data table with search
st.subheader("🔍 Raw Data Explorer")
if st.checkbox("Show Raw Data"):
    st.dataframe(
        filtered_data,
        use_container_width=True,
        height=400
    )
