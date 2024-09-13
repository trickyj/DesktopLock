import os
import tkinter as tk
from tkinter import simpledialog
import time
import threading


#stays always on top
os.system("wmctrl -r :ACTIVE: -b add,above")

# Disable Alt+F4 or window close button
def disable_close():
    pass

def check_quota():
    """Check if both buttons are disabled, and display a message if they are."""
    if btn_1_hour['state'] == 'disabled' and btn_30_minutes['state'] == 'disabled':
        quota_label.config(text="Note: That is enough for today. You played for 1 hour in total. Come back tomorrow.")
        quota_label.pack(pady=20)

def start_timer(duration):
    def countdown():
        remaining_time = duration
        # Show the timer window and update the time left
        while remaining_time > 0:
            minutes, seconds = divmod(remaining_time, 60)
            time_left_label.config(text=f"{minutes:02d}:{seconds:02d} remaining")
            time_left_label.update()
            time.sleep(1)
            remaining_time -= 1
        
        # When the timer is done, show the fullscreen window again
        timer_window.withdraw()  # Hide the timer window
        root.deiconify()  # Show the fullscreen window
        root.attributes('-fullscreen', True)  # Full screen again

    # Hide the fullscreen window and allow desktop access
    root.withdraw()
    timer_window.deiconify()  # Show the small timer window

    # Start the countdown in a new thread to avoid freezing the UI
    timer_thread = threading.Thread(target=countdown)
    timer_thread.start()

def start_timer_1_hour():
    btn_1_hour.config(state='disabled')  # Disable button after clicking
    check_quota()  # Check if both buttons are disabled
    start_timer(30* 60)  # 1 hour in seconds

def start_timer_30_minutes():
    btn_30_minutes.config(state='disabled')  # Disable button after clicking
    check_quota()  # Check if both buttons are disabled
    start_timer(30 * 60)  # 30 minutes in seconds

def start_custom_timer():
    # Ask user for custom time in minutes
    custom_time = simpledialog.askinteger("Custom Timer", "Enter time in minutes:")
    if custom_time:
        start_timer(custom_time * 60)  # Convert minutes to seconds

# Initialize the root (fullscreen) window
root = tk.Tk()
root.title("Full Screen Timer App")
root.attributes('-fullscreen', True)  # Make it full screen

# Override the close event (disable Alt+F4)
root.protocol("WM_DELETE_WINDOW", disable_close)  # Disable close button and Alt+F4

# Create UI elements for fullscreen window
label = tk.Label(root, text="Welcome Ayansh!! Choose your Game Play time:", font=("Helvetica", 24), fg="red")
label.pack(pady=20)

btn_1_hour = tk.Button(root, text="Play for 30 Minutes", command=start_timer_1_hour, font=("Helvetica", 20), fg="blue")
btn_1_hour.pack(pady=10)

btn_30_minutes = tk.Button(root, text="Play for additional 30 Minutes", command=start_timer_30_minutes, font=("Helvetica", 20), fg="green")
btn_30_minutes.pack(pady=10)

# btn_custom = tk.Button(root, text="Custom Timer", command=start_custom_timer, font=("Helvetica", 20))
# btn_custom.pack(pady=10)

# Label to display quota message
quota_label = tk.Label(root, text="", font=("Helvetica", 24), fg="red")

# Create the small timer window
timer_window = tk.Toplevel(root)
timer_window.title("Game play Time Remaining")
timer_window.geometry("200x60")  # Set the size of the timer window
timer_window.withdraw()  # Initially hide the timer window

# Disable window decorations (no close, minimize, or maximize buttons)
timer_window.overrideredirect(True)

# Override Alt+F4 and closing event for the timer window
timer_window.protocol("WM_DELETE_WINDOW", disable_close)

# Create the label in the small timer window
time_left_label = tk.Label(timer_window, text="", font=("Helvetica", 18), fg="red")
time_left_label.pack(pady=10)

# Run the application
root.mainloop()
