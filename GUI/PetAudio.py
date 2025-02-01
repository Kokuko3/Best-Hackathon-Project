import tkinter as tk
import random
import pygame
import os
from PIL import Image, ImageTk  # Required to load images in Tkinter

# Initialize pygame for audio playback
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Get the directory where PetAudio.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This is the GUI folder

# Set paths for images
PAWS_ICON = os.path.join(BASE_DIR, "paws.png")  # Header and footer icon
VOLUME_ICON = os.path.join(BASE_DIR, "volume.png")  # Audio button
DEFAULT_IMAGE_PATH = os.path.join(BASE_DIR, "default.png")  # Default mood image

# Mapping of moods to corresponding image files
MOOD_IMAGES = {
    "Happy": os.path.join(BASE_DIR, "happy-cat-face.png"),
    "Hungry": os.path.join(BASE_DIR, "hungry.png"),
    "Sad": os.path.join(BASE_DIR, "sad-cat.png"),
}

# Default values for mood and audio
current_mood = "Happy"
current_audio = None  # This will be updated with AI-received audio path
is_paused = False  # Track whether the audio is paused

# Function to load a mood image, using a default if missing
def get_mood_image(mood):
    img_path = MOOD_IMAGES.get(mood, DEFAULT_IMAGE_PATH)
    if not os.path.exists(img_path):
        print(f"⚠️ Warning: Image missing for {mood}, using default image.")
        return DEFAULT_IMAGE_PATH  # Use default if image is missing
    return img_path

# Function to check if audio is still playing and re-enable the button when done
def check_audio_status():
    if not pygame.mixer.music.get_busy():  # If no audio is playing
        play_button.config(state="normal")  # Re-enable play button
    else:
        root.after(500, check_audio_status)  # Check again every 500ms

# Function to play or pause the received AI audio
def play_pause_sound():
    global is_paused

    if pygame.mixer.music.get_busy():  # If audio is currently playing
        if is_paused:  # Resume playback if paused
            pygame.mixer.music.unpause()
            is_paused = False
        else:  # Pause playback if playing
            pygame.mixer.music.pause()
            is_paused = True
    elif current_audio:  # If there's a valid audio file, play it
        if os.path.exists(current_audio):
            pygame.mixer.music.load(current_audio)
            pygame.mixer.music.play()
            root.after(500, check_audio_status)  # Monitor audio status
            is_paused = False
        else:
            print(f"Error: File not found - {current_audio}")

# Function to update mood and audio when AI sends data
def update_mood(mood, audio_path):
    global current_mood, current_audio, mood_image

    # Update mood text and image
    current_mood = mood
    current_audio = audio_path

    # Update mood text label
    mood_text_label.config(text=f"Mood: {mood}")

    # Load and update mood image
    new_mood_path = get_mood_image(mood)
    new_mood_image = Image.open(new_mood_path)
    new_mood_image = new_mood_image.resize((100, 100), Image.ANTIALIAS)
    mood_image = ImageTk.PhotoImage(new_mood_image)
    mood_label.config(image=mood_image)

    print(f"🔄 Mood updated to: {mood}, Audio File: {audio_path}")  # Debugging log

# Create main window
root = tk.Tk()
root.title("PAWS - Mood Detector")
root.geometry("400x400")
root.configure(bg="#403A3A")  # Warm Dark Gray Background

# Colors
header_color = "#957B63"  # Soft Taupe Brown
text_color = "#FFFFFF"  # White for better contrast

# Create top menu frame
menu_frame = tk.Frame(root, bg=header_color)
menu_frame.pack(side="top", fill="x", anchor="w")

# Create a frame to hold the logo and title
title_frame = tk.Frame(menu_frame, bg=header_color)
title_frame.pack(pady=5)

# Load and resize PAWS icon for title
if os.path.exists(PAWS_ICON):
    paws_image = Image.open(PAWS_ICON)
    paws_image = paws_image.resize((25, 25), Image.ANTIALIAS)  # Resize smaller
    paws_image = ImageTk.PhotoImage(paws_image)
    
    paws_label = tk.Label(title_frame, image=paws_image, bg=header_color)
    paws_label.pack(side="left", padx=5)  # Adds spacing between icon and text
else:
    print("⚠️ Warning: PAWS icon not found. Skipping image.")

# Add title text next to the icon
title_label = tk.Label(title_frame, text="PAWS - Mood Detector", font=("Arial", 16, "bold"), bg=header_color, fg="white")
title_label.pack(side="left")

# Create main content frame
main_frame = tk.Frame(root, bg="#403A3A")
main_frame.pack(fill="both", expand=True)

# Load initial mood image
mood_path = get_mood_image(current_mood)
mood_image = Image.open(mood_path)
mood_image = mood_image.resize((100, 100), Image.ANTIALIAS)
mood_image = ImageTk.PhotoImage(mood_image)

# Label to display mood image
mood_label = tk.Label(main_frame, image=mood_image, bg="#403A3A")
mood_label.pack(pady=20)

# Label to display mood text
mood_text_label = tk.Label(main_frame, text=f"Mood: {current_mood}", font=("Arial", 14), bg="#403A3A", fg=text_color)
mood_text_label.pack(pady=5)

# Load volume button icon
if os.path.exists(VOLUME_ICON):
    volume_icon = Image.open(VOLUME_ICON)
    volume_icon = volume_icon.resize((40, 40), Image.ANTIALIAS)
    volume_icon = ImageTk.PhotoImage(volume_icon)
else:
    print("⚠️ Warning: Volume icon not found. Using text button instead.")
    volume_icon = None

# Button to play or pause audio
if volume_icon:
    play_button = tk.Button(main_frame, image=volume_icon, command=play_pause_sound, bg="#403A3A", relief="flat")
else:
    play_button = tk.Button(main_frame, text="🔊 Play Sound", command=play_pause_sound, bg="#957B63", fg="white", font=("Arial", 12), relief="flat")

play_button.pack(pady=10)

# Create footer frame
footer = tk.Frame(root, bg=header_color, height=30)
footer.pack(fill="x")

# Center the footer content
footer_content = tk.Frame(footer, bg=header_color)
footer_content.pack(anchor="center")

# Add footer text
footer_label = tk.Label(footer_content, text="Mood Detection in Progress...", font=("Arial", 10), bg=header_color, fg="white")
footer_label.pack(side="left")

# Run the application
root.mainloop()
