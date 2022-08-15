import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import plotly.express as px

st.set_page_config(layout="wide")

# Add a title and intro text
st.title('Data Explorer')
st.text('This is a web app to allow exploration of data')

# Sidebar setup
st.sidebar.title('Upload file')
upload_file = st.sidebar.file_uploader('Upload you data file ')

# Check if file has been uploaded
if upload_file is not None:
    df = pd.read_csv(upload_file)
    st.session_state['df'] = df