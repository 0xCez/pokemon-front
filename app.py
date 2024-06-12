import streamlit as st
import requests
from PIL import Image
import base64
import os

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
            text-shadow: 1px 1px #3B4CCA;
        }
        .section-subtitle {
            font-size: 1.2em;  /* Slightly smaller font size for subtitles */
            color: #FFCB05;
            font-family: 'Press Start 2P', cursive;
            text-shadow: 1px 1px #3B4CCA;
            margin-bottom: -10px;  /* Reduce spacing */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Adding a background image
add_bg_from_local(os.path.join(os.getcwd(), 'images', 'pok_bckgrnd.png' ))

# Load custom CSS
load_custom_css()

# Centering the title
st.markdown('<p class="title">Pokemon Generator</p>', unsafe_allow_html=True)

# First section: Upload button and image display
st.markdown('<p class="section-title">Classification</p>', unsafe_allow_html=True)
st.markdown('<p class="section-subtitle">Upload Picture</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("")
if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

    # Call the prediction API
    # Assuming your prediction API endpoint is /predict
    response = requests.post("https://pokedex-6cnzjfgdzq-od.a.run.app/predict", files={"file": uploaded_file})
    if response.status_code == 200:
        prediction = response.json()
        type_of_pokemon = prediction.get("type")
        pokemon_name = prediction.get("name")
        generation = prediction.get("generation")
    else:
        st.error("Prediction failed")
        type_of_pokemon = "Unknown"
        pokemon_name = "Unknown"
        generation = "Unknown"
else:
    type_of_pokemon = ""
    pokemon_name = ""
    generation = ""


st.markdown('<p class="section-title">Pokemon Information</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="prediction-box">Pokemon type: </div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="prediction-box">Pokemon Name: </div>', unsafe_allow_html=True)

st.markdown(f'<p class="section-title">Generation:</p>', unsafe_allow_html=True)

# Third section: Generate Pokemon Button

# Button click handler (add to the main script if necessary)
if st.button("POKEMON GENERATION"):

    # Construct the API request
    params = {
        "name": pokemon_name,
        "type": type_of_pokemon,
        "generation": generation
    }

    # Call the FastAPI endpoint
    response = requests.get("https://pokedex-6cnzjfgdzq-od.a.run.app/generate", params=params)

    if response.status_code == 200:
        pokemon_image = response.json().get("image_url")
        st.image(pokemon_image, caption=f"{pokemon_name} - {type_of_pokemon}")
    else:
        st.error("Failed to generate Pokemon.")
