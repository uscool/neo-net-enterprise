from google import genai
from dotenv import load_dotenv
import os

load_dotenv("auth.env")
api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=api_key)

def finding_hashtags(industry):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"generate a list of 10 trending social media hashtags related to the {industry} industry. I need only hashtags as output, no explanation, nothing else."]
    )
    if response.text:
        hashtags = response.text.split("\n")
        return [tag.strip() for tag in hashtags if tag.startswith("#")]
    else:
        return ["No hashtags found."]

def main():
    industry = input("Enter industry or related advert term: ")
    hashtags = finding_hashtags(industry)
    print("\nTrending Hashtags are:")
    print(", ".join(hashtags))

main()
