import tkinter as tk
from tkinter import ttk, scrolledtext
from dotenv import load_dotenv
import os
from google import genai

# Load API Key
def load_api_key():
    load_dotenv("auth.env")
    return os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=load_api_key())

# Generate Insights from API
def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text

def get_market_insights():
    industry = industry_entry.get().strip()
    if not industry:
        output_text.insert(tk.END, "⚠ Please enter an industry.\n", "warning")
        return

    status_label.config(text="⏳ Generating insights...", foreground="blue")
    root.update_idletasks()

    prompt = f"Get latest market insights and growth domains for the {industry} industry from sources like Moneycontrol, Jefferies, and JP Morgan. Summarize key findings with accurate numeric data. List Sources."
    
    insights = generate_response(prompt)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, insights)
    status_label.config(text="✅ Insights generated successfully!", foreground="green")

# Clear Output
def clear_output():
    output_text.delete(1.0, tk.END)
    status_label.config(text="")

# GUI Setup
root = tk.Tk()
root.title("Market Insights Generator")
root.geometry("700x500")
root.configure(bg="#f8f9fa")

title_label = ttk.Label(root, text="📊 AI Market Insights", font=("Arial", 16, "bold"), background="#f8f9fa", foreground="#007BFF")
title_label.pack(pady=10)

input_frame = ttk.Frame(root, padding=10)
input_frame.pack(pady=5)

ttk.Label(input_frame, text="Enter Industry:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
industry_entry = ttk.Entry(input_frame, width=40, font=("Arial", 12))
industry_entry.grid(row=0, column=1, padx=5, pady=5)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

generate_button = ttk.Button(button_frame, text="🔍 Generate Insights", command=get_market_insights, style="Primary.TButton")
generate_button.grid(row=0, column=0, padx=5, pady=5)

clear_button = ttk.Button(button_frame, text="🧹 Clear Output", command=clear_output, style="Secondary.TButton")
clear_button.grid(row=0, column=1, padx=5, pady=5)

output_text = scrolledtext.ScrolledText(root, width=80, height=15, font=("Arial", 10), bd=2, relief="sunken", wrap=tk.WORD)
output_text.pack(pady=10, padx=10)

status_label = ttk.Label(root, text="", font=("Arial", 10), background="#f8f9fa", foreground="gray")
status_label.pack(pady=5)

style = ttk.Style()
style.configure("TButton", font=("Arial", 11), padding=5)
style.configure("Primary.TButton", background="#007BFF", foreground="black")
style.configure("Secondary.TButton", background="#6c757d", foreground="black")

root.mainloop()
