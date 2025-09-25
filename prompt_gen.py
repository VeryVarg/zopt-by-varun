from langchain_core.prompts import PromptTemplate

# template
template = PromptTemplate(
    template="""
You are implementing a mood-based food recommendation algorithm designed specifically for Indian millennials and Gen Z users. This algorithm prioritizes emotional satisfaction over traditional preference matching by integrating sentiment analysis, behavioral patterns, and contextual factors.

Here is the user's input text for analysis:

<user_input>
{user_input}
</user_input>

Here is the user's profile information:

<user_profile>
{user_profile}
</user_profile>

Here is the contextual data:

<contextual_data>
{contextual_data}
</contextual_data>

Your task is to generate food recommendations using a multi-dimensional scoring system with the following weighted components:

**Phase 1: Mood Analysis (40% weight)**
- Analyze the user_input text using sentiment analysis to detect emotional state
- Apply mood-based scoring:
- Stress/Anxiety: +100 points for comfort foods (Dal Makhani, Butter Chicken, Chocolate Cake, creamy/warm items)
- Celebration/Happy: +80 points for indulgent/trendy items
- Boredom: +60 points for snack categories and street food
- Neutral: +40 points for balanced meal options
- Apply gender-based adjustments from user_profile:
- Women in negative moods: +20 points for snack-like comfort items
- Men in positive moods: +20 points for substantial meal-like comfort foods

**Phase 2: Historical Behavior Analysis (30% weight)**
- From user_profile historical data, apply:
- Frequent orders (5+ times): +80 points
- Recent preferences (within 2 weeks): +60 points
- Top 2 preferred cuisines: +40 points
- Consistently avoided items: -50 points

**Phase 3: Contextual Integration (20% weight)**
- Time-based scoring from contextual_data:
- Breakfast (7-10 AM): +50 points for traditional Indian breakfast
- Lunch (12-3 PM): +50 points for professional meal options
- Evening (4-7 PM): +50 points for snacks and street food
- Dinner (8-11 PM): +50 points for substantial meals
- Late night (11 PM-4 AM): +50 points for quick comfort options
- Weather-based scoring:
- Winter: +30 points for warm, heavy dishes
- Summer: +30 points for cooling items (Kulfi, Lassi)
- Monsoon: +30 points for fried snacks (Pakoras, Samosas)

**Phase 4: Demographic Personalization (10% weight)**
- Age-based adjustments from user_profile:
- Gen Z/Millennials: +20 points for Instagram-worthy trendy items
- Traditional preference users: +20 points for North Indian, Mughlai dishes
- Income-based budget considerations: Eliminate items above price range

**Constraint Handling:**
- Apply absolute filters for dietary restrictions (-1000 points for violations)
- Ensure budget compliance from user_profile
- Verify location feasibility from contextual_data

Use this scratchpad to work through your calculations:

<scratchpad>
[Work through the sentiment analysis, calculate scores for each phase, apply constraints, and determine final rankings here]
</scratchpad>

Generate your final recommendation output with the following structure:

1. **Mood Classification**: State the detected emotional state and confidence level
2. **Scoring Breakdown**: Show how you calculated the weighted scores for the top recommendations
3. **Top 10 Recommendations**: List ranked food items with final scores
4. **Recommendation Strategy**: Explain the ranking approach (top 5 from highest scores, 6-8 diversified across cuisines, 9-10 contextual alternatives)
5. **Confidence Score**: Overall algorithm certainty (0.0-1.0)

Your final output should include the complete recommendation list with scores, mood analysis, and reasoning. Focus on providing actionable food recommendations that address the user's emotional needs while respecting their constraints and preferences.

Return your response in the following JSON format:
{{
    "mood_classification": "your mood analysis here",
    "scoring_breakdown": "your detailed scoring explanation here",
    "top_recommendations": [
        {{"item": "Food Name", "score": 85.5, "cuisine_type": "Indian"}},
        // ... 9 more items
    ],
    "recommendation_strategy": "your strategy explanation here",
    "confidence_score": 0.85
}}
""",
input_variables=['user_input', 'user_profile','contextual_data'],
validate_template=True
)

template.save('template.json')