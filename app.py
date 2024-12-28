import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Data Scientist Salary Insights", layout="wide")

# Load data
@st.cache
def load_data():
    return pd.read_csv('DataScience_salaries_2024.csv')

data = load_data()

# Title and description
st.title("Data Scientist Salary Insights")
st.write("""
Explore insights into salaries for Data Scientists, including variations by experience level, remote ratio, 
and the top-paying countries.
""")

# Visualization: Average salary by experience level
st.subheader("Average Salary by Experience Level")
fig1, ax1 = plt.subplots(figsize=(8, 5))
sns.barplot(data=data, x='experience_level', y='salary_in_usd', ax=ax1, palette="viridis")
ax1.set_title("Average Salary by Experience Level")
ax1.set_xlabel("Experience Level")
ax1.set_ylabel("Average Salary (USD)")
st.pyplot(fig1)

# Visualization: Average salary by remote ratio
st.subheader("Average Salary by Remote Ratio")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(data=data, x='remote_ratio', y='salary_in_usd', ax=ax2, palette="muted")
ax2.set_title("Average Salary by Remote Ratio")
ax2.set_xlabel("Remote Ratio")
ax2.set_ylabel("Average Salary (USD)")
st.pyplot(fig2)

# Visualization: Top-paying countries
st.subheader("Top 10 Countries Offering Highest Average Salaries")
avg_salary_by_country = data.groupby('company_location')['salary_in_usd'].mean().sort_values(ascending=False)
top_countries = avg_salary_by_country.head(10)
fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.barplot(x=top_countries.values, y=top_countries.index, palette="coolwarm", ax=ax3)
ax3.set_title("Top 10 Countries with Highest Average Salaries")
ax3.set_xlabel("Average Salary (USD)")
ax3.set_ylabel("Country")
st.pyplot(fig3)
