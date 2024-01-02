import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="Image to Text")

import streamlit as st
from openai import OpenAI
import base64
import requests
import json


# Set OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key = openai_api_key)

# display title    
st.title("Explain me this image!")

def get_text(image):
    # read image
    base64_image = base64.b64encode(image.read()).decode('utf-8')
    
    # set up request header
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
    }
    
    # set up request payload
    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What's in this image?"
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }
    
    # send request ang get the response
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    result = response.json()['choices'][0]['message']['content']
    return result


uploaded_file = st.file_uploader("Choose a file (png, jpg, jpeg)", type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    
    st.divider()
    
    col1, col2 = st.columns([1,2])
    
    with col1:
        st.write("Your Image:")
        st.image(uploaded_file, caption='Uploaded Image.', )
        
    with col2:
        st.write("Result:")
        with st.container(border=True):
            with st.spinner("Processing...") :
                result = get_text(uploaded_file)
                st.write(result)
                # show text with lorem ipsum
                # st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec euismod, nisl eget aliquam ultricies, nunc nisl aliquet nunc, vitae aliquam ni")
    
st.divider()
st.markdown("Image To Text - GPT 4. created by <a href = https://github.com/mikirinkode>mikirinkode</a>", unsafe_allow_html=True)