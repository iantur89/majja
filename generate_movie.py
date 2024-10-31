import json
import os
import numpy as np
from PIL import Image, ImageDraw
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip, vfx

# Debug mode: Set to True to increase video speed by 20x for quick review
DEBUG = True

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (234, 4, 4)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
EXERCISES_DIR = "exercises"
LOGO_PATH = "logo.webp"  # Update to your logo path

# Desired screen size (larger than the largest clip)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Helper function to create a countdown screen with logo
def create_countdown_screen(duration, text, color):
    img = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), color)
    draw = ImageDraw.Draw(img)
    text_width, text_height = draw.textsize(text)
    draw.text(((SCREEN_WIDTH - text_width) // 2, (SCREEN_HEIGHT - text_height) // 2), text, fill=WHITE)
    img.save("temp_countdown.png")  # Save the image as a temporary file

    countdown_clip = ImageClip("temp_countdown.png", duration=duration)
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((150, 150))  # Resize logo to fit in the corners
    logo_array = np.array(logo)

    logo_clip = ImageClip(logo_array).set_position(("right", "top")).set_duration(duration)
    return CompositeVideoClip([countdown_clip, logo_clip])

# Create welcome screen
welcome_text = f"{config['gym_name']} \n {config['date']} \n {config['workout_name']}"
welcome_clip = create_countdown_screen(15, welcome_text, BLACK)

# Load and center exercise clips in order
exercise_files = [
    "(1) Hip Escape.mp4",
    "(2) Slamball Over the Shoulder.mp4",
    "(3) Russian Kettlebell Swing.mp4",
    "(4) Sit Through.mp4",
    "(5) Med Ball Oblique Slams.mp4",
    "(6) Burpee Sprawl.mp4",
    "(7) Med Ball Russian Twist.mp4",
    "(8) Bear Crawl mp4.mp4"
]
exercise_clips = []
exercise_duration = 90 / len(exercise_files)

for file in exercise_files:
    file_path = os.path.join(EXERCISES_DIR, file)
    clip = VideoFileClip(file_path)
    if clip.duration < exercise_duration:
        # Loop the clip until it reaches the required duration
        loops = int(exercise_duration // clip.duration) + 1
        clip = concatenate_videoclips([clip] * loops).subclip(0, exercise_duration)
    else:
        clip = clip.subclip(0, exercise_duration)
    
    # Center the clip on a larger screen without resizing
    centered_clip = CompositeVideoClip([clip.set_position("center")], size=(SCREEN_WIDTH, SCREEN_HEIGHT))
    exercise_clips.append(centered_clip)

demo_clip = concatenate_videoclips(exercise_clips).set_duration(90)

# Create warmup screen
warmup_clip = create_countdown_screen(120, "Warmup", BLACK)

# Create get to your stations screen
stations_clip = create_countdown_screen(20, "Get to your stations", BLACK)

# Create workout sequence
workout_clips = []
work_intervals = [
    (75, 35), (75, 35), (75, 35), (75, 35),
    (75, 35), (75, 35), (75, 35), (75, 35),
    (60, 0), (60, 30), (60, 30), (60, 30),
    (60, 30), (60, 30), (60, 30), (60, 30),
    (60, 0), (45, 25), (45, 25), (45, 25),
    (45, 25), (45, 25), (45, 25), (45, 25),
    (60, 0)
]

for work, rest in work_intervals:
    work_clip = create_countdown_screen(work, "Work", GREEN)
    workout_clips.append(work_clip)
    if rest > 0:
        rest_clip = create_countdown_screen(rest, "Rest", RED)
        workout_clips.append(rest_clip)

workout_sequence = concatenate_videoclips(workout_clips)

# Create water break screen
water_break_clip = create_countdown_screen(60, "Water Break", BLUE)

# Cooldown screen
cooldown_clip = create_countdown_screen(60, "Great Job!", BLACK)

# Final video
final_video = concatenate_videoclips([
    welcome_clip, demo_clip, warmup_clip, stations_clip,
    workout_sequence, water_break_clip, cooldown_clip
])

# Apply debug speed-up if DEBUG is True
if DEBUG:
    final_video = final_video.fx(vfx.speedx, 20)

# Export video
final_video.write_videofile("workout_video.mp4", fps=24)
