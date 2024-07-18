import streamlit as st
import pandas as pd
import pygwalker as pyg
import streamlit.components.v1 as components
import base64
from PIL import Image
import requests
import io

# Function to encode image to base64
def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

# Function to call ChatGPT Vision API
def analyze_image_with_gpt4(base64_image, prompt):
    api_key = st.secrets["OPENAI_API_KEY"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Set page to wide mode
st.set_page_config(layout="wide")

# Set Streamlit title
st.title("Interactive Data Visualization with PyGWalker and ChatGPT Vision")

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
    
    # Button to analyze the visualization
    if st.button("Analyze Visualization"):
        # Capture the current view as an image
        img_bytes = st.experimental_get_query_params().get("screenshot", [None])[0]
        if img_bytes:
            img_bytes = base64.b64decode(img_bytes)
            
            # Encode image
            base64_image = encode_image(img_bytes)
            
            # Set preset prompt
            preset_prompt = "Analyze this data visualization and provide insights on the main trends or patterns shown."
            
            # Call GPT-4 Vision API
            response = analyze_image_with_gpt4(base64_image, preset_prompt)
            
            # Display response
            if 'choices' in response and len(response['choices']) > 0:
                analysis = response['choices'][0]['message']['content']
                st.write("Analysis:")
                st.write(analysis)
            else:
                st.write("Error in API response")
        else:
            st.write("Please interact with the visualization first to generate a screenshot.")

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