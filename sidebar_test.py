import streamlit as st

st.title("Sidebar Demo")

with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.success(f"Uploaded: {uploaded_file.name}")
else:
    st.info("Upload a file using the sidebar.")
