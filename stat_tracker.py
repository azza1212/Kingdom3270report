import streamlit as st
import pandas as pd
import plotly.express as px
import json

def stat_tracker():
    st.header("STAT Tracker")
    
    # Load JSON data
    def load_json(json_file):
        with open(json_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
            data = json.load(f)
        return data

    # Define calculate_target_status function
    def calculate_target_status(row):
        # Calculate changes in T4 and T5 kills and deads
        t4_kills_change = row['T4 Kills_current'] - row['T4 Kills_baseline']
        t5_kills_change = row['T5 Kills_current'] - row['T5 Kills_baseline']
        deads_change = row['Deads_current'] - row['Deads_baseline']

        # Calculate changes in Power
        power_change = row['Power_current'] - row['Power_baseline']

        # Calculate DKP change
        dkp_current = row['DKP_current']

        # DKP goals based on Power range
        power = row['Power_current']
        if 20000000 <= power <= 30000000:
            goal = 250000
        elif 30000001 <= power <= 40000000:
            goal = 300000
        elif 40000001 <= power <= 50000000:
            goal = 400000
        elif 50000001 <= power <= 60000000:
            goal = 550000
        elif 60000001 <= power <= 70000000:
            goal = 650000
        elif 70000001 <= power <= 80000000:
            goal = 750000
        elif 80000001 <= power <= 85000000:
            goal = 900000
        elif 85000001 <= power <= 90000000:
            goal = 1250000
        elif 90000001 <= power <= 100000000:
            goal = 1500000
        elif power >= 100000001:
            goal = 2000000
        else:
            goal = 0

        return {
            "T4 Kills Change": t4_kills_change,
            "T5 Kills Change": t5_kills_change,
            "Deads Change": deads_change,
            "Power Change": power_change,
            "DKP Current": dkp_current,
            "Goal": goal
        }

    # Convert main JSON data to DataFrame
    baseline_data = load_json('rok_data 221224.json')
    current_data = load_json('Current_Rokdata.json')
    baseline_df = pd.DataFrame(baseline_data)
    current_df = pd.DataFrame(current_data)

    # Ensure 'ID' column is treated as string
    baseline_df['ID'] = baseline_df['ID'].astype(str)
    current_df['ID'] = current_df['ID'].astype(str)

    # Calculate total kills for both datasets
    for df in [baseline_df, current_df]:
        df['Total Kills'] = df['T1 Kills'] + df['T2 Kills'] + df['T3 Kills'] + df['T4 Kills'] + df['T5 Kills']
        df['DKP'] = (df['T4 Kills'] * 1) + (df['T5 Kills'] * 2) + (df['Deads'] * 2)
        df.drop_duplicates(subset=['ID', 'Name'], keep='first', inplace=True)

    # Compare current data to baseline data
    comparison_data = current_df.merge(baseline_df, on='ID', suffixes=('_current', '_baseline'))
    comparison_data = comparison_data.apply(lambda row: pd.Series(calculate_target_status(row)), axis=1)
    
    # Align the indexes to avoid length mismatch
    comparison_data = comparison_data.reset_index(drop=True)
    current_ids_names = current_df[['ID', 'Name']].reset_index(drop=True)
    comparison_data = pd.concat([comparison_data, current_ids_names], axis=1)

    # Display comparison data in Streamlit
    st.markdown('<h1 style="color: orange;">Kingdom 3270 Report</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="color: purple;">Comparison of Current and Baseline Data</h2>', unsafe_allow_html=True)
    st.write(comparison_data[['ID', 'Name', 'T4 Kills Change', 'T5 Kills Change', 'Deads Change', 'Power Change', 'DKP Current', 'Goal']])

    # Your existing display logic
    # KD Power and Seed
    top_300_power = current_df.nlargest(300, 'Power')['Power'].sum()
    if top_300_power >= 10000000000:
        seed = 'A'
    elif top_300_power >= 5000000000:
        seed = 'B'
    else:
        seed = 'C'
    st.markdown(f'<h2 style="color: purple;">KD Power: {top_300_power:,} | Seed: {seed}</h2>', unsafe_allow_html=True)

    # Full Kingdom List Section
    with st.container():
        st.markdown('<h2 style="color: purple;">Full Kingdom List (Top 300)</h2>', unsafe_allow_html=True)
        full_kingdom_data = current_df.sort_values(by='Power', ascending=False)
        st.write(full_kingdom_data[['ID', 'Name', 'Power', 'Killpoints', 'Deads', 'T1 Kills', 'T2 Kills', 'T3 Kills', 'T4 Kills', 'T5 Kills']].head(300))

    # Power Ranking section sorted by Power
    with st.container():
        st.markdown('<h2 style="color: purple;">Power Ranking</h2>', unsafe_allow_html=True)
        sorted_power_data = current_df.sort_values(by='Power', ascending=False)
        st.write(sorted_power_data[['ID', 'Name', 'Power', 'Killpoints', 'Deads', 'T1 Kills', 'T2 Kills', 'T3 Kills', 'T4 Kills', 'T5 Kills']].head(10))

    # KP Overview section
    with st.container():
        st.markdown('<h2 style="color: purple;">Server Total Power & KP Overview</h2>', unsafe_allow_html=True)
        fig1 = px.bar(current_df.nlargest(10, 'Killpoints'), x='Name', y='Killpoints', title='Top 10 Players by Killpoints',
                      color_discrete_sequence=['orange'])
        fig1.update_layout(title_font_color='purple', font=dict(color='purple'))
        st.plotly_chart(fig1)

    # Contributions section using corrected column names
    with st.container():
        st.markdown('<h2 style="color: purple;">Contributions</h2>', unsafe_allow_html=True)
        fig2 = px.bar(current_df.nlargest(10, 'Rss Gathered'), x='Name', y='Rss Gathered', title='Top 10 Players by RSS Gathered',
                      color_discrete_sequence=['orange'])
        fig2.update_layout(title_font_color='purple', font=dict(color='purple'))
        st.plotly_chart(fig2)

        fig3 = px.bar(current_df.nlargest(10, 'Rss Assistance'), x='Name', y='Rss Assistance', title='Top 10 Players by RSS Assistance',
                      color_discrete_sequence=['orange'])
        fig3.update_layout(title_font_color='purple', font=dict(color='purple'))
        st.plotly_chart(fig3)

        fig4 = px.bar(current_df.nlargest(10, 'Helps'), x='Name', y='Helps', title='Top 10 Players by Helps',
                      color_discrete_sequence=['orange'])
        fig4.update_layout(title_font_color='purple', font=dict(color='purple'))
        st.plotly_chart(fig4)

    # DKP section using revised formula
    with st.container():
        st.markdown('<h2 style="color: purple;">DKP Rankings</h2>', unsafe_allow_html=True)
        dkp_data = current_df.sort_values(by='DKP', ascending=False).head(10)
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
        results = current_df[current_df['Name'].str.contains(search_term, case=False) | current_df['ID'].str.contains(search_term)]
        st.sidebar.write(results)

        if not results.empty:
            st.sidebar.markdown("### Player Overview")
            player_data = results.iloc[0]  # Taking the first match
            overview_fig = px.bar(x=x, y=y, title="Overview Chart", labels={'x': 'Categories', 'y': 'Values'})