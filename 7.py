import tkinter as tk
from tkinter import ttk, scrolledtext
from dotenv import load_dotenv
import os
from google import genai

def load_api_key():
    load_dotenv("auth.env")
    return os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=load_api_key())

def finding_hashtags(industry):
    response=client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"generate a list of 10 trending social media hashtags related to the {industry} industry. I need only hashtags as output no explanation, nothing else."]

    )
    if response.text:
        hashtags = response.text.split("\n")
        return [tag.strip() for tag in hashtags if tag.startswith("#")]
    else:
        return ["No hashtags found."]
    
def suggestions(hashtags):
    response=client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"I'm a company who wants to use these hashtags for advertising: {', '.join(hashtags)} give me recommendations on how to use them."]

    )
    print("\nMarketing Recommendations:\n")
    print(response.text)

def main():
    industry = input("Enter industry or advert term: ")
    hashtags = finding_hashtags(industry)
    print("\nTrending Hashtags are:")
    print(", ".join(hashtags))
    suggestions(hashtags)

main()
