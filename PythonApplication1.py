import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
data = pd.read_csv('C:\\Users\\jacki\\source\\repos\\PythonApplication1\\PythonApplication1\\3270 data.csv')

# Ensure 'ID' column is treated as string
data['ID'] = data['ID'].astype(str)

# Calculate total kills using the correct column names from your CSV
data['Total Kills'] = data['T1 Kills'] + data['T2 Kills'] + data['T3 Kills'] + data['T4 Kills'] + data['T5 Kills']

# Revised DKP formula using available columns
data['DKP'] = (data['T4 Kills'] * 1) + (data['T5 Kills'] * 2) + (data['Deads'] * 2)

# Title
st.markdown('<h1 style="color: orange;">Kingdom 3270 Report</h1>', unsafe_allow_html=True)

# Power Ranking section sorted by Power
with st.container():
    st.markdown('<h2 style="color: purple;">Power Ranking</h2>', unsafe_allow_html=True)
    sorted_power_data = data.sort_values(by='Power', ascending=False)
    st.write(sorted_power_data[['ID', 'Name', 'Power', 'Killpoints', 'Deads', 'T1 Kills', 'T2 Kills', 'T3 Kills', 'T4 Kills', 'T5 Kills']].head(10))

# KP Overview section
with st.container():
    st.markdown('<h2 style="color: purple;">Server Total Power & KP Overview</h2>', unsafe_allow_html=True)
    fig1 = px.bar(data.nlargest(10, 'Killpoints'), x='Name', y='Killpoints', title='Top 10 Players by Killpoints',
                  color_discrete_sequence=['orange'])
    fig1.update_layout(title_font_color='purple', font=dict(color='purple'))
    st.plotly_chart(fig1)

# Contributions section using corrected column names
with st.container():
    st.markdown('<h2 style="color: purple;">Contributions</h2>', unsafe_allow_html=True)
    fig2 = px.bar(data.nlargest(10, 'Rss Gathered'), x='Name', y='Rss Gathered', title='Top 10 Players by RSS Gathered',
                  color_discrete_sequence=['orange'])
    fig2.update_layout(title_font_color='purple', font=dict(color='purple'))
    st.plotly_chart(fig2)

    fig3 = px.bar(data.nlargest(10, 'Rss Assistance'), x='Name', y='Rss Assistance', title='Top 10 Players by RSS Assistance',
                  color_discrete_sequence=['orange'])
    fig3.update_layout(title_font_color='purple', font=dict(color='purple'))
    st.plotly_chart(fig3)

    fig4 = px.bar(data.nlargest(10, 'Helps'), x='Name', y='Helps', title='Top 10 Players by Helps',
                  color_discrete_sequence=['orange'])
    fig4.update_layout(title_font_color='purple', font=dict(color='purple'))
    st.plotly_chart(fig4)

# DKP section using revised formula
with st.container():
    st.markdown('<h2 style="color: purple;">DKP Rankings</h2>', unsafe_allow_html=True)
    dkp_data = data.sort_values(by='DKP', ascending=False).head(10)
    fig5 = px.bar(dkp_data, x='Name', y='DKP', title='Top Players by DKP',
                  color_discrete_sequence=['orange'])
    fig5.update_layout(title_font_color='purple', font=dict(color='purple'))
    st.plotly_chart(fig5)

# Sidebar for search functionality
st.sidebar.title("Search Player")
st.sidebar.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: orange;
    }
    </style>
    """, unsafe_allow_html=True
)
search_term = st.sidebar.text_input("Enter Player Name or ID:")
if search_term:
    results = data[data['Name'].str.contains(search_term, case=False) | data['ID'].str.contains(search_term)]
    st.sidebar.write(results)
    
    if not results.empty:
        st.sidebar.markdown("### Player Overview")
        player_data = results.iloc[0]  # Taking the first match
        overview_fig = px.bar(x=['T4 Kills', 'T5 Kills', 'Deads', 'DKP'], y=[player_data['T4 Kills'], player_data['T5 Kills'], player_data['Deads'], player_data['DKP']], 
                              labels={'x': 'Metrics', 'y': 'Values'}, title=f"{player_data['Name']} Overview", color_discrete_sequence=['orange'])
        overview_fig.update_layout(title_font_color='purple', font=dict(color='purple'))
        st.sidebar.plotly_chart(overview_fig)
