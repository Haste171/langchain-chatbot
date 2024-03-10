import streamlit as st
import requests

FASTAPI_URL = "http://localhost:9091/ingest"  

st.title("Document Ingestion")

uploaded_files = st.file_uploader("Upload Document(s)", accept_multiple_files=True)

namespace = st.text_input("Namespace (Optional)")

if st.button("Ingest Documents"):
    if uploaded_files:
        try:
            files = [("files", file) for file in uploaded_files]
            
            payload = {"namespace": namespace}
            
            response = requests.post(FASTAPI_URL, files=files, data=payload)
            
            if response.status_code == 200:
                st.success("Documents ingested successfully!")
            else:
                st.error(f"Failed to ingest documents. Error: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload at least one document.")

