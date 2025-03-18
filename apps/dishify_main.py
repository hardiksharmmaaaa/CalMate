import streamlit as st 
import google.generativeai as genai
from dotenv import load_dotenv
import os
from PIL import Image
from gtts import gTTS
from io import BytesIO
import base64
import time
import threading

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize session state variables
if "response" not in st.session_state:
    st.session_state["response"] = ""

if "audio" not in st.session_state:
    st.session_state["audio"] = None

if "highlighted_text" not in st.session_state:
    st.session_state["highlighted_text"] = ""

if "play_tts" not in st.session_state:
    st.session_state["play_tts"] = False

# Function to get response from Google Gemini API
def get_gemini_response(prompt, image=None):
    model = genai.GenerativeModel("gemini-1.5-pro")
    if image:
        response = model.generate_content([prompt, image[0]], stream=True)
    else:
        response = model.generate_content([prompt], stream=True)
    
    for chunk in response:
        for letter in chunk.text:
            yield letter
            time.sleep(0.01)

# Function to handle uploaded images
def image_image_setup(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    return None

# Generate speech from text using gTTS
def text_to_speech(text):
    tts = gTTS(text)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# Function to animate text highlighting
def highlight_text(text):
    words = text.split()
    num_words = len(words)
    duration = 8  # Total duration of the audio (adjust as needed)
    delay = duration / max(num_words, 1)

    for i in range(num_words):
        highlighted_text = "<p style='font-size:18px; text-align:center;'>"
        for j, word in enumerate(words):
            if j == i:
                highlighted_text += f"<b style='color:#f76b1c; font-size:22px;'>{word}</b> "
            else:
                highlighted_text += f"{word} "
        highlighted_text += "</p>"
        
        st.session_state["highlighted_text"] = highlighted_text
        time.sleep(delay)

# Function to reapply background styling
def apply_custom_style():
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
    [data-testid="stAppViewContainer"] div {
        background-color: transparent !important;
    }
    </style>
    '''
    st.markdown(page_bg_gradient_with_image, unsafe_allow_html=True)

def main():
    # Apply background styling at the start
    apply_custom_style()

    # Display logo
    logo = Image.open("chef.png")
    st.image(logo, width=100)
    
    st.header("Dishify - Your Personal Chef, One Chat Away!")
    
    # Input for text prompt
    user_input = st.text_input("Enter dish or ingredient query here:", key="user_input")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    # Display uploaded image
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Submit button
    submit = st.button("Generate Recipe")
    
    if submit:
        st.session_state["response"] = ""
        response_container = st.empty()

        if uploaded_file:
            image_data = image_image_setup(uploaded_file)
            response_generator = get_gemini_response(user_input, image_data)
        elif user_input:
            response_generator = get_gemini_response(user_input)
        else:
            st.warning("Please provide either an image or a text query.")
            return

        response_text = ""
        for letter in response_generator:
            response_text += letter
            response_container.markdown(f"<p style='white-space: pre-wrap;'>{response_text}</p>", unsafe_allow_html=True)
            apply_custom_style()  # Keep the gradient background

            # **SCROLLING JAVASCRIPT INJECTION**
            st.markdown(
                """  
                <script>
                var container = window.parent.document.querySelector("section[data-testid='stAppViewContainer']");
                container.scrollTop = container.scrollHeight;
                </script>
                """,
                unsafe_allow_html=True
            )

        # Store the generated response
        st.session_state["response"] = response_text

    # Display stored response
    if st.session_state["response"]:
        st.markdown(f"<p style='font-size:18px; white-space: pre-wrap;'>{st.session_state['response']}</p>", unsafe_allow_html=True)
        apply_custom_style()  # Ensure background stays visible

    # Play DIY button for TTS
    if st.session_state["response"]:
        if st.button("🎤 Play The DIY"):
            st.session_state["audio"] = text_to_speech(st.session_state["response"])
            st.session_state["play_tts"] = True
            apply_custom_style()

    # Play audio if available
    if st.session_state["play_tts"] and st.session_state["audio"]:
        audio_bytes = st.session_state["audio"].read()
        audio_b64 = base64.b64encode(audio_bytes).decode()
        st.audio(f"data:audio/mp3;base64,{audio_b64}", format="audio/mp3")

        # Start text animation
        text_animation_thread = threading.Thread(target=highlight_text, args=(st.session_state["response"],))
        text_animation_thread.start()
        apply_custom_style()

    # Display highlighted text during TTS
    if st.session_state["highlighted_text"]:
        st.markdown(st.session_state["highlighted_text"], unsafe_allow_html=True)
        apply_custom_style()

if __name__ == "__main__":
    main()
