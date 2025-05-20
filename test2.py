import customtkinter as ctk
import datetime

def get_percentage_of_day():
    now = datetime.datetime.now()
    seconds_passed = now.hour * 3600 + now.minute * 60 + now.second
    total_seconds_in_day = 24 * 3600
    # print(now.day())
    return (seconds_passed / total_seconds_in_day) * 100

def update_progress():
    percentage = get_percentage_of_day()
    # progress_var.set(percentage)
    progress.set(get_percentage_of_day() / 100) 
    progress_label.configure(text=f"{percentage:.2f}% of the day completed")
    root.after(60000, update_progress)  # Update every 60 seconds

# Set appearance mode and theme (optional)
# ctk.set_appearance_mode("System")  # Options: "Light", "Dark", "System"
# ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

# Create GUI
root = ctk.CTk()
root.title("24-Hour Progress Bar")
root.geometry("400x120")

# Progress variable
progress_var = ctk.DoubleVar()

# Progress bar
progress = ctk.CTkProgressBar(root, variable=progress_var, orientation="horizontal") # Initial set (0-1 scale)
progress.pack(pady=(20, 10), padx=20, fill="x")

# Progress label
progress_label = ctk.CTkLabel(root, text="")
progress_label.pack()

# Initial update
update_progress()

# Run the app
root.mainloop()


now = datetime.datetime.now()
print(now.date)