import os
from dotenv import load_dotenv
import google.generativeai as genai

def get_gemini_model():
    load_dotenv("auth.env")  # Load environment variables from auth.env file
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.  Please set it in your auth.env file or environment.")
    genai.configure(api_key=api_key)
    return genai

def find_potential_clients(startup_details):
    try:
        model = get_gemini_model()
        gemini = model.GenerativeModel('gemini-pro')  # Specify the model to use
        prompt = f"""
        Based on the following startup information, identify potential clients and market entry strategies:

        Industry: {startup_details['industry']}
        Product/Service: {startup_details['product']}
        Target Market: {startup_details['target_market']}
        Value Proposition: {startup_details['value_proposition']}

        Please provide:
        1. Detailed ideal client profiles with demographics and psychographics
        2. List of potential client segments ranked by conversion probability
        3. Specific strategies to reach and convert each client segment
        4. Estimated client acquisition costs for each segment
        5. Potential market size and reachable clients in first year
        6. Most effective marketing channels for each segment
        7. Common client pain points and how to address them

        Be specific and provide actionable insights.
        """

        response = gemini.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating client analysis: {e}"


def analyze_competitors(startup_details):
    try:
        model = get_gemini_model()
        gemini = model.GenerativeModel('gemini-pro')  # Specify the model to use
        prompt = f"""
        Provide a detailed competitor analysis for a startup in the following space:

        Industry: {startup_details['industry']}
        Product/Service: {startup_details['product']}
        Target Market: {startup_details['target_market']}
        Key Features: {startup_details['key_features']}

        Please provide:
        1. Top 5 direct competitors and their market positions
        2. Detailed SWOT analysis for each major competitor
        3. Competitor pricing strategies and business models
        4. Market share distribution among key players
        5. Competitive advantages and disadvantages
        6. Gaps in competitor offerings that can be exploited
        7. Potential defensive strategies from competitors
        8. Recommended positioning strategy based on competition

        Focus on actionable insights and specific strategies.
        """

        response = gemini.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating competitor analysis: {e}"


def analyze_market_entry(startup_details):
    try:
        model = get_gemini_model()
        gemini = model.GenerativeModel('gemini-pro')  # Specify the model to use
        prompt = f"""
        Analyze market entry strategies for:

        Industry: {startup_details['industry']}
        Product/Service: {startup_details['product']}
        Target Market: {startup_details['target_market']}
        Available Resources: {startup_details['resources']}

        Please provide:
        1. Most viable market entry strategies ranked by effectiveness
        2. Resource requirements for each strategy
        3. Timeline for market penetration
        4. Risk assessment for each strategy
        5. Key success metrics to track
        6. Potential barriers to entry and how to overcome them

        Consider both immediate impact and long-term sustainability.
        """

        response = gemini.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating market entry analysis: {e}"


def main():
    print("\nMarket Analysis and Client Discovery Tool")
    print("----------------------------------------")

    # Collect startup information
    startup_details = {}
    startup_details['industry'] = input("What industry is your startup in? ")
    startup_details['product'] = input("What is your main product/service? ")
    startup_details['target_market'] = input("Who is your target market? ")
    startup_details['value_proposition'] = input("What is your unique value proposition? ")
    startup_details['key_features'] = input("What are your key product/service features? ")
    startup_details['resources'] = input("What resources do you have available for market entry? ")

    while True:
        print("\nMarket Analysis Options:")
        print("1. Find Potential Clients")
        print("2. Analyze Competitors")
        print("3. Analyze Market Entry Strategies")
        print("4. Exit")

        choice = input("\nSelect an option (1-4): ")

        if choice == "1":
            print("\n--- Potential Client Analysis ---")
            print("\nAnalyzing potential clients...")
            client_analysis = find_potential_clients(startup_details)
            print("\n" + client_analysis)

            save = input("\nSave this client analysis to file? (y/n): ")
            if save.lower() == 'y':
                with open('client_analysis.txt', 'w', encoding='utf-8') as f:
                    f.write(client_analysis)
                print("Analysis saved to client_analysis.txt")

        elif choice == "2":
            print("\n--- Competitor Analysis ---")
            print("\nAnalyzing competitors...")
            competitor_analysis = analyze_competitors(startup_details)
            print("\n" + competitor_analysis)

            save = input("\nSave this competitor analysis to file? (y/n): ")
            if save.lower() == 'y':
                with open('competitor_analysis.txt', 'w', encoding='utf-8') as f:
                    f.write(competitor_analysis)
                print("Analysis saved to competitor_analysis.txt")

        elif choice == "3":
            print("\n--- Market Entry Strategy ---")
            print("\nAnalyzing market entry strategies...")
            entry_analysis = analyze_market_entry(startup_details)
            print("\n" + entry_analysis)

            save = input("\nSave this market entry analysis to file? (y/n): ")
            if save.lower() == 'y':
                with open('market_entry_analysis.txt', 'w', encoding='utf-8') as f:
                    f.write(entry_analysis)
                print("Analysis saved to market_entry_analysis.txt")

        elif choice == "4":
            print("Exiting. Good luck with your market analysis!")
            break

        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()