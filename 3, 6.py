import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("auth.env")
gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)

def get_gemini_model():
    return genai.GenerativeModel('gemini-pro')

def generate_survey_questions():
    topic = topic_entry.get().strip()
    audience = audience_entry.get().strip()
    num_questions = num_questions_entry.get().strip()

    if not topic or not audience:
        messagebox.showerror("Input Error", "Please enter both Topic and Audience.")
        return

    try:
        num_questions = int(num_questions) if num_questions else 10
    except ValueError:
        messagebox.showerror("Input Error", "Number of questions must be a number.")
        return

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Generating survey questions...\n")

    prompt = f"""
    Create {num_questions} market research questions for {topic}. 
    Target audience: {audience}.
    
    For each question, include:
    1. The question text
    2. The response type (multiple choice, scale 1-5, text response)
    3. If multiple choice, provide the options
    4. The purpose of this question in market research
    
    Format each question clearly with these sections.
    """
    
    response = get_gemini_model().generate_content(prompt)
    output_text.insert(tk.END, response.text)

def analyze_company_and_find_investors():
    company_description = company_entry.get("1.0", tk.END).strip()
    industry = industry_entry.get().strip()
    stage = stage_entry.get().strip()
    products_input = products_entry.get().strip()

    if not company_description or not industry:
        messagebox.showerror("Input Error", "Please enter company description and industry.")
        return

    products = [p.strip() for p in products_input.split(",") if p.strip()]
    if not products:
        messagebox.showerror("Input Error", "Please enter at least one product.")
        return

    output_text_investor.delete(1.0, tk.END)
    output_text_investor.insert(tk.END, "Finding investors...\n")

    prompt = f"""
    Based on the following company information, identify suitable investors and provide pitch recommendations:
    
    Company Description: {company_description}
    Products: {', '.join(products)}
    Industry: {industry}
    Stage: {stage}
    
    Please provide:
    1. A list of 5 specific investors or VC firms that would be a good match for this company overall
    2. For each product, suggest 2 specific investors that would be particularly interested in that product
    3. The key USPs (Unique Selling Propositions) that should be emphasized when pitching to these investors
    4. Specific pitch angles for different types of investors
    
    Format your response in a clear, readable way with section headings.
    """
    
    response = get_gemini_model().generate_content(prompt)
    output_text_investor.insert(tk.END, response.text)

def save_output(output_widget):
    text_content = output_widget.get("1.0", tk.END).strip()
    if not text_content:
        messagebox.showwarning("No Content", "No content to save!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_content)
        messagebox.showinfo("Success", f"Output saved to {file_path}")

root = tk.Tk()
root.title("AI-Powered Startup Assistant")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

survey_frame = ttk.Frame(notebook)
notebook.add(survey_frame, text="📋 Survey Generator")

ttk.Label(survey_frame, text="Topic:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
topic_entry = ttk.Entry(survey_frame, width=40)
topic_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(survey_frame, text="Target Audience:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
audience_entry = ttk.Entry(survey_frame, width=40)
audience_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(survey_frame, text="Number of Questions:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
num_questions_entry = ttk.Entry(survey_frame, width=10)
num_questions_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

generate_survey_button = ttk.Button(survey_frame, text="Generate Questions", command=generate_survey_questions)
generate_survey_button.grid(row=3, column=0, columnspan=2, pady=10)

output_text = scrolledtext.ScrolledText(survey_frame, width=90, height=15, wrap=tk.WORD)
output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

save_button = ttk.Button(survey_frame, text="Save to File", command=lambda: save_output(output_text))
save_button.grid(row=5, column=0, columnspan=2, pady=5)

investor_frame = ttk.Frame(notebook)
notebook.add(investor_frame, text="💰 Investor Finder")

ttk.Label(investor_frame, text="Company Description:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
company_entry = tk.Text(investor_frame, width=60, height=3)
company_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(investor_frame, text="Industry:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
industry_entry = ttk.Entry(investor_frame, width=40)
industry_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(investor_frame, text="Company Stage:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
stage_entry = ttk.Entry(investor_frame, width=40)
stage_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(investor_frame, text="Products (comma-separated):", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
products_entry = ttk.Entry(investor_frame, width=40)
products_entry.grid(row=3, column=1, padx=5, pady=5)

generate_investors_button = ttk.Button(investor_frame, text="Find Investors", command=analyze_company_and_find_investors)
generate_investors_button.grid(row=4, column=0, columnspan=2, pady=10)

output_text_investor = scrolledtext.ScrolledText(investor_frame, width=90, height=15, wrap=tk.WORD)
output_text_investor.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

save_button_investor = ttk.Button(investor_frame, text="Save to File", command=lambda: save_output(output_text_investor))
save_button_investor.grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()
