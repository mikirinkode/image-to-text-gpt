import streamlit as st
from openai import OpenAI
import base64
import requests


st.set_page_config(page_title="Image to Text", page_icon="📷")


# display title    
st.title("Image to Text!")
st.write("This app uses GPT-4-vision-preview to generate text from an image. Upload an image and GPT-4 will try to explain what's in it.")

# NOTE: This is a temporary solution to hide the input API key section.


# st.info("To begin, please input your OpenAI API key. Remember to keep it secure, as you'll need it for future access. \n Don't have an OpenAI API key? No worries, let's go and get one for you: \n- Create an account at https://platform.openai.com/ \n- Go to https://platform.openai.com/api-keys \n- Click 'Create new secret key' \n- Copy the key and paste it below.")

# # Set OpenAI API key
# st.subheader("Set OpenAI API key")
# openai_api_key = st.text_input("OpenAI API key:", key="openai_api_key", placeholder="Paste your key here (sk-...)")
# client = OpenAI(api_key = openai_api_key)
# st.info("Note: Your key is only used each time you upload an image and we don't store your key.")

openai_api_key=st.secrets["OPENAI_API_KEY"]

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
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "low" 
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

st.subheader("Let's try it out!")
with st.container(border=True):
    uploaded_file = st.file_uploader("Choose a file (png, jpg, jpeg)", type=['png', 'jpg', 'jpeg'])

    st.divider()
    col1, col2 = st.columns([1,2])

    if uploaded_file is not None:    
        with col1:
            st.write("Your Image:")
            st.image(uploaded_file, caption='Uploaded Image.', )
            
        with col2:
            st.write("Result:")
            with st.container(border=True):
                with st.spinner("Processing...") :
                    if not openai_api_key.startswith("sk-"):
                        st.warning("Please enter your OpenAI API key", icon='⚠')
                    else: 
                        result = get_text(uploaded_file)
                        st.write(result)
    else:
        with col1:
            st.write("Sample Image:")
            st.image("assets/miaw.png", caption='miaw.png',) 
        
        with col2:
            st.write("Sample Result:")
            with st.container(border=True):
                st.write("The image shows a cat standing on a tiled floor, possibly a patio or indoor area with a view of an outdoor area in the background due to the presence of grass. The cat has black and white fur, with distinctive markings on its face. It's looking back over its shoulder, perhaps at the camera or someone behind it. To the left side of the image, there is a broom leaning against what looks like a table or railing, suggesting this might be a domestic or semi-domestic space. The lighting suggests it might be daytime with sunlight filtering through.")
    
st.divider()
st.markdown("Image To Text - GPT 4. This code is open source and available <a href = https://github.com/mikirinkode/image-to-text-gpt>[here on Github]</a>", unsafe_allow_html=True)