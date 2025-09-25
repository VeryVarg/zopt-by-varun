# 🍽️ Mood-Based Food Recommender Setup Guide

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Google API Key:**
   - Visit https://ai.google.dev/
   - Sign in with your Google account
   - Create a new API key for Gemini
   - Keep your API key secure

3. **Run the Application:**
   ```bash
   streamlit run mood_food_recommender.py
   ```

4. **Access the Web Interface:**
   - Open your browser to `http://localhost:8501`
   - Enter your Google API key in the sidebar
   - Start getting personalized food recommendations!

## File Structure

```
your-project/
├── mood_food_recommender.py    # Main Streamlit application
├── user_profile.txt            # User preferences and history
├── contextual_data.txt         # Current context (time, weather, etc.)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## How It Works

### Algorithm Overview
The system uses a sophisticated 4-phase scoring algorithm:

1. **Mood Analysis (40% weight)** - Analyzes your text input for emotional state
2. **Historical Behavior (30% weight)** - Considers your past food preferences  
3. **Contextual Integration (20% weight)** - Factors in time, weather, location
4. **Demographic Personalization (10% weight)** - Adjusts for age, income, preferences

### Input Requirements

1. **User Input (GUI):** Your current mood/feelings as text
2. **User Profile (File):** Your preferences, history, demographics
3. **Contextual Data (File):** Current time, weather, location info

### Technology Stack

- **Frontend:** Streamlit (Web Interface)
- **LLM:** Google Gemini 2.0 Flash
- **Framework:** LangChain for LLM orchestration
- **Data Validation:** Pydantic for structured outputs
- **Language:** Python 3.8+

## Customization

### Modifying User Profile
Edit `user_profile.txt` to include:
- Your actual food preferences
- Order history
- Dietary restrictions
- Budget preferences
- Demographics

### Updating Context Data
Edit `contextual_data.txt` to reflect:
- Current time and date
- Local weather conditions
- Your location
- Current situation/stress levels

### Algorithm Tweaks
The algorithm weights can be adjusted in the prompt template within `mood_food_recommender.py`:
- Mood Analysis: Currently 40%
- Historical Behavior: Currently 30%  
- Contextual Integration: Currently 20%
- Demographics: Currently 10%

## Troubleshooting

### Common Issues:

1. **API Key Error:**
   - Ensure your Google API key is correct
   - Check if you have Gemini API access enabled
   - Verify billing is set up if required

2. **File Not Found:**
   - Ensure `user_profile.txt` and `contextual_data.txt` exist
   - Check file permissions and encoding (UTF-8)

3. **Import Errors:**
   - Run `pip install -r requirements.txt`
   - Check Python version (3.8+ required)
   - Consider using a virtual environment

4. **Rate Limiting:**
   - Google API has usage limits
   - Wait a few minutes between requests if hitting limits
   - Check your API quota in Google Cloud Console

## Advanced Features

### Structured Output
The system uses Pydantic models to ensure consistent response formatting:
- `RecommendationResponse` - Main output structure
- `FoodRecommendation` - Individual recommendation format

### LangChain Integration
- Uses `ChatGoogleGenerativeAI` for Gemini access
- Implements `PromptTemplate` for consistent prompting
- Leverages `with_structured_output()` for JSON mode

### Safety & Privacy
- API keys are handled securely through Streamlit's sidebar
- No data is stored permanently
- All processing happens in real-time

## Contributing

Feel free to enhance the algorithm by:
1. Adding more sophisticated mood detection
2. Implementing user feedback loops
3. Adding more contextual factors
4. Improving the UI/UX

## License

This project is open source and available under the MIT License.
