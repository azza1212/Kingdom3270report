import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv('C:\\Users\\jacki\\source\\repos\\PythonApplication1\\PythonApplication1\\3270 data.csv')

# Calculate total kills using the correct column names from your CSV
data['Total Kills'] = data['T1 Kills'] + data['T2 Kills'] + data['T3 Kills'] + data['T4 Kills'] + data['T5 Kills']

# Title
st.title('Kingdom 3270 Report')

# Power Ranking section sorted by Power
with st.container():
    st.subheader('Power Ranking')
    sorted_power_data = data.sort_values(by='Power', ascending=False)
    st.write(sorted_power_data[['ID', 'Name', 'Power', 'Killpoints', 'Deads', 'T1 Kills', 'T2 Kills', 'T3 Kills', 'T4 Kills', 'T5 Kills']].head(10))

# KP Overview section
with st.container():
    st.subheader('Server Total Power & KP Overview')
    fig1 = px.bar(data.nlargest(10, 'Killpoints'), x='Name', y='Killpoints', title='Top 10 Players by Killpoints')
    st.plotly_chart(fig1)

# Contributions section using corrected column names
with st.container():
    st.subheader('Contributions')
    fig2 = px.bar(data.nlargest(10, 'Rss Gathered'), x='Name', y='Rss Gathered', title='Top 10 Players by RSS Gathered')
    st.plotly_chart(fig2)

    fig3 = px.bar(data.nlargest(10, 'Rss Assistance'), x='Name', y='Rss Assistance', title='Top 10 Players by RSS Assistance')
    st.plotly_chart(fig3)

    fig4 = px.bar(data.nlargest(10, 'Helps'), x='Name', y='Helps', title='Top 10 Players by Helps')
    st.plotly_chart(fig4)

# Sidebar for search functionality
st.sidebar.title("Search Player")
search_term = st.sidebar.text_input("Enter Player Name or ID:")
if search_term:
    results = data[data['Name'].str.contains(search_term, case=False) | data['ID'].str.contains(search_term)]
    st.sidebar.write(results)
