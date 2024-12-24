import streamlit as st
import pandas as pd

# Function definition for aoo_registration_tool
def aoo_registration_tool():
    st.title("AOO Registration Tool")
    # Custom CSS to change the colors of the sidebar and other elements
    st.markdown(
        """
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
        """,
        unsafe_allow_html=True
    )
    
    # Function to get the color for each alliance
    def get_alliance_color(alliance):
        colors = {
            "GP70": "#ffa500",  # Orange
            "GK70": "#0000ff",  # Blue
            "GY70": "#800080",  # Purple
            "P70A": "#00ffff",  # Cyan
            "70Gk": "#87ceeb",  # Baby blue
            "70YB": "#ff0000",  # Red
            "70GA": "#00008b"   # Dark blue
        }
        return colors.get(alliance, "#ffffff")  # Default to white if not found

    # Predefined alliances
    ALLIANCES = ["GP70", "GK70", "GY70", "P70A", "70Gk", "70YB", "70GA"]

    def load_data():
        try:
            return pd.read_csv("registrations.csv")
        except FileNotFoundError:
            return pd.DataFrame(columns=["Name", "Alliance", "Time Zone", "Fight Time", "Approved"])

    def save_data(data):
        data.to_csv("registrations.csv", index=False)

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

    def remove_user(name):
        data = load_data()
        data = data[data["Name"] != name]
        save_data(data)
        st.success(f"Registration for {name} has been removed.")

    data = load_data()
    for alliance in ALLIANCES:
        st.markdown(f"## <span style='color: {get_alliance_color(alliance)};'>{alliance}</span>", unsafe_allow_html=True)
        alliance_data = data[data["Alliance"] == alliance]
        if not alliance_data.empty:
            for i, row in alliance_data.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 1, 1])
                col1.markdown(f"<span style='color: #ff69b4;'>{row['Name']}</span>", unsafe_allow_html=True)
                col2.markdown(f"<span style='color: #ff69b4;'>{row['Fight Time']}</span>", unsafe_allow_html=True)
                col3.markdown(f"<span style='color: #ff69b4;'>{row['Time Zone']}</span>", unsafe_allow_html=True)
                col4.markdown(f"<span style='color: #ff69b4;'>{'Approved' if row['Approved'] else 'Pending'}</span>", unsafe_allow_html=True)
                if st.session_state.admin_logged_in:
                    if not row["Approved"]:
                        if col5.button("Approve", key=f"approve_{row['Name']}"):
                            data.at[i, "Approved"] = True
                            save_data(data)
                            st.experimental_rerun()
                        if col6.button("Remove", key=f"remove_{row['Name']}"):
                            remove_user(row["Name"])
                            st.experimental_rerun()
        else:
            st.write("No members registered yet.")

    with st.sidebar.form("registration_form"):
        name = st.text_input("Name")
        alliance = st.selectbox("Alliance", ALLIANCES)
        timezone = st.text_input("Time Zone")
        fight_time = st.time_input("Fight Time")
        submitted = st.form_submit_button("Register")

        if submitted:
            if name and alliance and timezone and fight_time:
                register_user(name, alliance, timezone, fight_time)
                st.success(f"Registration submitted for {name} in {alliance}")
                st.experimental_rerun()  # Refresh the page to show the new registration
            else:
                st.error("Please fill in all fields")

if __name__ == "__main__":
    aoo_registration_tool()
