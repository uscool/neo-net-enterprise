import os
import google.generativeai as genai
import re
from dotenv import load_dotenv

load_dotenv("auth.env")

gemini_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=gemini_api_key)

def configure_genai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: Please set the GEMINI_API_KEY environment variable")
        exit(1)
    genai.configure(api_key=api_key)

def get_gemini_model():
    return genai.GenerativeModel('gemini-pro')

def generate_survey_questions(topic, audience, num_questions=10):
    model = get_gemini_model()
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
    
    response = model.generate_content(prompt)
    return response.text

def analyze_company_and_find_investors(company_description, products, industry, stage):
    model = get_gemini_model()
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
    
    response = model.generate_content(prompt)
    return response.text

def main():
    
    while True:
        print("\nAI-Powered Startup Assistant")
        print("1. Generate Market Research Survey")
        print("2. Find Investors and Pitch Recommendations")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            topic = input("What product/service are you researching? ")
            audience = input("Who is your target audience? ")
            num_questions = input("Number of questions (default: 10): ")
            
            if not topic or not audience:
                print("Error: Topic and audience are required")
                continue
                
            try:
                num_questions = int(num_questions) if num_questions else 10
            except ValueError:
                print("Error: Number of questions must be a number")
                continue
                
            print("\nGenerating survey questions...")
            questions = generate_survey_questions(topic, audience, num_questions)
            print("\n--- SURVEY QUESTIONS ---\n")
            print(questions)
            
            filename = input("\nEnter filename to save survey (or press Enter to skip): ")
            if filename:
                with open(filename, 'w') as f:
                    f.write(questions)
                print(f"Survey saved to {filename}")
            
        elif choice == "2":
            company_description = input("Describe your company: ")
            industry = input("What industry are you in? ")
            stage = input("Company stage (e.g., Pre-seed, Seed, Series A): ")
            products_input = input("List your products (separated by commas): ")
            
            if not company_description or not industry:
                print("Error: Company description and industry are required")
                continue
                
            products = [p.strip() for p in products_input.split(",") if p.strip()]
            if not products:
                print("Error: At least one product is required")
                continue
            
            print("\nAnalyzing your company and finding investors...")
            investor_data = analyze_company_and_find_investors(
                company_description, products, industry, stage
            )
            print("\n--- INVESTOR RECOMMENDATIONS ---\n")
            print(investor_data)
            
            filename = input("\nEnter filename to save recommendations (or press Enter to skip): ")
            if filename:
                with open(filename, 'w') as f:
                    f.write(investor_data)
                print(f"Recommendations saved to {filename}")
            
        elif choice == "3":
            print("Exiting. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

main()