from dotenv import load_dotenv
import os
from google import genai

def load_api_key():
    load_dotenv("auth.env")
    return os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=load_api_key())

def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text

def market_insights():
    industry = input("Enter the industry you want insights on: ")
    prompt = f"Get latest market insights and growth domains for the {industry} industry from sources like Moneycontrol, Jefferies, and JP Morgan. Summarize key findings with accurate numeric data.List Sources"
    print(generate_response(prompt))

market_insights()