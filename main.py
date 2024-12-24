import streamlit as st
from stat_tracker import stat_tracker
from AOO_Registration_Tool import aoo_registration_tool
from gameplay_info import gameplay_info
from contact_and_admin import contact_and_admin

def main():
    st.title("Welcome to 3270 Data Center")

    # Custom CSS for larger uniform button sizes
    st.markdown("""
        <style>
        .button-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
        }
        .button {
            font-size: 28px;
            padding: 30px;
            width: 250px;
            height: 150px;
            margin: 20px;
            text-align: center;
            line-height: 60px;
            background-color: #4b0082; /* Dark purple */
            color: #ffa500; /* Orange */
            border: none;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .button:hover {
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

    # Display the navigation options as buttons
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    
    if st.button("STAT Tracker", key="stat_tracker"):
        st.session_state.page = "STAT Tracker"
    if st.button("AOO Registration Tool", key="aoo_registration_tool"):
        st.session_state.page = "AOO Registration Tool"
    if st.button("Gameplay Information", key="gameplay_information"):
        st.session_state.page = "Gameplay Information"
    if st.button("Contact and Administration", key="contact_and_admin"):
        st.session_state.page = "Contact and Administration"

    st.markdown('</div>', unsafe_allow_html=True)

    # Default page
    if "page" not in st.session_state:
        st.session_state.page = "Landing"

    # Navigation to the selected page
    if st.session_state.page == "STAT Tracker":
        stat_tracker()
    elif st.session_state.page == "AOO Registration Tool":
        aoo_registration_tool()
    elif st.session_state.page == "Gameplay Information":
        gameplay_info()
    elif st.session_state.page == "Contact and Administration":
        contact_and_admin()
    else:
        st.write("Please select an option from the buttons above.")

if __name__ == "__main__":
    main()
