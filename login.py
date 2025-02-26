# login.py
import streamlit as st
import core_functions as cf  # Import the shared functions

def main():
    st.title("Login")
    cf.check_session()
    if "email" in st.session_state:
        st.success(f"You're currently logged in as {st.session_state["email"]}")

        col1, col2 = st.columns([8, 3])  # Divide the names into two columns
        with col1:
            if st.button("Upload Files"):
                st.switch_page("pages/admin_app.py")
        with col2:
            if st.button("Logout", type="primary"):
                cf.logout()
    else:
        st.write(f"Please log in.")
        with st.form("login_form"):
            username = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                cf.login(username, password)


if __name__ == "__main__":
    main()