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
        </style>
        """,
        unsafe_allow_html=True
    )

# Adding a background image
add_bg_from_local(os.path.join(os.getcwd(), 'images', 'bourg_palette.png' ))

# Load custom CSS
load_custom_css()

# Centering the title
st.markdown('<p class="title">Pokemon Generator</p>', unsafe_allow_html=True)

# Adding instructions
st.markdown('''
## Generate New Pokemon
''')
st.markdown('''
Input the parameters for generating a new Pokemon and get an image of the generated Pokemon.
''')

# Adding images as labels for input fields
name_image = Image.open(os.path.join(os.getcwd(), 'images', 'button_1.png' ))
type_image = Image.open(os.path.join(os.getcwd(), 'images', 'button_2.png'))
generation_image = Image.open(os.path.join(os.getcwd(), 'images', 'button_3.png'))

# Set the width of the images consistently
image_width = 150

st.image(name_image, width=image_width)
name = st.text_input("", key="name")

st.image(type_image, width=image_width)
type_ = st.text_input("", key="type")

st.image(generation_image, width=image_width)
generation = st.number_input("", min_value=1, max_value=8, step=1, key="generation")

# File upload
uploaded_file = st.file_uploader("Choose a Pokemon")

# Button to generate Pokemon
if st.button("Generate Pokemon"):
    # Construct the API request
    params = {
        "name": name,
        "type": type_,
        "generation": generation
    }

    # Call the FastAPI endpoint
    response = requests.get("http://localhost:8000/generate", params=params)

    if response.status_code == 200:
        pokemon_image = response.json().get("image_url")
        st.image(pokemon_image, caption=f"{name} - {type_} - Generation {generation}")
    else:
        st.error("Failed to generate Pokemon.")
