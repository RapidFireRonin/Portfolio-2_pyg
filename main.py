import streamlit as st
import pandas as pd
import pygwalker as pyg

# Set Streamlit title
st.title("PyGWalker with Streamlit")

# Instructions
st.write("Upload a CSV file to visualize the data using PyGWalker.")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Display DataFrame
    st.write("Here is the uploaded data:")
    st.dataframe(df)

    # Display PyGWalker
    st.write("Visualize the data using PyGWalker:")
    pyg.walk(df)
else:
    st.write("Please upload a CSV file to proceed.")
