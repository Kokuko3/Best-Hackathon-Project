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

# Mapping: Mood -> (Emoji Image Path, Sound File)
moods = {
    "Happy": (os.path.join(BASE_DIR, "happy-cat-face.png"), os.path.join(BASE_DIR, "cats-meow-81221.mp3")),
    "Hungry": (os.path.join(BASE_DIR, "hungry.png"), os.path.join(BASE_DIR, "angry-cat-41822.mp3")),
    "Sad": (os.path.join(BASE_DIR, "sad-cat.png"), os.path.join(BASE_DIR, "200412-cat-stray-sad-meows-ms-6am-60384.mp3")),
}

# Function to get the correct image path (uses default if missing)
def get_mood_image(mood):
    img_path = moods[mood][0]
    if not os.path.exists(img_path):
        print(f"⚠️ Warning: Image missing for {mood}, using default image.")
        return DEFAULT_IMAGE_PATH  # Return default image instead
    return img_path

# Randomize the starting mood
current_mood = random.choice(list(moods.keys()))
is_paused = False  # Track whether the audio is paused

# Function to check if audio is still playing and re-enable the button when done
def check_audio_status():
    if not pygame.mixer.music.get_busy():  # If audio is not playing
        play_button.config(state="normal")  # Re-enable button
    else:
        root.after(500, check_audio_status)  # Check again after 500ms

# Function to toggle play/pause
def play_pause_sound():
    global is_paused

    if pygame.mixer.music.get_busy():  # If sound is playing
        if is_paused:  # Resume if paused
            pygame.mixer.music.unpause()
            is_paused = False
        else:  # Pause if playing
            pygame.mixer.music.pause()
            is_paused = True
    else:  # If sound is not playing, start playback
        sound_file = moods[current_mood][1]  # Get sound file for the current mood
        if os.path.exists(sound_file):
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            root.after(500, check_audio_status)  # Monitor audio status
            is_paused = False
        else:
            print(f"Error: File not found - {sound_file}")

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

# Load mood image from the GUI folder or use default if missing
mood_path = get_mood_image(current_mood)
mood_image = Image.open(mood_path)  # Load image
mood_image = mood_image.resize((100, 100), Image.ANTIALIAS)  # Resize
mood_image = ImageTk.PhotoImage(mood_image)

mood_label = tk.Label(main_frame, image=mood_image, bg="#403A3A")
mood_label.pack(pady=20)

# Create a Label to display text description of mood
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

# Add an Image Button to play or pause sound
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

# Load and resize PAWS icon for footer
if os.path.exists(PAWS_ICON):
    paws_footer = Image.open(PAWS_ICON)
    paws_footer = paws_footer.resize((20, 20), Image.ANTIALIAS)  # Resize smaller
    paws_footer = ImageTk.PhotoImage(paws_footer)

    paws_footer_label = tk.Label(footer_content, image=paws_footer, bg=header_color)
    paws_footer_label.pack(side="left", padx=5)  # Moves PAWS icon to left of text
else:
    print("⚠️ Warning: PAWS icon not found for footer.")

# Add centered footer text next to icon
footer_label = tk.Label(footer_content, text="Mood Detection in Progress...", font=("Arial", 10), bg=header_color, fg="white")
footer_label.pack(side="left")

# Run the application
root.mainloop()
