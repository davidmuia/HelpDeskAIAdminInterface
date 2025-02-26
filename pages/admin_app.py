# admin_app.py
import streamlit as st
import core_functions as cf  # Import the shared functions
import time

def main():
        st.title("PDF Upload")
        cf.check_session()
        if "email" in st.session_state:
            col1, col2 = st.columns([8, 2])  # Divide the names into two columns
            with col1:
                st.write(f"Welcome {st.session_state["email"]}")
            with col2:
                if st.button("Logout", type="primary"):
                    cf.logout()
            # Initialize database table on startup
            try:
                conn = cf.create_connection()
                cf.create_table(conn)
                conn.close()  # Close the connection immediately after table creation
            except Exception as e:
                st.error(f"Error connecting to or initializing the database: {e}")
                return  # Stop execution if database connection fails

            uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

            if uploaded_files:
                for pdf_file in uploaded_files:
                    st.write(f"Processing: {pdf_file.name}")
                    try:
                        text = cf.extract_text_from_pdf(pdf_file)
                        text = text.encode('utf-8', errors='ignore').decode('utf-8')
                        chunks = cf.chunk_text(text)
                        data_to_insert = []  # Prepare data for batch insert
                        for i, chunk in enumerate(chunks):
                            embedding = cf.generate_embedding(chunk)
                            if embedding:
                                data_to_insert.append((pdf_file.name, i, chunk, embedding))
                            else:
                                st.warning(f"Failed to generate embedding for chunk {i} in {pdf_file.name}. Skipping.")

                        conn = cf.create_connection()  # Create connection for data insertion
                        if data_to_insert:  # only try to insert data if the embedding process has been successful
                            cf.insert_data(conn, data_to_insert)
                            st.success(f"Successfully processed and stored: {pdf_file.name}")
                        else:
                            st.warning(f"No embeddings could be generated for {pdf_file.name}.  Skipping insertion.")
                        conn.close()  # Close connection after data insertion

                    except Exception as e:
                        st.error(f"Error processing {pdf_file.name}: {e}")

            # --- PDF Management Section ---
            st.subheader("Manage Existing PDFs")

            try:
                conn = cf.create_connection()
                pdf_names = cf.get_all_pdf_names(conn)
                conn.close()
            except Exception as e:
                st.error(f"Error retrieving PDF names: {e}")
                pdf_names = []

            if pdf_names:
                selected_pdf = st.selectbox("Select a PDF to delete:", pdf_names)

                if st.button("Delete Selected PDF"):
                    try:
                        conn = cf.create_connection()
                        cf.delete_pdf_chunks(conn, selected_pdf)
                        conn.close()
                        st.success(f"Successfully deleted PDF: {selected_pdf}")
                        time.sleep(1)  # Pause briefly before rerun
                        st.rerun() # refresh page
                    except Exception as e:
                        st.error(f"Error deleting PDF: {e}")
            else:
                st.info("No PDFs found in the database.")
        else:
            st.error(f"Please log in to access this page.")


if __name__ == "__main__":
    main()