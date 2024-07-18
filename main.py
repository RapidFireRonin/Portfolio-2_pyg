import streamlit as st
import pandas as pd
import pygwalker as pyg
import streamlit.components.v1 as components
import base64
from html2image import Html2Image
import requests
import os

# Path to chromedriver executable
CHROMEDRIVER_PATH = r"C:\Users\Garrett\Documents\chromedriver\chromedriver.exe"

# Function to capture screenshot using html2image
def capture_screenshot(html_content, output_path):
    hti = Html2Image(browser_executable=CHROMEDRIVER_PATH)
    hti.screenshot(html_str=html_content, save_as=output_path, size=(1200, 800))

# Function to encode image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

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
    pyg_html = pyg.walk(df, return_html=True)
    
    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=800, scrolling=True)
    
    # Button to analyze the visualization
    if st.button("Analyze Visualization"):
        # Capture screenshot
        screenshot_path = "visualization.png"
        try:
            capture_screenshot(pyg_html, screenshot_path)
        except Exception as e:
            st.error(f"Error capturing screenshot: {e}")
            st.stop()
        
        # Encode image
        base64_image = encode_image(screenshot_path)
        
        # Set preset prompt
        preset_prompt = "Analyze this data visualization and provide insights on the main trends or patterns shown."
        
        # Call GPT-4 Vision API
        try:
            response = analyze_image_with_gpt4(base64_image, preset_prompt)
            # Display response
            if 'choices' in response and len(response['choices']) > 0:
                analysis = response['choices'][0]['message']['content']
                st.write("Analysis:")
                st.write(analysis)
            else:
                st.write("Error in API response")
        except Exception as e:
            st.error(f"Error calling GPT-4 Vision API: {e}")
        
        # Remove the screenshot file
        os.remove(screenshot_path)
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
