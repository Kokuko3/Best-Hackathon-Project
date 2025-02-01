import tkinter as tk
import random
import pygame
import os

# Initialize pygame for audio playback
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Get the directory where PetAudio.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Mapping: Mood -> (Emoji, Sound File)
moods = {
    "Happy": ("😺", os.path.join(BASE_DIR, "cats-meow-81221.mp3")),
    "Sad": ("😿", os.path.join(BASE_DIR, "200412-cat-stray-sad-meows-ms-6am-60384.mp3")),
    "Angry": ("😾", os.path.join(BASE_DIR, "angry-cat-41822.mp3")),
}

# Default mood at start
current_mood = "Happy"  # Default starting mood

# Function to check if audio is still playing and re-enable the button when done
def check_audio_status():
    if not pygame.mixer.music.get_busy():  # If audio is not playing
        play_button.config(state="normal", bg=button_color, fg="white")  # Re-enable button
    else:
        root.after(500, check_audio_status)  # Check again after 500ms

# Function to play sound
def play_sound():
    sound_file = moods[current_mood][1]  # Get sound file for the current mood

    if os.path.exists(sound_file):  # Check if the file exists before playing
        play_button.config(state="disabled", bg="white", fg="black")  # Disable and turn white
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
        root.after(500, check_audio_status)  # Start checking if audio is done
    else:
        print(f"Error: File not found - {sound_file}")

# Function to change mood randomly
def change_mood():
    global current_mood
    current_mood = random.choice(list(moods.keys()))  # Pick a random mood
    emoji, sound_file = moods[current_mood]  # Get emoji and sound
    
    mood_label.config(text=emoji)  # Update emoji
    mood_text_label.config(text=f"Mood: {current_mood}")  # Update text

# Create main window
root = tk.Tk()
root.title("🐾 PAWS - Mood Detector")
root.geometry("400x400")
root.configure(bg="#403A3A")  # Warm Dark Gray Background

# Colors
header_color = "#957B63"  # Soft Taupe Brown
button_color = "#957B63"  # Same as header for consistency
text_color = "#FFFFFF"  # White for better contrast

# Create top menu frame for hamburger button
menu_frame = tk.Frame(root, bg=header_color)
menu_frame.pack(side="top", fill="x", anchor="w")

# Create an empty dropdown menu
menu_bar = tk.Menu(root, tearoff=0)

def open_menu(event):
    menu_bar.post(event.x_root, event.y_root)

# Create the hamburger button and place it in the top-left corner
hamburger_btn = tk.Button(menu_frame, text="☰", font=("Arial", 14), command=lambda: menu_bar.post(10, 50), bg=header_color, fg="white", relief="flat")
hamburger_btn.pack(side="left", padx=5, pady=5)

# Create header
header_label = tk.Label(menu_frame, text="🐾 PAWS - Mood Detector", font=("Arial", 16, "bold"), bg=header_color, fg="white")
header_label.pack(pady=10)

# Create main content frame
main_frame = tk.Frame(root, bg="#403A3A")
main_frame.pack(fill="both", expand=True)

# Create a Label to display mood emoji
mood_label = tk.Label(main_frame, text="😺", font=("Arial", 50), bg="#403A3A", fg=text_color)
mood_label.pack(pady=20)

# Create a Label to display text description of mood
mood_text_label = tk.Label(main_frame, text="Mood: Happy", font=("Arial", 14), bg="#403A3A", fg=text_color)
mood_text_label.pack(pady=5)

# Add a Button to detect mood
detect_button = tk.Button(main_frame, text="Detect Mood", command=change_mood, bg=button_color, fg="white", font=("Arial", 12), relief="flat")
detect_button.pack(pady=10)

# Add a Button to play sound
play_button = tk.Button(main_frame, text="🔊 Play Sound", command=play_sound, bg=button_color, fg="white", font=("Arial", 12), relief="flat")
play_button.pack(pady=10)

# Create footer
footer = tk.Frame(root, bg=header_color, height=30)
footer.pack(fill="x")

footer_label = tk.Label(footer, text="🐾 Mood Detection in Progress...", font=("Arial", 10), bg=header_color, fg="white")
footer_label.pack(pady=5)

# Run the application
root.mainloop()
