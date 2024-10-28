import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
from gtts import gTTS
from io import BytesIO
import base64

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to get response from Google Gemini API
def get_gemini_response(prompt, image):
    model = genai.GenerativeModel("gemini-1.5-pro")
    try:
        response = model.generate_content([prompt, image[0]])
        return response.text
    except Exception as e:
        st.error(f"Error fetching response from API: {e}")
        return None

# Function to handle the uploaded image
def image_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        st.error("No file uploaded")
        return None

# Function to generate speech from text using gTTS
def text_to_speech(text):
    tts = gTTS(text)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# Function to play the audio in Streamlit
def play_audio(audio_data):
    audio_bytes = audio_data.read()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    st.audio(f"data:audio/mp3;base64,{audio_b64}", format="audio/mp3")

# Main function for the Streamlit app
def updated_app():
    st.set_page_config(page_title="CalMate", page_icon="🍽️")
    st.header("Calmate - Your Calorie Advisor App")

    # Initialize session states
    if 'response' not in st.session_state:
        st.session_state.response = None
    if 'show_camera' not in st.session_state:
        st.session_state.show_camera = False

    # File uploader for images
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    camera_file = st.camera_input("Capture an image with your camera") if st.session_state.show_camera else None

    # Button to toggle the camera
    if st.button("Open Camera"):
        st.session_state.show_camera = not st.session_state.show_camera

    # Display uploaded or captured image
    image = None
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    elif camera_file:
        image = Image.open(camera_file)
        st.image(image, caption="Captured Image.", use_column_width=True)

    # Button to submit and analyze
    submit = st.button("Tell me the Total Calories!!")
    
    # Create the prompt for the app
    prompt = """
    You are an expert nutritionist. Analyze the food items from the image and calculate the total calories.
    Also, provide the details of every food item with calorie intake in the following format:

    1. Item 1 - No of Calories
    2. Item 2 - No of Calories
    3. Item 3 - No of Calories
    -------
    -------
    The details are very important and at the end I want you to give me the sum of all the items and a total of calories of that meal.

    Finally, mention whether the food is healthy or not. Also, provide the percentage split of carbohydrates, fats, fibers, sugar, and important nutrients in the diet.

    If the diet is healthy, write a healthy quote and praise the user. If the diet is not healthy, educate the user with some recommendations for healthier alternatives.
    """

    # Process the image and generate the response
    if submit and (uploaded_file or camera_file):
        image_data = image_image_setup(uploaded_file if uploaded_file else camera_file)
        if image_data:
            st.session_state.response = get_gemini_response(prompt, image_data)

            st.header("The Response is:")
            st.write(st.session_state.response)

    # Background styling with gradient and image
    page_bg_gradient_with_image = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://img.freepik.com/premium-photo/fresh-fruits-vegetables-grey-background-healthy-eating-concept-flat-lay-copy-space_1101366-601.jpg?semt=ais_hybrid'), linear-gradient(270deg, #a8e063, #f76b1c, #a8e063);
        background-size: cover, 800% 800%;
        background-position: center, 0% 50%;
        animation: moveGradient 12s ease infinite;
    }

    @keyframes moveGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    '''
    st.markdown(page_bg_gradient_with_image, unsafe_allow_html=True)

    # Only show the 'Play Nutrition Analysis as Speech' button if a response is available
    if st.session_state.response:
        if st.button("Play Nutrition Analysis as Speech"):
            audio_data = text_to_speech(st.session_state.response)
            play_audio(audio_data)

# Call the function to run the app
if __name__ == "__main__":
    updated_app()
