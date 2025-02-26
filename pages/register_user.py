# register_user.py
import streamlit as st
import core_functions as cf  # Import the shared functions

# --- List of Departments ---
DEPARTMENTS = ["IT", "Billing", "HR"]

def main():
    st.title("Admin: User Registration")
    cf.check_session()
    if "email" in st.session_state:

        # --- Registration Form ---
        col1, col2 = st.columns([0.5, 0.5])  # Divide the names into two columns
        with col1:
            first_name = st.text_input("First Name")
        with col2:
            last_name = st.text_input("Last Name")

        email = st.text_input("Email")

        col3, col4 = st.columns([0.5, 0.5])  # Divide the password area into two columns
        with col3:
            password = st.text_input("Password", type="password")
        with col4:
            confirm_password = st.text_input("Confirm Password", type="password")

        col5, col6 = st.columns([0.5, 0.5])  # Divide the department and role into two columns
        with col5:
            department = st.multiselect("Department", DEPARTMENTS)
        with col6:
            role = st.selectbox("Role", ["admin", "trainer"])

        if st.button("Register"):
            if password == confirm_password:
                try:
                    conn = cf.create_connection()
                    cf.create_user_table(conn)
                    success = cf.create_user(conn, first_name, last_name, email, password, department, role) #New table creation
                    conn.close()
                    if success:
                        st.success("Registration successful.")
                    else:
                        st.error("Email already exists. Please use a different email.")

                except Exception as e:
                    st.error(f"Error creating user: {e}")
            else:
                st.error("Passwords do not match.")
    else:
        st.error(f"Please log in to access this page.")

if __name__ == "__main__":
    main()