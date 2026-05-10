# 🍽️ ZoPT: Zomato Personalized Ordering AI

**🔗 Try the App:** [https://zopt-by-varungarg.streamlit.app/](https://zopt-by-varungarg.streamlit.app/)

## 1. Executive Summary
ZoPT is an AI-driven, conversational food ordering interface designed to solve the limitations of traditional graphical UIs (GUIs) in food delivery apps like Zomato. By leveraging natural language processing, ZoPT translates complex user intent, context, and historical behavior into precise, tailored food recommendations. 

**Why ZoPT Wins Over Traditional GUIs (Zomato):**
1. **Ambiguous, multi-constraint goal articulation**
   * *"Order something light, under ₹200, no onion-garlic, delivers in under 25 mins, not Chinese"*
   * Traditional filter systems require users to manually locate and apply multiple specific filters. ZoPT handles this natively as a single, conversational intent.
2. **Edge cases and exceptions the UI didn’t anticipate**
   * *"My last order from Paradise was wrong — reorder but replace the raita with extra naan and apply my remaining Zomato credits"*
   * GUI flows break on highly specific compound operations. Chat handles the composition and overrides naturally.
3. **"Change of plans" mid-flow situations**
   * Research shows GUIs win on "happy-path" flows, but chat wins when users need to deviate — *"actually, make it for 3 people, split the order between two addresses, and schedule for 8pm"*. 

---

## 2. The Problem: User Pain Points
Modern food delivery apps rely on categorical searching, hard-coded filters, and static carousels. This causes friction when:
* **Decision Fatigue**: Users are overwhelmed by options and spend an excessive amount of time deciding what to eat.
* **Rigid Flows**: Standard apps assume a linear ordering process. Deviating from the path (e.g., splitting orders, substituting items across past orders) requires frustrating workarounds.
* **Context Blindness**: Standard algorithms rely primarily on past orders, often ignoring the user's immediate emotional state, weather, or real-time intent.

---

## 3. The Solution: Reasoning & Algorithm Inputs
To provide magical, hyper-personalized recommendations, ZoPT dynamically weighs multiple data vectors to create a scored output.

### Algorithm Design
The system uses a sophisticated scoring logic to rank food options:
* **Mood & Intent Analysis (40%)**: Translates free-form text into an emotional/activity state (e.g., stressed, tired, craving comfort).
* **Historical Behavior (30%)**: Matches recommendations against past orders and established culinary preferences.
* **Contextual Integration (20%)**: Pulls variables like time of day, weather conditions, and day of the week to suggest situationally appropriate food (e.g., warm soups during rain).
* **Demographic Personalization (10%)**: Tunes recommendations strictly within budget, dietary constraints, and regional affinities.

### The Inputs
* **User Prompt**: The chat interface captures nuanced intent flawlessly.
* **user_profile.txt**: Acts as the backend "database" storing dietary limitations, average order value, demographics, and frequent items.
* **contextual_data.txt**: Simulates the real-time device signals (GPS, Clock, Weather API).

---

## 4. How to Run and Test (For QA / Local Dev)

If you'd like to test the logic loops and algorithms locally:

1. **Setup the Environment:**
   Run the following to create your virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure the AI Provider:**
   Create a `.env` file in the root directory and add your OpenAI API Key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Test the Variables:**
   * Edit `user_profile.txt` to simulate different user personas (e.g., strict vegan vs. meat lover).
   * Edit `contextual_data.txt` to simulate different environmental triggers (e.g., Rainy Friday Night vs. Hot Monday Morning).

4. **Run the Application:**
   ```bash
   streamlit run streamlit_app.py
   ```
   Open `http://localhost:8501`, input a conversational request (e.g., "I'm exhausted and it's pouring rain, get me something comforting"), and review the analytical breakdown of why specific foods were chosen.
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
