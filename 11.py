import os
import google.generativeai as genai
import fitz  # PyMuPDF for reading PDFs
from dotenv import load_dotenv

load_dotenv("auth.env")

gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)

MODEL_NAME = 'gemini-1.0-pro'
model = genai.GenerativeModel(MODEL_NAME)


def load_laws_from_pdf(filepath):
    """Loads laws from a PDF file, assuming one law per line."""
    try:
        doc = fitz.open(filepath)
        laws = []
        for page in doc:
            text = page.get_text() 
            lines = text.splitlines() 
            laws.extend([line.strip() for line in lines if line.strip()])
        doc.close()
        return laws
    except FileNotFoundError:
        print(f"Error: Law PDF file not found at {filepath}")
        return []
    except Exception as e:
        print(f"Error reading law PDF file: {e}")
        return []


def analyze_decision_vs_laws(decision_text, laws, model):
    """
    Analyzes a business decision against a list of laws using Gemini.

    Args:
        decision_text (str): The text describing the business decision.
        laws (list): A list of strings, where each string is a law.
        model: The Gemini model to use.

    Returns:
        list: A list of laws that the decision potentially violates,
              or returns no violation found.  Also returns a list of rationales,
              explaining why each law could be violated if a law is violated.
    """

    if not laws:
        print("Warning: No laws provided for analysis.")
        return [], []

    prompt = f"""
You are an expert legal analyst.  You must carefully analyze the following business decision and compare it to the following laws.

Business Decision:
{decision_text}

Laws:
{chr(10).join(laws)}  # Join laws with newline character

Analyze whether the business decision potentially violates any of the listed laws.
For each law, provide a clear and concise explanation of how the decision could violate it.
If a law is not violated, you should EXPLICITLY state "No violation".
Your response should follow this format EXACTLY:

Law: [Law text]
Violation: [Explanation of violation OR "No violation"]

Begin!
"""

    try:
        response = model.generate_content(prompt)
        response_text = response.text

        violations = []
        rationales = []
        current_law = None
        current_violation = None

        for line in response_text.splitlines():
            line = line.strip()

            if line.startswith("Law:"):
                current_law = line[len("Law:"):].strip()
            elif line.startswith("Violation:"):
                current_violation = line[len("Violation:"):].strip()  

            if current_law is not None and current_violation is not None:
                if current_violation != "No violation":
                    violations.append(current_law)
                    rationales.append(current_violation)
                current_law = None 
                current_violation = None

        return violations, rationales

    except Exception as e:
        print(f"Error during Gemini analysis: {e}")
        return [], []


if __name__ == "__main__":
    law_file_path = "laws.pdf" 
    laws = load_laws_from_pdf(law_file_path)
    business_decision = input("Enter the business decision to analyze: ")

    violations, rationales = analyze_decision_vs_laws(business_decision, laws, model)
    if violations:
        print("Potential Law Violations:")
        for i, law in enumerate(violations):
            print(f"- {law}")
            print(f"  Rationale: {rationales[i]}")  # Print the rationale
    else:
        print("No potential law violations found.")
