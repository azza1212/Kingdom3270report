import streamlit as st
import pandas as pd
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to load player data from JSON file
def load_player_data(json_file):
    with open(json_file, 'r', encoding='utf-8-sig', errors='ignore') as f:
        return json.load(f)

# Function definition for aoo_registration_tool
def aoo_registration_tool():
    st.title("AOO Registration Tool")

    # Custom CSS to change the colors of the sidebar and other elements
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #4b0082; /* Dark purple */
    }
    .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3, .sidebar .sidebar-content h4, .sidebar .sidebar-content h5, .sidebar .sidebar-content h6, .sidebar .sidebar-content p, .sidebar .sidebar-content li, .sidebar .sidebar-content a {
        color: #ffa500; /* Orange */
    }
    .sidebar .sidebar-content .stButton>button {
        background-color: #4b0082; /* Dark purple */
        color: #ffa500; /* Orange */
    }
    .sidebar .sidebar-content .stTextInput>div>div>input {
        background-color: #4b0082; /* Dark purple */
        color: #ffa500; /* Orange */
    }
    .sidebar .sidebar-content .stSelectbox>div>div>div>div>div {
        background-color: #4b0082; /* Dark purple */
        color: #ffa500; /* Orange */
    }
    .sidebar .sidebar-content .stTimeInput>div>div>input {
        background-color: #4b0082; /* Dark purple */
        color: #ffa500; /* Orange */
    }
    .stButton>button {
        background-color: #4b0082; /* Dark purple */
        color: #ffa500; /* Orange */
    }
    .stApp {
        background-color: #000000; /* Black */
    }
    .stApp .stMarkdown h2 {
        color: #ffa500; /* Default color for h2 */
    }
    .stApp .stMarkdown p, .stApp .stMarkdown li, .stApp .stMarkdown a {
        color: #ff69b4; /* Pink for other information */
    }
    </style>
    """, unsafe_allow_html=True)

    # Function to get the color for each alliance
    def get_alliance_color(alliance):
        colors = {
            "GP70": "#ffa500", # Orange
            "GK70": "#0000ff", # Blue
            "GY70": "#800080", # Purple
            "P70A": "#00ffff", # Cyan
            "70Gk": "#87ceeb", # Baby blue
            "70YB": "#ff0000", # Red
            "70GA": "#00008b" # Dark blue
        }
        return colors.get(alliance, "#ffffff") # Default to white if not found

    # Predefined alliances
    ALLIANCES = ["GP70", "GK70", "GY70", "P70A", "70Gk", "70YB", "70GA"]

    # Load player data from JSON file
    player_data = load_player_data('rok_data 221224.json')

    def load_data():
        try:
            with open("registrations.json", "r", encoding="utf-8") as file:
                return pd.DataFrame(json.load(file))
        except FileNotFoundError:
            return pd.DataFrame(columns=["Name", "Alliance", "Time Zone", "Fight Time", "Approved"])

    def save_data(data):
        temp_file = "registrations_temp.json"
        data.to_json(temp_file, orient="records", force_ascii=False, indent=4)
        os.replace(temp_file, "registrations.json")

    def register_user(name, alliance, timezone, fight_time):
        data = load_data()
        new_entry = pd.DataFrame([{
            "Name": name,
            "Alliance": alliance,
            "Time Zone": timezone,
            "Fight Time": fight_time,
            "Approved": False
        }])
        data = pd.concat([data, new_entry], ignore_index=True)
        save_data(data)
        st.query_params.update({})

    def remove_user(name):
        data = load_data()
        data = data[data["Name"] != name]
        save_data(data)
        st.success(f"Registration for {name} has been removed.")
        st.query_params.update({})

    def send_emails():
        data = load_data()
        for i, row in data.iterrows():
            email = "KD3270@outlook.com"  # Replace with admin email
            subject = "Registration Update"
            body = f"Hello {row['Name']},\n\nYour registration status is: {'Approved' if row['Approved'] else 'Pending'}."
            send_email(email, subject, body)
        st.success("Emails sent successfully.")

    def send_email(to, subject, body):
        msg = MIMEMultipart()
        msg['From'] = "KD3270@outlook.com"  # Replace with sender email
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP('smtp.office365.com', 587) as server:  # Replace with SMTP server
                server.starttls()
                server.login("KD3270@outlook.com", "vhdmuwkywqycyokv")  # Replace with sender email and app password
                text = msg.as_string()
                server.sendmail(msg['From'], msg['To'], text)
        except Exception as e:
            st.error(f"Error sending email: {e}")

    data = load_data()
    for alliance in ALLIANCES:
        st.markdown(f"## <span style='color: {get_alliance_color(alliance)};'>{alliance}</span>", unsafe_allow_html=True)
        if "Alliance" in data.columns:
            alliance_data = data[data["Alliance"] == alliance]
            if not alliance_data.empty:
                for i, row in alliance_data.iterrows():
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
                    col1.markdown(f"<span style='color: #ff69b4;'>{row['Name']}</span>", unsafe_allow_html=True)
                    col2.markdown(f"<span style='color: #ff69b4;'>{row['Fight Time']}</span>", unsafe_allow_html=True)
                    col3.markdown(f"<span style='color: #ff69b4;'>{row['Time Zone']}</span>", unsafe_allow_html=True)
                    col4.markdown(f"<span style='color: #ff69b4;'>{'Approved' if row['Approved'] else 'Pending'}</span>", unsafe_allow_html=True)
                    if st.session_state.admin_logged_in:
                        if col5.button("Remove", key=f"remove_{row['Name']}"):
                            remove_user(row["Name"])
                        if not row["Approved"] and col6.button("Approve", key=f"approve_{row['Name']}"):
                            data.at[i, "Approved"] = True
                            save_data(data)
                            st.query_params.update({})
            else:
                st.write("No members registered yet.")
        else:
            st.write(f"No members registered yet for the alliance {alliance} as the 'Alliance' column is missing.")

    # Generate a list of times in 30-minute intervals
    time_options = []
    for hour in range(24):
        for minute in (0, 30):
            time_options.append(f"{hour:02d}:{minute:02d}")

    with st.sidebar.form("registration_form"):
        # Create a list of player names for the dropdown
        player_names = [player['Name'] for player in player_data]
        name = st.selectbox("Name", player_names)
        alliance = st.selectbox("Alliance", ALLIANCES)
        timezone = st.text_input("Time Zone")
        fight_time = st.selectbox("Fight Time", time_options)
        submitted = st.form_submit_button("Register")
        if submitted:
            if name and alliance and timezone and fight_time:
                register_user(name, alliance, timezone, fight_time)
                st.success(f"Registration submitted for {name} in {alliance}")
                st.query_params.update({})
            else:
                st.error("Please fill in all fields")

    # Add a button to manually send emails
    if st.button("Send Emails Now"):
        send_emails()

if __name__ == "__main__":
    aoo_registration_tool()
