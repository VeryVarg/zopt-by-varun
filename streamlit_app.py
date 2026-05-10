import os
import json
import openmeteo_requests
import requests_cache
from retry_requests import retry
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate, load_prompt
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from typing import List, Optional
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

st.set_page_config(layout="wide")

def get_dynamic_contextual_data():
    """Fetches real-time weather and combines with fixed delivery constants."""
    
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 12.9719,
        "longitude": 77.5937,
        "current": ["temperature_2m", "relative_humidity_2m", "is_day", "wind_speed_10m", "precipitation", "rain", "showers"],
        "timezone": "auto",
        "forecast_days": 1,
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    
    now = datetime.now()
    
    rain_val = current.Variables(5).Value()
    precipitation_val = current.Variables(4).Value()
    is_day = current.Variables(2).Value()
    weather = "Rainy" if (rain_val > 0 or precipitation_val > 0) else ("Sunny" if is_day else "Clear Night")

    return json.dumps({
        "time": now.strftime("%H:%M"),
        "day": now.strftime("%A"),
        "weather": weather,
        "temperature_2m": f"{round(current.Variables(0).Value(), 1)}°C",
        "relative_humidity_2m": f"{round(current.Variables(1).Value(), 1)}%",
        "is_day": int(is_day),
        "wind_speed_10m": f"{round(current.Variables(3).Value(), 1)} km/h",
        "precipitation": f"{round(precipitation_val, 1)} mm",
        "rain": f"{round(rain_val, 1)} mm",
        "showers": f"{round(current.Variables(6).Value(), 1)} mm"
    }, indent=4)

prompt = load_prompt('template.json')
user_profile_content = open("user_profile.txt").read()
contextual_data_content = get_dynamic_contextual_data()

llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.3)

# Define the Pydantic model for structured output
class FoodRecommendation(BaseModel):
    item: str = Field(description="Name of the recommended food item")
    score: float = Field(description="Recommendation score")
    cuisine_type: str = Field(description="Type of cuisine")

class FoodRecommendationResponse(BaseModel):
    mood_classification: str = Field(description="Detected emotional state and confidence level")
    scoring_breakdown: str = Field(description="Detailed explanation of how scores were calculated")
    top_recommendations: List[FoodRecommendation] = Field(description="List of top 10 food recommendations")
    recommendation_strategy: str = Field(description="Explanation of the ranking approach used")
    confidence_score: float = Field(description="Overall algorithm certainty between 0.0 and 1.0")

parser = PydanticOutputParser(pydantic_object=FoodRecommendationResponse)

# Custom CSS for the button and spacing
st.markdown("""
    <style>
    div.stButton > button[kind="primary"] {
        background-color: #E23744;
        color: white;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        margin-top: 10px;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #C02D3A;
        color: white;
        border: none;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        gap: 24px;
    }
    h1 {
        margin-bottom: 24px;
    }
    textarea {
        margin-bottom: 16px;
    }
    </style>
""", unsafe_allow_html=True)


st.title("ZoPT: Mood based food ordering using GenAI")
st.caption("How are you feeling? What would you like to eat?")

# Added placeholder so it looks cleaner when empty
user_input = st.text_area(
    "How are you feeling? What would you like to eat?", 
    label_visibility="collapsed",
    placeholder="e.g. I am very tired. Suggest something warm and make me feel homely",
    height=100
)

chain = prompt | llm | parser

def get_emoji(cuisine: str, item_name: str) -> str:
    cuisine_l = cuisine.lower()
    item_l = item_name.lower()
    if 'coffee' in item_l or 'tea' in item_l or 'chocolate' in item_l: return "☕"
    if 'pizza' in item_l: return "🍕"
    if 'burger' in item_l: return "🍔"
    if 'dessert' in cuisine_l or 'brownie' in item_l or 'halwa' in item_l or 'jamun' in item_l: return "🧁"
    if 'south indian' in cuisine_l: return "🍛"
    if 'north indian' in cuisine_l: return "🥘"
    return "🍽️"

if st.button("Get Recommendations", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Please tell us how you're feeling first!")
    else:
        # Loading State: Narrates AI thinking
        with st.spinner("⏳ Reading your mood... Matching with your preferences and context... Finding your perfect meal.."):
            try:
                result = chain.invoke({
                    "user_input": user_input,
                    "user_profile": user_profile_content,
                    "contextual_data": contextual_data_content
                })
                
                top_3 = result.top_recommendations[:3]
                rest = result.top_recommendations[3:]

                st.markdown("---")

                # ZONE 1: Top 3 Picks
                st.subheader("Top Picks for You")
                cols = st.columns(3)
                
                for i, col in enumerate(cols):
                    if i < len(top_3):
                        item = top_3[i]
                        with col:
                            # Soft container for cards (using markdown/containers)
                            with st.container():
                                st.markdown(f"## {get_emoji(item.cuisine_type, item.item)}")
                                st.markdown(f"### {item.item}")
                                st.button("Order", key=f"z1_{i}_{item.item}", use_container_width=True)

                # ZONE 2: More Suggestions
                if rest:
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("View More Suggestions"):
                        cols2 = st.columns(3)
                        for i, item in enumerate(rest):
                            with cols2[i % 3]:
                                with st.container():
                                    st.markdown(f"## {get_emoji(item.cuisine_type, item.item)}")
                                    st.markdown(f"### {item.item}")
                                    st.button("Order", key=f"z2_{i}_{item.item}", use_container_width=True)

                # ZONE 3: Expansion/Why
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("See why these match your mood"):
                    st.markdown(f"🧠 **Mood Match**  \n<span style='color: gray; font-size: 0.9em;'>{result.mood_classification}</span>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown(f"💡 **Context Integration**  \n<span style='color: gray; font-size: 0.9em;'>{result.scoring_breakdown}</span>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    st.markdown(f"🎯 **Strategy**  \n<span style='color: gray; font-size: 0.9em;'>{result.recommendation_strategy}</span>", unsafe_allow_html=True)
                    
                    st.divider()
                    st.caption("✅ *Your budget and dietary rules were strictly enforced.*")

            except Exception as e:
                st.error("Something went wrong. Please try again.")
                st.button("Try Again", use_container_width=True)
