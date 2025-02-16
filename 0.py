import os
import tkinter as tk
from tkinter import messagebox

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
        messagebox.showinfo("Running Script", f"Running {script_name}...")
        os.system(f'python "{script_name}"')
    else:
        messagebox.showerror("Error", f"Script {script_name} not found.")

def on_button_click(choice):
    if choice == "0":
        root.destroy()
    else:
        run_script(choice)

root = tk.Tk()
root.title("Script Runner")
root.geometry("400x500")
root.configure(bg="#dbe7f0")  # Muted light blue background

label = tk.Label(root, text="Select a script to run:", font=("Arial", 14, "bold"), bg="#dbe7f0", fg="#333")
label.pack(pady=10)

buttons = [
    ("Finding the right people", "1", "#b56576"),  # Muted red
    ("Market Insights, growth domains", "2", "#6d8b74"),  # Muted green
    ("AI generated surveys and finding investors", "3", "#4c6a92"),  # Muted blue
    ("Financials management and evaluating options", "4", "#a17a7d"),  # Muted pink
    ("Marketing (Social Media presence growth)", "5", "#6b5b95"),  # Muted purple
    ("Legality Checks for Business Decisions", "6", "#89a1b0"),  # Muted teal
    ("Calendar Management", "7", "#d4a373"),  # Muted orange
    ("Entry strategy and stakeholder analysis", "8", "#a3b18a"),  # Muted olive green
    ("Exit", "0", "#b0a8b9")  # Muted gray
]

for text, value, color in buttons:
    btn = tk.Button(root, text=text, font=("Arial", 12), bg=color, fg="white", activebackground="#555", activeforeground="white", command=lambda v=value: on_button_click(v))
    btn.pack(fill='x', padx=20, pady=5)

root.mainloop()
