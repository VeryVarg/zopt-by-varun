import os
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

#class Person(BaseModel):
 #   name: str
    

prompt = load_prompt('template.json')
user_profile_content = open("user_profile.txt").read()
contextual_data_content = open("contextual_data.txt").read()

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

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


st.title("Order What You Crave With ZoPT AI")
user_input = st.text_area("Heyy! How are you feeling? What would you like to eat? ")

chain = prompt | llm | parser

if st.button("Generate Food Recommendations"):
    result = chain.invoke({
        "user_input": user_input,
        "user_profile": user_profile_content,
        "contextual_data": contextual_data_content
    })
    st.write(result)
