import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("auth.env")

def configure_genai():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: Please set the GEMINI_API_KEY environment variable")
        exit(1)
    genai.configure(api_key=api_key)

def get_gemini_model():
    return genai.GenerativeModel('gemini-pro')

def calculate_breakeven(startup_details):
    model = get_gemini_model()
    prompt = f"""
    Based on the following startup information, calculate the breakeven point and provide analysis:
    
    Industry: {startup_details['industry']}
    Product/Service: {startup_details['product']}
    Fixed Costs: {startup_details['fixed_costs']}
    Variable Costs: {startup_details['variable_costs']}
    Pricing: {startup_details['pricing']}
    
    Please provide:
    1. Breakeven calculation in units and revenue
    2. Analysis of what this means for the business
    3. Recommendations for reducing the breakeven point
    4. Estimated timeline to reach breakeven based on market conditions
    5. Key metrics to track for financial sustainability
    
    Be specific and practical in your analysis.
    """
    
    response = model.generate_content(prompt)
    return response.text

def create_budget_plan(startup_details, monthly_capital):
    model = get_gemini_model()
    prompt = f"""
    Create a detailed budget plan for a startup with the following details:
    
    Industry: {startup_details['industry']}
    Product/Service: {startup_details['product']}
    Current Monthly Capital: ${monthly_capital}
    Fixed Costs: {startup_details['fixed_costs']}
    
    Please provide:
    1. A breakdown of recommended budget allocation (marketing, development, operations, etc.)
    2. Cost-cutting strategies specific to this type of business
    3. Essential vs. non-essential expenses for a startup in this phase
    4. Cash flow projection for the first 6 months
    5. Financial red flags to watch out for
    
    The goal is to maximize runway and achieve breakeven as quickly as possible.
    """
    
    response = model.generate_content(prompt)
    return response.text

def analyze_focus_areas(startup_details):
    model = get_gemini_model()
    prompt = f"""
    For a new startup in the {startup_details['industry']} industry offering {startup_details['product']},
    identify the key areas that should be prioritized for best returns on investment.
    
    Please provide:
    1. Top 5 areas the founder should focus on, ranked by ROI potential
    2. Specific metrics to track for each focus area
    3. Estimated resource allocation (time and money) for each area
    4. Low-cost strategies for maximizing impact in each area
    5. Market trends affecting these focus areas in 2025
    
    The startup has limited capital and needs to prioritize efforts for survival and growth.
    """
    
    response = model.generate_content(prompt)
    return response.text

def evaluate_capital_options(startup_details, available_capital):
    model = get_gemini_model()
    prompt = f"""
    Evaluate the best options for utilizing ${available_capital} in capital for a startup with these details:
    
    Industry: {startup_details['industry']}
    Product/Service: {startup_details['product']}
    Current Stage: {startup_details['stage']}
    
    Please provide:
    1. 5 different options for deploying this capital with pros/cons for each
    2. Expected ROI timeline for each option
    3. Risk assessment for each option (low/medium/high)
    4. How each option affects the runway and burn rate
    5. Recommendation on the optimal allocation strategy given current market conditions
    
    Consider both short-term survival and long-term growth potential in your analysis.
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    configure_genai()
    
    print("\nStartup Financial Advisor")
    print("------------------------")
    
    # Collect basic startup information
    startup_details = {}
    startup_details['industry'] = input("What industry is your startup in? ")
    startup_details['product'] = input("What is your main product/service? ")
    startup_details['stage'] = input("What stage is your startup in? (idea, MVP, pre-revenue, revenue) ")
    
    while True:
        print("\nFinancial Management Options:")
        print("1. Calculate Breakeven Point")
        print("2. Create Budget Plan")
        print("3. Analyze Key Focus Areas")
        print("4. Evaluate Capital Utilization Options")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ")
        
        if choice == "1":
            print("\n--- Breakeven Calculation ---")
            startup_details['fixed_costs'] = input("What are your monthly fixed costs? (e.g., rent, salaries) ")
            startup_details['variable_costs'] = input("What are your variable costs per unit/customer? ")
            startup_details['pricing'] = input("What is your product/service pricing? ")
            
            print("\nCalculating breakeven point...")
            breakeven_analysis = calculate_breakeven(startup_details)
            print("\n" + breakeven_analysis)
            
            save = input("\nSave this analysis to file? (y/n): ")
            if save.lower() == 'y':
                with open('breakeven_analysis.txt', 'w') as f:
                    f.write(breakeven_analysis)
                print("Analysis saved to breakeven_analysis.txt")
            
        elif choice == "2":
            print("\n--- Budget Planning ---")
            monthly_capital = input("What is your current monthly capital? ")
            
            try:
                float(monthly_capital)
            except ValueError:
                print("Error: Please enter a valid number for monthly capital")
                continue
            
            print("\nCreating budget plan...")
            budget_plan = create_budget_plan(startup_details, monthly_capital)
            print("\n" + budget_plan)
            
            save = input("\nSave this budget plan to file? (y/n): ")
            if save.lower() == 'y':
                with open('budget_plan.txt', 'w') as f:
                    f.write(budget_plan)
                print("Budget plan saved to budget_plan.txt")
            
        elif choice == "3":
            print("\n--- Key Focus Areas Analysis ---")
            print("\nAnalyzing optimal focus areas...")
            focus_areas = analyze_focus_areas(startup_details)
            print("\n" + focus_areas)
            
            save = input("\nSave this focus area analysis to file? (y/n): ")
            if save.lower() == 'y':
                with open('focus_areas.txt', 'w') as f:
                    f.write(focus_areas)
                print("Analysis saved to focus_areas.txt")
            
        elif choice == "4":
            print("\n--- Capital Utilization Options ---")
            available_capital = input("How much capital do you have available to deploy? ")
            
            try:
                float(available_capital)
            except ValueError:
                print("Error: Please enter a valid number for available capital")
                continue
            
            print("\nEvaluating capital options...")
            capital_options = evaluate_capital_options(startup_details, available_capital)
            print("\n" + capital_options)
            
            save = input("\nSave this capital options analysis to file? (y/n): ")
            if save.lower() == 'y':
                with open('capital_options.txt', 'w') as f:
                    f.write(capital_options)
                print("Analysis saved to capital_options.txt")
            
        elif choice == "5":
            print("Exiting. Good luck with your startup!")
            break
            
        else:
            print("Invalid choice. Please select 1-5.")

main()