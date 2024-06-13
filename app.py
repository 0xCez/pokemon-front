import streamlit as st
import requests
from PIL import Image
import base64
import os
from io import BytesIO
import time

# Function to add a background image from a local file
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_string = base64.b64encode(image.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Add custom CSS for styling
def load_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        .title {
            font-size: 3em;
            text-align: center;
            color: #FFCB05;
            font-family: 'Press Start 2P', cursive;
            text-shadow: 2px 2px #3B4CCA;
        }
        .caption {
            text-align: center;
            color: #FFCB05;
            font-family: 'Press Start 2P', cursive;
            text-shadow: 1px 1px #3B4CCA;
        }
        .stButton>button {
            background-color: #FFCB05;
            color: #000000;
            border: none;
            border-radius: 12px;
            padding: 10px 24px;
            font-size: 16px;
            font-family: 'Press Start 2P', cursive;
            display: block;
            margin: auto;
        }
        
        .stButton>button:hover{
            box-shadow: rgba(128, 0, 128, 0.5) 0px 0px 0px 0.2rem;
        }
        
        .stTextInput>div>div {
            width: 50%;  /* Reduce the width to half */
        }
        .stTextInput>div>div>input {
            font-family: 'Press Start 2P', cursive;
            color: #3B4CCA;
        }
        .stNumberInput>div>div>input {
            font-family: 'Press Start 2P', cursive;
            color: #3B4CCA;
        }
        .stImage {
            margin-bottom: -10px;  /* Adjust this value to move the input box closer to the image */
        }
        .prediction-box {
            background-color: rgba(59, 76, 202, 0.8);
            color: #FFCB05;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-size: 1em;
            font-family: 'Press Start 2P', cursive;
            margin-bottom: 10px;
            width: 80%;  /* Adjust the width to reduce size */
            margin: 10px auto;  /* Center the box */
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-top: 20px;
            
        }
        .section-title {
            font-size: 1.5em;  /* Unified font size for section titles */
            color: #FFCB05;
            font-family: 'Press Start 2P', cursive;
            text-shadow: 1px 2px #3B4CCA;
            padding-top: 2%;
        }
        .section-subtitle {
            font-size: 1.2em;  /* Slightly smaller font size for subtitles */
            color: #FFCB05;
            font-family: 'Press Start 2P', cursive;
            text-shadow: 1px 2px #3B4CCA;
            margin-bottom: -10px;  /* Reduce spacing */
        }
        # .css-ffhzg2{
        #     text-align: center;
        # }
        
        .css-1kyxreq {
            justify-content: center;
        }
        # .css-1kyxreq > img {
        #     bottom: 0;
        #     position: absolute;
        # }
        
        # .etr89bj2>img {
        #     width: 60%;
        #     margin: auto;
        #     display: block;
        # }
        
        .stTabs [data-baseweb="tab-list"] {
		    gap: 2px;
        }
        
        .stTabs [data-baseweb="tab-highlight"] {
            border: 1px solid #3B4CCA;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #3B4CCA
        }

        .stTabs [data-baseweb="tab"] {
            height: 35px;
            white-space: pre-wrap;
            background-color: rgba(0, 0, 0, 0.3);
            border-radius: 6px 6px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            padding-right: 2%;
            padding-left: 2%;

        }

        .stTabs [aria-selected="true"] {
            background-color: #FFCB03;
            color: #3B4CCA;

        }
        
        .css-1p3cbdm {
            background-color: rgb(38, 39, 48, 0.3);
        }
        .css-1p3cbdm:hover {
            background-color: rgb(38, 39, 48, 0.5);
        }
        
        .css-7gsey4 {
            background-color: rgb(38, 39, 48, 0.3);
        }
        
        # .row-widget {
        #     border: 15px solid #cfe0e6;
        #     box-shadow: 0 15px 30px rgba(0, 0, 0, .5);
        #     right: calc(5vw);
        #     left: calc(5vw);
        #     top: calc(5vw);
        #     bottom: 5vw;
        #     border-radius: 50%;
        #     overflow: hidden;
        #     background: #000;
        # }
        
        # .css-7gsey4 {
        #     height: 331px;
        # }
        # .css-1a3it4f {
        #     width: 70%;
        # }
        
        .block-container {
            background: rgba(0, 0, 0, 0.6);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Adding a background image
add_bg_from_local(os.path.join(os.getcwd(), 'images', 'pok_bckgrnd.png'))

# Load custom CSS
load_custom_css()

# Centering the title
st.markdown('<p class="title">Pokemon Generator</p>', unsafe_allow_html=True)

# First section: Upload button and image display
st.markdown('<p class="section-title">Classification</p>', unsafe_allow_html=True)


type_of_pokemon = ""
pokemon_name = ""

# Insert containers separated into tabs:
tab1, tab2 = st.tabs(["⬆", "◉"])
with tab1:
    tab1.markdown('<p class="section-subtitle">Upload a picture</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("")
    
    if uploaded_file is not None:

        col1, col2, col3 = st.columns(3)
        with col2:
            img = Image.open(uploaded_file)
            st.image(img, caption='Uploaded Image', use_column_width=True)
        
        # Convert image to RGB if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        # Convert the image to bytes for API request
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()

        # Call the prediction API on endpoint /predict
        response = requests.post("https://pokedex-6cnzjfgdzq-od.a.run.app/predict", files={"img": ("filename", img_bytes, "image/jpeg")})
        if response.status_code == 200:
            prediction = response.json()
            type_of_pokemon = prediction.get("type")
            pokemon_name = prediction.get("Pokemon")
            
            time.sleep(3)
            
            # Fetching badge and pokemon images
            type_img_path = f"images/badges/{type_of_pokemon}.png"
            pokemon_img_path = f'images/pokemon_pics/{pokemon_name}.png'

        else:
            st.error("Prediction failed")
            type_of_pokemon = "Unknown"
            pokemon_name = "Unknown"
    else:
        type_of_pokemon = ""
        pokemon_name = ""
        type_img_path = ""
        pokemon_img_path = ""


with tab2:
    tab2.markdown('<p class="section-subtitle">Take a photo of a wild Pokemon</p>', unsafe_allow_html=True)
    photo = st.camera_input('')
    
    if photo is not None:
        # Display the uploaded image
        img = Image.open(photo)
        # st.image(img, caption='Uploaded Image', use_column_width=False)

        # Convert image to RGB if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Convert the image to bytes for API request
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()

        # Call the FastAPI endpoint
        try:
            response = requests.post(
                "https://pokedex-6cnzjfgdzq-od.a.run.app/predict",  # API URL from environment variable
                files={"img": ("filename", img_bytes, "image/jpeg")}
            )
            # Check the response status and display the result
            if response.status_code == 200:
                result = response.json()

                type_of_pokemon = result.get("type")
                pokemon_name = result.get("Pokemon")
                
                time.sleep(3)

                # Fetching badge and pokemon images
                type_img_path = f"images/badges/{type_of_pokemon}.png"
                pokemon_img_path = f'images/pokemon_pics/{pokemon_name}.png'
                
            else:
                st.error("Prediction failed")
                type_of_pokemon = "Unknown"
                pokemon_name = "Unknown"
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")


            
st.markdown('<p class="section-title">Pokemon Information</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f'<div class="prediction-box">Pokemon type: {type_of_pokemon}</div>', unsafe_allow_html=True)
    placeholder1 = st.empty()
    if os.path.exists(type_img_path):
            placeholder1.image(type_img_path)
        
with col2:
    st.markdown(f'<div class="prediction-box">Pokemon Name: {pokemon_name}</div>', unsafe_allow_html=True)
    # Verify that the file exists
    placeholder2 = st.empty()
    if os.path.exists(pokemon_img_path):
            placeholder2.image(pokemon_img_path) 

    
    


# Third section: Generate Pokemon Button
st.markdown(f'<p class="section-title">Generation</p>', unsafe_allow_html=True)


# Button click handler (add to the main script if necessary)
if st.button("POKEMON GENERATION"):

    # Call the FastAPI endpoint
    response = requests.get("https://pokedex-6cnzjfgdzq-od.a.run.app/generate")

    if response.status_code == 200:
        try:
            # Attempt to open the response as an image
            image = Image.open(BytesIO(response.content))
            st.image(image)
        except Exception as e:
            # Handle errors in opening the image
            st.error(f"Failed to decode image: {e}")
    else:
        st.error("Failed to generate Pokemon.")


