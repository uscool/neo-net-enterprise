import tkinter as tk
from tkinter import scrolledtext
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

def get_market_insights():
    industry = industry_entry.get()
    if not industry:
        output_text.insert(tk.END, "Please enter an industry.\n")
        return
    prompt = f"Get latest market insights and growth domains for the {industry} industry from sources like Moneycontrol, Jefferies, and JP Morgan. Summarize key findings with accurate numeric data. List Sources"
    insights = generate_response(prompt)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, insights)

# GUI Setup
root = tk.Tk()
root.title("Market Insights Generator")
root.geometry("600x400")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Enter Industry:", font=("Arial", 12), bg="#f0f0f0", fg="#333").pack(pady=5)
industry_entry = tk.Entry(root, width=50, font=("Arial", 12), bd=2, relief="groove")
industry_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Insights", font=("Arial", 12, "bold"), bg="#007BFF", fg="white", relief="raised", padx=10, pady=5, command=get_market_insights)
generate_button.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, width=70, height=15, font=("Arial", 10), bd=2, relief="sunken", wrap=tk.WORD)
output_text.pack(pady=10)

root.mainloop()
