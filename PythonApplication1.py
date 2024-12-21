import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Load JSON data
def load_json(json_file):
    with open(json_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
        data = json.load(f)
    return data

# Convert main JSON data to DataFrame
json_data = load_json('rok_data 221224.json')
data = pd.DataFrame(json_data)

# Load seed data
seed_data = load_json('SEED-221224.json')
seed_df = pd.DataFrame(seed_data)

# Ensure 'ID' column is treated as string
data['ID'] = data['ID'].astype(str)

# Calculate total kills using the correct column names from your JSON
data['Total Kills'] = data['T1 Kills'] + data['T2 Kills'] + data['T3 Kills'] + data['T4 Kills'] + data['T5 Kills']

# Revised DKP formula using available columns
data['DKP'] = (data['T4 Kills'] * 1) + (data['T5 Kills'] * 2) + (data['Deads'] * 2)

# Calculate KD Power and determine Seed from seed data using 'score'
top_300_power = seed_df.nlargest(300, 'score')['score'].sum()
if top_300_power >= 10000000000:  # Adjust these thresholds based on your specific criteria
    seed = 'A'
elif top_300_power >= 5000000000:
    seed = 'B'
else:
    seed = 'C'

# Title
st.markdown('<h1 style="color: orange;">Kingdom 3270 Report</h1>', unsafe_allow_html=True)

# KD Power and Seed
st.markdown(f'<h2 style="color: purple;">KD Power: {top_300_power:,} | Seed: {seed}</h2>', unsafe_allow_html=True)

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
    fig2 = px.bar(data.nlargest(10, 'Rss Gathered'), x='Name', y='Rss Gathered',