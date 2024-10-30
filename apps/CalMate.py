import streamlit as st 
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
from gtts import gTTS
from io import BytesIO
import base64

# Loading all the environment variables
load_dotenv()

# Configuring Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to get response from Google Gemini API
def get_gemini_response(prompt, image):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([prompt, image[0]])
    return response.text

# Function to handle the uploaded image
def image_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Reading the file into bytes
        bytes_data = uploaded_file.getvalue()

        # Formatting the image for Google Gemini Pro
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the MIME type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
# Creating the prompt for the app
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
def main():
    # Setting up Streamlit App (Front-end Setup)
    #st.set_page_config(page_title="CalMate", page_icon="🍽️")

    # Load and display the logo in the header
    logo = Image.open("CalMate.png")
    st.image(logo, width=100)

    st.header("Calmate - Your Calorie Advisor App")


    # Initialize session states for camera and response if not already initialized
    if 'response' not in st.session_state:
        st.session_state.response = None
    if 'show_camera' not in st.session_state:
        st.session_state.show_camera = False

    # File uploader for uploaded images
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = None

    # Button to toggle the camera input visibility
    if st.button("Open Camera"):
        st.session_state.show_camera = not st.session_state.show_camera

    # Display the camera input only if show_camera flag is True
    camera_file = st.camera_input("Capture an image with your camera") if st.session_state.show_camera else None

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    elif camera_file is not None:
        image = Image.open(camera_file)
        st.image(image, caption="Captured Image.", use_column_width=True)

    submit = st.button("Tell me the Total Calories!!")

    # Process the image and generate the response
    if submit and (uploaded_file or camera_file):
        image_data = image_image_setup(uploaded_file if uploaded_file else camera_file)  # Prepare image data for the API
        st.session_state.response = get_gemini_response(prompt, image_data)  # Store the result in session state

        st.header("The Response is:")
        st.write(st.session_state.response)  # Display the response

    # Background styling with gradient and image
    page_bg_gradient_with_image = '''
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url('https://img.freepik.com/premium-photo/fresh-fruits-vegetables-grey-background-healthy-eating-concept-flat-lay-copy-space_1101366-601.jpg?semt=ais_hybrid'), linear-gradient(270deg, #a8e063, #f76b1c, #a8e063);
        background-size: cover, 800% 800%;
        background-position: center, 0% 50%;
        animation: moveGradient 12s ease infinite;
    }

    /* Define the gradient animation */
    @keyframes moveGradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    '''

    st.markdown(page_bg_gradient_with_image, unsafe_allow_html=True)

    # Function to generate speech from text using gTTS
    def text_to_speech(text):
        tts = gTTS(text)  # Convert the given text to speech
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)  # Save the audio in an in-memory file
        audio_file.seek(0)  # Go to the start of the file
        return audio_file

    # Function to play the audio in Streamlit
    def play_audio(audio_data):
        audio_bytes = audio_data.read()
        audio_b64 = base64.b64encode(audio_bytes).decode()  # Convert the audio to base64 format
        st.audio(f"data:audio/mp3;base64,{audio_b64}", format="audio/mp3")

    # Only show the 'Play Nutrition Analysis as Speech' button if a response is available
    if st.session_state.response:
        # Add a button to generate speech
        if st.button("Play Nutrition Analysis as Speech"):
            # Convert the output text to speech
            audio_data = text_to_speech(st.session_state.response)
            # Play the generated audio in the app
            play_audio(audio_data)
if __name__ == "__main__":
    main()