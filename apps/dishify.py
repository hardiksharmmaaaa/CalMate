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
def get_gemini_response(prompt, image=None):
    model = genai.GenerativeModel("gemini-1.5-pro")
    if image:
        response = model.generate_content([prompt, image[0]])
    else:
        response = model.generate_content([prompt])
    return response.text

# Function to handle the uploaded image
def image_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Reading the file into bytes
        bytes_data = uploaded_file.getvalue()

        # Formatting the image for Google Gemini Pro
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None
    
# Creating the base prompt
prompt = """
Imagine you are a personal chef providing guidance on creating a specific dish. When someone asks you how to make a dish, respond by including:

Whenever given a dish name (e.g., ‘Spaghetti Carbonara’) followed by quantity, provide a detailed recipe including:

Dish Name: Sure, lets Cook this , Start with the dish name provided.
Ingredients: List precise quantities for each ingredient based on the given quantity.
Procedure: Outline a clear, beginner-friendly procedure with steps separated by line breaks.
Example Input: ‘Spaghetti Carbonara, for 2 people’

Desired Response:
Dish: Spaghetti Carbonara

Ingredients:

200g spaghetti
100g pancetta or guanciale, diced
2 large eggs
50g grated Parmesan cheese
1 clove garlic, peeled
Salt and black pepper, to taste

Procedure:

Step 1 - Cook the Spaghetti: Bring a large pot of salted water to a boil, then add the spaghetti. Cook until al dente, about 8-10 minutes. Reserve a cup of pasta water before draining.

Step 2 - Prepare the Sauce: In a bowl, beat the eggs and mix in the grated Parmesan cheese until smooth. Season with black pepper.

step 3 - Cook the Pancetta: In a large pan, heat a little olive oil over medium heat. Add the garlic clove and cook for 1 minute, then remove it. Add the pancetta and cook until crispy, about 4-5 minutes.

Step 4 - Combine Ingredients: Add the hot, drained spaghetti to the pan with the pancetta. Toss well to combine.

Step 5 - Add the Sauce: Remove the pan from heat, wait a few seconds, then pour the egg and cheese mixture over the pasta, stirring quickly to create a creamy sauce. If needed, add a bit of reserved pasta water to reach your desired consistency.

Step 6 - Serve: Season with additional black pepper, garnish with extra Parmesan, and serve immediately.

Note that the steps should be seperated by the next line 
Repeat this structure for all dishes, ensuring the response includes clear ingredients and easy-to-follow instructions."
"""


def main():
    # Setting up Streamlit App (Front-end Setup)
    # st.set_page_config(page_title="Dishify", page_icon="👨‍🍳")

    # Load and display the logo in the header
    logo = Image.open("chef.png")
    st.image(logo, width=100)

    st.header("Dishify - Your Personal Chef, One Chat Away!")

    # Input for text prompt
    user_input = st.text_input("Enter dish or ingredient query here:", key="user_input")

    # File uploader for uploaded images
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Display image if uploaded
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Submit button
    submit = st.button("Generate Recipe")

    # Generate response based on input
    if submit:
        if uploaded_file:
            # Process the image and use both prompt and image to generate response
            image_data = image_image_setup(uploaded_file)
            st.session_state.response = get_gemini_response(prompt, image_data)
        elif user_input:
            # Use user_input as the prompt if no image is uploaded
            st.session_state.response = get_gemini_response(user_input)
        else:
            st.warning("Please provide either an image or a text query.")

    # Display the response
    if st.session_state.get("response"):
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

    # Only show 'Play DIY' button if response is available
    if st.session_state.get("response"):
        if st.button("Play The DIY"):
            audio_data = text_to_speech(st.session_state.response)
            play_audio(audio_data)

if __name__ == "__main__":
    main()



