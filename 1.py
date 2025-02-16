import tkinter as tk
from tkinter import simpledialog, messagebox
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

def large_input_dialog(title, prompt):
    """Creates a larger input dialog with a big entry box."""
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.geometry("400x200")
    dialog.configure(bg="#2C3E50")

    tk.Label(dialog, text=prompt, font=("Arial", 12), wraplength=380, bg="#2C3E50", fg="white").pack(pady=10)
    
    entry = tk.Entry(dialog, font=("Arial", 14), width=50, bg="#ECF0F1", fg="#2C3E50")
    entry.pack(pady=10, padx=10)

    result = []

    def submit():
        result.append(entry.get())
        dialog.destroy()

    submit_button = tk.Button(dialog, text="Submit", command=submit, font=("Arial", 12), bg="#27AE60", fg="white")
    submit_button.pack(pady=10)

    dialog.wait_window()
    return result[0] if result else None

def asking_user_togive_headers(allheaders):
    userdata = {}
    for i, field in enumerate(allheaders):
        if i >= 5:
            break
        userdata[field] = large_input_dialog("Input", f"{field}:")
    return userdata

def showing_candidates(role, user_inputs):
    user_inputs_str = json.dumps(user_inputs)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[f"I need to hire {role}. Based on these details:\n{user_inputs_str}\nSuggest ideal candidate profiles. Give me a relevant search term I should use in LinkedIn to search for such a candidate. Don't give extra info, just the details I need to enter in LinkedIn to search users with that criteria."]
    )
    return response.text

def search_linkedin_profiles(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={custom_search_api_key}&cx={search_engine_id}&q={query}+Mumbai"
    response = requests.get(url)
    results = response.json()
    return results

def main():
    root = tk.Tk()
    root.withdraw()
    
    role = large_input_dialog("Input", "What role are you looking to hire? (e.g. Developer, Designer):")
    if not role:
        return
    
    allheaders = get_dheader_to_ask_user(role)
    user_inputs = asking_user_togive_headers(allheaders)
    recommendations = showing_candidates(role, user_inputs)
    
    messagebox.showinfo("Recommended Search Term", recommendations)
    
    linkedin_profiles = search_linkedin_profiles(recommendations)
    result_text = "LinkedIn Profiles:\n\n"
    
    for item in linkedin_profiles.get('items', []):
        result_text += f"Title: {item['title']}\nLink: {item['link']}\n\n"
    
    if not linkedin_profiles.get('items'):
        result_text += "No profiles found."
    
    messagebox.showinfo("LinkedIn Search Results", result_text)

main()
