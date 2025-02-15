from google import genai
import json
from dotenv import load_dotenv
import os
import requests

load_dotenv("auth.env")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
custom_search_api_key = os.getenv("CUSTOM_SEARCH_API_KEY")
search_engine_id = os.getenv("SEARCH_ENGINE_ID")

def get_dheader_to_ask_user(jobrole):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"What would you need to know to help me decide what profile to search for when hiring a {jobrole}? Give in list and do not give any preface and para info just give headers in list. Just provide headers for what's needed. Give directly from point 1 no pretexts and explanations."]
    )
    return response.text.split("\n")

def asking_user_togive_headers(allheaders):
    userdata = {}
    print("\nPlease provide the following details:")
    i = 1
    for field in allheaders:
        if i > 5:
            break
        userdata[field] = input(f"{field}: ")
        i += 1
    return userdata

def showing_candidates(role, user_inputs):
    user_inputs_str = json.dumps(user_inputs)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"I need to hire {role}. Based on these details:\n{user_inputs_str}\nSuggest ideal candidate profiles. Give me a relevant search term I should use in LinkedIn to search for such a candidate. Don't give extra info, just the details I need to enter in LinkedIn to search users with that criteria."]
    )
    return response.text

def search_linkedin_profiles(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={custom_search_api_key}&cx={search_engine_id}&q={query}"
    response = requests.get(url)
    results = response.json()
    return results

def main():
    role = input("What role are you looking to hire? (e.g. Developer, Designer): ")
    allheaders = get_dheader_to_ask_user(role)
    user_inputs = asking_user_togive_headers(allheaders)
    recommendations = showing_candidates(role, user_inputs)
    print("\nRecommended candidate profiles:\n")
    print(recommendations)

    search_query = recommendations  # Use the generated recommendations as the search query
    linkedin_profiles = search_linkedin_profiles(search_query)
    print("\nLinkedIn Profiles:\n")
    for item in linkedin_profiles.get('items', []):
        print(f"Title: {item['title']}\nLink: {item['link']}\n")

main()
