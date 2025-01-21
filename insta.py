import json
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import csv
from tkinter import ttk

# GUI Setup
app = tk.Tk()
app.title("Instagram Follower Analyzer")

# Dynamic window sizing
def adjust_window_size():
    app.update_idletasks()
    width = max(700, app.winfo_reqwidth())
    height = max(500, app.winfo_reqheight())
    app.geometry(f"{width}x{height}")
adjust_window_size()

# Global Variables
followers_file = None
following_file = None
output_data = []

# Style configurations
PRIMARY_COLOR = "#0073e6"
HOVER_COLOR = "#005bb5"
SECONDARY_COLOR = "#f2f2f2"
TEXT_COLOR = "#333333"
BUTTON_FONT = ("Helvetica Neue", 14, "bold")
LABEL_FONT = ("Helvetica Neue", 12)
TEXT_FONT = ("Helvetica Neue", 11)

def load_connections_folder():
    """Load the Instagram folder and locate the followers and following files."""
    global followers_file, following_file
    folder_path = filedialog.askdirectory(title="Select the Instagram Folder (Containing 'Connections')")

    if not folder_path:
        messagebox.showwarning("No Folder Selected", "Please select a valid Instagram folder.")
        return

    # Locate the 'connections' folder within the selected folder
    connections_folder_path = os.path.join(folder_path, 'connections')

    # Check if the 'connections' folder exists
    if not os.path.exists(connections_folder_path):
        messagebox.showerror("Missing Folder", "Could not find 'connections' folder in the selected directory.")
        return

    # Locate the 'followers_1.json' and 'following.json' files within the 'connections' folder
    followers_path = os.path.join(connections_folder_path, 'followers_and_following', 'followers_1.json')
    following_path = os.path.join(connections_folder_path, 'followers_and_following', 'following.json')

    if not os.path.exists(followers_path) or not os.path.exists(following_path):
        messagebox.showerror("Missing Files", "Could not find 'followers_1.json' or 'following.json' in the 'connections' folder.")
        return

    try:
        with open(followers_path, 'r') as f:
            followers_file = json.load(f)
        with open(following_path, 'r') as f:
            following_file = json.load(f)
        messagebox.showinfo("Success", "Successfully loaded followers and following data!")
        analyze_button.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load files: {e}")

    adjust_window_size()


def parse_json(json_file, key):
    """Extract usernames from the JSON file."""
    curr_set = set()
    for user in json_file[key]:
        curr_set.add(user['string_list_data'][0]['value'])
    return curr_set

def parse_json2(json_file):
    """Extract usernames from a different JSON file structure."""
    curr_set = set()
    for user in json_file:
        curr_set.add(user['string_list_data'][0]['value'])
    return curr_set

def analyze_followers():
    """Analyze who is not following back."""
    global output_data

    if not followers_file or not following_file:
        messagebox.showerror("Error", "Followers or Following data not loaded.")
        return

    try:
        following_set = parse_json(following_file, 'relationships_following')
        followers_set = parse_json2(followers_file)

        not_following_back = following_set - followers_set

        # Display results
        output_text.delete("1.0", tk.END)
        output_data = list(not_following_back)

        if not output_data:
            output_text.insert(tk.END, "Everyone you follow is following you back!")
        else:
            output_text.insert(tk.END, "Users not following you back:\n")
            for user in output_data:
                output_text.insert(tk.END, f"- {user}\n")

        output_text.insert(tk.END, f"\nTotal: {len(output_data)}")
        export_button.config(state=tk.NORMAL)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to analyze data: {e}")

    adjust_window_size()

def export_to_csv():
    """Export the results to a CSV file."""
    global output_data

    if not output_data:
        messagebox.showwarning("No Data", "No data to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[["CSV files", "*.csv"]])

    if not file_path:
        return

    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Username"])
            for user in output_data:
                writer.writerow([user])
        messagebox.showinfo("Success", f"Data successfully exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export data: {e}")

# GUI Elements
instructions_label = tk.Label(
    app,
    text=( 
        "\U0001F44B Welcome to Instagram Follower Analyzer!\n\n"
        "1. Navigate to https://accountscenter.instagram.com/info_and_permissions/dyi \n"
        "2. Click 'Download or transfer your information'.\n"
        "3. Select 'Some of your information' and then scroll down and select 'Followers and Following'.\n"
        "4. Select 'Download to device'.\n"
        "5. For Date range, select 'All time' and for Format, select 'JSON'. Leave Medium quality.\n"
        "6. Click 'Create files' and wait for files to be prepared for download.\n"
        "7. Unzip the folder you downloaded from instagram."
        "\U0001F4C2 8. Click 'Load Instagram Folder' to select your main Instagram folder you unzipped.\n"
        "\U0001F50D 9. Click 'Analyze' to see who is not following you back.\n"
        "\U0001F4BE 10. Optionally, export the results to a CSV file."
    ),
    justify="left",
    wraplength=550,
    font=LABEL_FONT,
    bg=SECONDARY_COLOR,
    fg=TEXT_COLOR
)
instructions_label.pack(pady=20, padx=20)

load_button = tk.Button(
    app, 
    text="\U0001F4C2 Load Instagram Folder", 
    command=load_connections_folder, 
    font=BUTTON_FONT, 
    bg=PRIMARY_COLOR, 
    fg="white", 
    activebackground=HOVER_COLOR, 
    activeforeground="white",
    relief="flat",
    height=2,
    width=25
)
load_button.pack(pady=15)

analyze_button = tk.Button(
    app, 
    text="Analyze", 
    command=analyze_followers, 
    state=tk.DISABLED, 
    font=BUTTON_FONT, 
    bg=PRIMARY_COLOR, 
    fg="white", 
    activebackground=HOVER_COLOR, 
    activeforeground="white",
    relief="flat",
    height=2,
    width=25
)
analyze_button.pack(pady=10)

export_button = tk.Button(
    app, 
    text="Export to CSV", 
    command=export_to_csv, 
    state=tk.DISABLED, 
    font=BUTTON_FONT, 
    bg=PRIMARY_COLOR, 
    fg="white", 
    activebackground=HOVER_COLOR, 
    activeforeground="white",
    relief="flat",
    height=2,
    width=25
)
export_button.pack(pady=10)

# Output Text Box with Enhanced Visuals
output_frame = tk.Frame(app, bg=SECONDARY_COLOR, relief="flat")
output_frame.pack(pady=20, padx=20, fill="both", expand=True)

output_text = tk.Text(
    output_frame, 
    height=15, 
    width=70, 
    font=TEXT_FONT, 
    wrap="word", 
    bg="#f8f8f8",  # Light grey background for the text box
    fg=TEXT_COLOR, 
    bd=2,  # Border thickness
    relief="solid",
    padx=10,  # Padding inside the text box
    pady=10,  # Padding inside the text box
    highlightthickness=0  # Remove the default highlight border
)
output_text.pack(side="left", fill="both", expand=True)

# Add Scrollbar to the Output Box
scrollbar = tk.Scrollbar(output_frame, orient="vertical", command=output_text.yview)
scrollbar.pack(side="right", fill="y")
output_text.config(yscrollcommand=scrollbar.set)

# Run the Application
app.configure(bg=SECONDARY_COLOR)
app.mainloop()
