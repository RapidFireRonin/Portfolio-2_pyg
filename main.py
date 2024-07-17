import streamlit as st
import pandas as pd
import pygwalker as pyg

# Sample Data
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Age": [24, 27, 22, 32, 29],
    "City": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
    "Score": [85, 92, 88, 76, 95]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Set Streamlit title
st.title("PyGWalker with Streamlit")

# Display DataFrame
st.write("Here is the sample data:")
st.dataframe(df)

# Display PyGWalker
st.write("Visualize the data using PyGWalker:")
pyg.walk(df)
