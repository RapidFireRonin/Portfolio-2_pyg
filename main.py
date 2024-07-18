import streamlit as st
import pandas as pd
import pygwalker as pyg
import streamlit.components.v1 as components

# Set page to wide mode
st.set_page_config(layout="wide")

# Set Streamlit title
st.title("Interactive Data Visualization with PyGWalker")

# Instructions
st.write("Upload a CSV file to visualize the data using PyGWalker.")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display PyGWalker
    st.write("Visualize the data using PyGWalker:")
    
    # Generate the HTML using PyGWalker with increased height
    pyg_html = pyg.to_html(df, spec="./gw_config.json")
    
    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=800, scrolling=False)
else:
    st.write("Please upload a CSV file to proceed.")

# Add custom CSS to make the visualization more prominent
st.markdown("""
    <style>
        .stApp {
            max-width: 100%;
        }
        iframe {
            width: 100%;
            min-height: 800px;
        }
    </style>
""", unsafe_allow_html=True)