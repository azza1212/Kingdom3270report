
import streamlit as st
from stat_tracker import stat_tracker
from aoo_registration_tool import aoo_registration_tool
from gameplay_info import gameplay_info
from contact_and_admin import contact_and_admin

def main():
    st.title("Welcome to 3270 Data Center")

    # Navigation options
    options = ["Select an Option", "STAT Tracker", "AOO Registration Tool", "Gameplay Information and Resources", "Contact and Administration"]
    choice = st.selectbox("Navigate to:", options)

    # Navigate to the selected page
    if choice == "STAT Tracker":
        stat_tracker()
    elif choice == "AOO Registration Tool":
        aoo_registration_tool()
    elif choice == "Gameplay Information and Resources":
        gameplay_info()
    elif choice == "Contact and Administration":
        contact_and_admin()

if __name__ == "__main__":
    main()
