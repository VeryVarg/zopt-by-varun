import json

# Let's cleanly recreate the whole file
data = {
    "name": None,
    "input_variables": [
        "contextual_data",
        "user_input",
        "user_profile"
    ],
    "optional_variables": [],
    "output_parser": None,
    "partial_variables": {},
    "metadata": None,
    "tags": None,
    "template_format": "f-string",
    "validate_template": True,
    "_type": "prompt"
}

from pathlib import Path
content = Path("prompt_gen.py").read_text() if Path("prompt_gen.py").exists() else ""

template_str = """
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

**PHASE 1: HISTORICAL BEHAVIOR ANALYSIS (45% weight)
Primary signal. Highest signal-to-noise ratio. Treat as the anchor layer.

From user_profile order history:
- Ordered same item 5+ times (strong habit signal): +90 points
- Ordered same item 2-4 times: +70 points
- Ordered within last 7 days (recency peak window): +80 points
- Ordered within 8-14 days: +50 points
- Top 2 cuisines by frequency (past 90 days): +60 points
- Items rated 4+ stars by user: +50 points
- Items consistently skipped after being shown (implicit negative): -60 points
- Items explicitly removed from cart: -80 points

Behavioral economics note: Recency and frequency together form the RFM (Recency-Frequency-Monetary) core of habit prediction. Weight recency 1.5x frequency for dinner; reverse for breakfast (breakfast is highest-recurrence meal).

---

PHASE 2: CONTEXTUAL INTEGRATION (20% weight)
High-precision, low-noise signals. Context eliminates irrelevant items before scoring.

Time-of-day hard filters (eliminate before scoring):
- 7-10 AM: Remove items with prep time >25 mins; deprioritize heavy meals
- 12-2 PM: Neutral; prioritize "quick + filling" slot
- 4-7 PM: Snacks and street food window; boost lighter formats
- 8-11 PM: Full-meal window; boost restaurant mains
- 11 PM-5 AM: Late-night window; boost quick, comfort-heavy items

Time-of-day scoring boost (post-filter):
- Apply +50 points to items in their natural consumption window (e.g., poha at 8 AM, biryani at 8 PM)

Weather modifiers (apply after time scoring):
- Monsoon: +40 points for fried items (Pakoras, Samosas, Vada Pav)
- Winter: +35 points for warm, heavy dishes (Nihari, Dal Makhani, Maggi)
- Summer: +35 points for cooling items (Kulfi, Lassi, Cold Coffee, Chaas)
- Rainy + cold night: combine both modifiers, cap at +55

Day-of-week signal:
- Weekday: boost habitual, familiar items (recurrence strength is higher on weekdays [research-backed])
- Weekend: apply +20 points for discovery/indulgent items (biryani feasts, new cuisines)

---

PHASE 3: MOOD ANALYSIS (25% weight)
Real signal, but volatile. Use as modifier on top of behavioral + contextual anchor. Do not let mood override established habit.

From user_input text — run sentiment + emotion NLP:

Negative valence detected (stress, anxiety, sadness):
- +80 points for personal comfort foods (cross-reference user's own historical "feel-good" orders first)
- If no personal comfort food history: +60 points for category defaults (warm, creamy, carb-heavy items)
- Apply dopamine-reset heuristic: favor items user has previously ordered under similar mood signals (requires mood-tagging in order history)

Positive valence detected (celebration, excitement):
- +70 points for indulgent, premium, or shareable items
- +50 points for cuisine exploration (novel items user hasn't ordered before)

Boredom / neutral detected:
- +60 points for snack formats and street food
- +30 points for variety: boost second-ranked cuisine over top-ranked (break the loop)

Ambiguous / no mood signal:
- Reduce Phase 3 weight to 10%; redistribute to Phase 1 (+10%) and Phase 2 (+5%)

Gender-based comfort modifiers (apply cautiously — use only if statistically validated in user cohort A/B tests):
- Do not hardcode gender-food stereotypes; use cohort-level behavioral data to derive, not assumption

---

PHASE 4: DEMOGRAPHIC & PLATFORM PERSONALIZATION (10% weight)
Weakest signal. Use as tie-breaker, not as driver. Primarily a budget and discovery filter.

Age-cohort adjustments (use as soft boost, not elimination):
- Gen Z / Millennials (18-30): +20 points for "trending" items (high reorder rate in peer cohort within last 72 hours)
- 31-45: +20 points for proven, reliable cuisine options with strong ratings
- 45+: +20 points for traditional, familiar formats

Budget hard filter (non-negotiable, applied before any scoring):
- Eliminate all items above user's stated or inferred price ceiling
- Inferred ceiling = 1.3x of user's median order value (last 60 days)

Discovery injection (prevents filter bubble):
- Reserve 1 of every 5 recommendation slots for a novel item outside the user's top-3 cuisine history
- This mirrors Uber Eats' diversity objective in multi-objective optimization

Collaborative filtering overlay:
- If item scores are tied (within 5 points), surface the item preferred by users with >80% behavioral profile similarity (Zomato-style collaborative filtering)

---

FINAL SCORING FORMULA:
FinalScore = (Phase1_score × 0.45) + (Phase2_score × 0.20) + (Phase3_score × 0.25) + (Phase4_score × 0.10)

DYNAMIC WEIGHT ADJUSTMENT:
- If user is new (< 3 orders): Redistribute Phase 1 weight → Phase 3 (mood) and Phase 4 (demographics) to handle cold-start
  New user weights: Phase1=15%, Phase2=20%, Phase3=40%, Phase4=25%
- If mood signal confidence < 0.6 (ambiguous input): Drop Phase 3 to 10%, add 15% to Phase 1
- If time is late-night (11PM-5AM): Boost Phase 2 to 30%; reduce Phase 3 to 15%**Constraint Handling:**
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
"""

data["template"] = template_str

with open('template.json', 'w') as f:
    json.dump(data, f, indent=4)

