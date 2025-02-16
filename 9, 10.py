import os
from dotenv import load_dotenv
import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk

def get_gemini_model():
    load_dotenv("auth.env")
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your auth.env file or environment.")
    genai.configure(api_key=api_key)
    return genai

def generate_analysis(startup_details, analysis_type):
    try:
        model = get_gemini_model()
        gemini = model.GenerativeModel('gemini-pro')
        
        prompts = {
            "clients": f"""
            Based on the following startup information, identify potential clients and market entry strategies:

            Industry: {startup_details['industry']}
            Product/Service: {startup_details['product']}
            Target Market: {startup_details['target_market']}
            Value Proposition: {startup_details['value_proposition']}

            Provide detailed insights on client segmentation, conversion strategies, and marketing channels.
            """,
            "competitors": f"""
            Provide a detailed competitor analysis for a startup in the following space:

            Industry: {startup_details['industry']}
            Product/Service: {startup_details['product']}
            Target Market: {startup_details['target_market']}
            Key Features: {startup_details['key_features']}

            Include SWOT analysis, pricing strategies, and competitor gaps.
            """,
            "market_entry": f"""
            Analyze market entry strategies for:

            Industry: {startup_details['industry']}
            Product/Service: {startup_details['product']}
            Target Market: {startup_details['target_market']}
            Available Resources: {startup_details['resources']}

            Provide effective strategies, risk assessments, and success metrics.
            """
        }
        
        response = gemini.generate_content(prompts[analysis_type])
        return response.text
    except Exception as e:
        return f"Error generating analysis: {e}"

def analyze(option):
    startup_details = {
        "industry": industry_entry.get(),
        "product": product_entry.get(),
        "target_market": market_entry.get(),
        "value_proposition": value_entry.get(),
        "key_features": features_entry.get(),
        "resources": resources_entry.get()
    }
    
    analysis_types = {"Clients": "clients", "Competitors": "competitors", "Market Entry": "market_entry"}
    result = generate_analysis(startup_details, analysis_types[option])
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, result)

def save_analysis():
    content = output_text.get(1.0, tk.END).strip()
    if not content:
        messagebox.showwarning("Warning", "No analysis to save!")
        return
    filename = "analysis.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    messagebox.showinfo("Success", f"Analysis saved to {filename}")

# GUI Setup
root = tk.Tk()
root.title("Market Analysis Tool")
root.geometry("800x700")
root.configure(bg="#e3f2fd")

title_label = tk.Label(root, text="Market Analysis Tool", font=("Arial", 16, "bold"), bg="#e3f2fd", fg="#0d47a1")
title_label.pack(pady=10)

frame = tk.Frame(root, bg="#e3f2fd")
frame.pack(pady=5)

fields = ["Industry", "Product/Service", "Target Market", "Value Proposition", "Key Features", "Resources Available"]
entries = {}
for field in fields:
    tk.Label(frame, text=field + ":", font=("Arial", 10), bg="#e3f2fd", fg="#0d47a1").pack(anchor="w")
    entry = tk.Entry(frame, width=70)
    entry.pack(pady=2)
    entries[field] = entry

industry_entry, product_entry, market_entry, value_entry, features_entry, resources_entry = (entries[field] for field in fields)

button_frame = tk.Frame(root, bg="#e3f2fd")
button_frame.pack(pady=10)

style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"), padding=5)

btn_clients = ttk.Button(button_frame, text="Find Potential Clients", command=lambda: analyze("Clients"))
btn_clients.grid(row=0, column=0, padx=5, pady=5)

btn_competitors = ttk.Button(button_frame, text="Analyze Competitors", command=lambda: analyze("Competitors"))
btn_competitors.grid(row=0, column=1, padx=5, pady=5)

btn_market_entry = ttk.Button(button_frame, text="Analyze Market Entry", command=lambda: analyze("Market Entry"))
btn_market_entry.grid(row=0, column=2, padx=5, pady=5)

btn_save = ttk.Button(root, text="Save Analysis", command=save_analysis)
btn_save.pack(pady=5)

output_frame = tk.Frame(root, bg="#bbdefb")
output_frame.pack(pady=10, padx=20, fill="both", expand=True)

output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=90, height=20, font=("Arial", 10), bg="#e3f2fd", fg="#0d47a1", padx=10, pady=10)
output_text.pack(fill="both", expand=True)

root.mainloop()
