import os

def display_menu():
    print("\nSelect a script to run:")
    print("1. Finding the right people")
    print("2. Market Insights, growth domains")
    print("3. AI generated surveys and finding investors")
    print("4. Financials management and progress reports and evaluating options")
    print("5. Marketing (Social Media presence growth)")
    print("6. Legality Checks for Business Decisions")
    print("7. Calendar Management")
    print("8. Analyse stakeholders, competitors and entry strategies")
    print("0. Exit")

def run_script(script_number):
    script_map = {
        "1": "1.py",
        "2": "2.py",
        "3": "3, 6.py",
        "4": "4, 5.py",  
        "5": "7.py",
        "6": "11.py",
        "7": "12.py",
        "8": "9, 10.py"
    }
    
    script_name = script_map.get(script_number)
    
    if script_name and os.path.exists(script_name):
        print(f"Running {script_name}...")
        os.system(f'python "{script_name}"')
    else:
        print(f"Script {script_name} not found.")

def main():
    while True:
        display_menu()
        choice = input("Enter the number of the script to run (or 0 to exit): ")
        
        if choice == "0":
            print("Exiting program.")
            break
        elif choice in map(str, range(1, 9)):
            run_script(choice)
        else:
            print("Invalid choice. Please select a valid script number.")

main()
