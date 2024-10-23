import streamlit as st
from gtts import gTTS
from io import BytesIO
import base64

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

# Sample output text from your nutrition app (replace this with actual output)
output_text = """
1. Apple - 95 calories
2. Banana - 105 calories
3. Orange - 62 calories
-------
Total Calories: 262
The meal is healthy!
"""

# Display the text output in the Streamlit app
st.header("Nutrition Analysis")
st.write(output_text)

# Add a button to generate speech
if st.button("Play Nutrition Analysis as Speech"):
    # Convert the output text to speech
    audio_data = text_to_speech(output_text)
    # Play the generated audio in the app
    play_audio(audio_data)
