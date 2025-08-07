# CalMate Project Structure

```
CalMate/
├── final_app_updated.py    # Main application entry point
├── apps/                   # Application modules
│   ├── CalMate.py         # Calorie analysis module
│   └── dishify.py         # Recipe generation module
├── assets/                 # Static assets (images, logos)
│   ├── CalMate-bg.png     # CalMate logo
│   ├── chef.png           # Dishify logo
│   └── *.png, *.jpeg      # Other image assets
├── images/                 # Image resources
│   └── testing/           # Test images for the application
├── docs/                   # Documentation
│   └── README.md          # Project documentation
├── legacy/                 # Old/unused files (kept for reference)
│   ├── app.py
│   ├── final_app.py
│   └── other legacy files
├── requirements.txt        # Python dependencies
└── .env                   # Environment variables (create this)
```

## Main Files:
- **final_app_updated.py**: Main Streamlit application with navigation
- **apps/CalMate.py**: Calorie analysis and nutrition tracking
- **apps/dishify.py**: Recipe generation and cooking assistance

## Setup:
1. Create a `.env` file with your `GEMINI_API_KEY`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run final_app_updated.py`