# Calmate - Your Personal Chef Assistant 🍽️

**Calmate** combines the culinary expertise of **Dishify** and the nutritional insights of **Calmate (AI Nutritionist)**, all in a single, intuitive app designed to enhance your cooking experience and nutritional well-being.

## Features

### Dishify 🧑‍🍳
Dishify acts as your personal chef:
- **Image Upload:** Upload an image of any dish, and Dishify will guide you through making it.
- **Detailed Instructions:** Provides a clear list of ingredients with measurements, followed by step-by-step cooking instructions, perfect for beginners.
- **Interactive AI Chef:** Ask cooking-related questions, and Dishify responds with precise directions.
  
### Calmate - Calorie Calculator 🍎
Calmate is your AI-powered nutritionist:
- **Nutritional Analysis:** Upload an image of your meal, and Calmate will analyze it to estimate its calorie count and key nutritional information.
- **Fitness Tips:** Receive customized advice on staying fit and ways to make the meal more nutritious.
- **AI Recommendations:** Get suggestions on balanced meals, caloric adjustments, and dietary tips to support a healthy lifestyle.


## Environment Setup
- Google Gemini API Key: Obtain an API key from Google and add it to the .env file as shown above.
- Google Text-to-Speech (gTTS): The project uses gTTS for converting recipe text to audio.

## Usage

1. **Image Upload**: Use the file uploader to upload an image of your dish.
2. **Request Analysis**: Click on "Tell me how to make this" (Dishify) or "Analyze Nutritional Content" (Calmate) to get detailed information.
3. **Calmate’s Health Tips**: For calorie and nutritional information, check out additional fitness and dietary tips provided after analysis.

## Technologies Used
- **Streamlit**: For the app’s front-end interface.
- **Google Gemini AI**: Powers the Dishify chatbot’s responses.
- **gTTS (Google Text-to-Speech)**: Enables audio playback for the cooking instructions.
- **PIL (Python Imaging Library)**: Manages image handling and processing.

Dishify UI
![image](https://github.com/user-attachments/assets/0ee7b163-73ae-433c-a6fe-7f44b7fbf88c)

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/calmate-chef-assistant.git
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the app:
    ```bash
    streamlit run app.py
    ```
4. Ensure your Google Gemini API key is set in your environment variables (`GEMINI_API_KEY`).

## Future Enhancements
- **Recipe Suggestions**: Based on the user’s dietary preferences.
- **Food Recognition**: Automatically identify food items without manual input.

## Feedback
Have feedback or suggestions? Contact us 

---

