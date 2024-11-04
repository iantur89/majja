import json
import os
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip, TextClip, vfx, AudioFileClip

# Debug mode: Set to True to increase video speed by 40x for quick review
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
ORANGE = (255, 165, 0)
EXERCISES_DIR = "exercises"
LOGO_PATH = "logo.webp"  # Update to your logo path
BEEP_PATH = "beep.mp3"  # Path to your single beep sound file

# Desired screen size (larger than the largest clip)
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920

# Helper function to create a countdown screen with logo, visible timer, and beeps
def create_countdown_screen(duration, text, color):
    # Calculate font sizes
    main_font_size = int(SCREEN_HEIGHT * 0.33)  # Countdown font size: 66% of the screen height
    top_font_size = int(SCREEN_HEIGHT * 0.175)  # Top text font size: 12.5% (1/8) of the screen height

    # Create the background screen
    img = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), color)
    img.save("temp_countdown.png")  # Save the image as a temporary file

    # Create ImageClip for the background
    background_clip = ImageClip("temp_countdown.png", duration=duration)

    # Create a TextClip for each second of the countdown
    countdown_clips = []
    beep_audio = AudioFileClip(BEEP_PATH)
    beeps = []

    for t in range(int(duration)):
        countdown_text = f"{int(duration - t)}s"
        countdown_text_clip = TextClip(
            txt=countdown_text,
            fontsize=main_font_size,
            color="white",
            align="center"  # Center align the text
        ).set_duration(1).set_position(("center", "center"))  # Center the countdown text

        countdown_clips.append(countdown_text_clip)

        # Play the beep audio at 3 seconds remaining
        if duration - t == 3:
            beeps.append(beep_audio.set_start(t))

    # Concatenate the countdown clips into one
    countdown_text_clip = concatenate_videoclips(countdown_clips)

    # Create a TextClip for the top text
    top_text_clip = TextClip(
        txt=text,
        fontsize=top_font_size,
        color="white",
        align="center"  # Center align the top text
    ).set_position(("right", "bottom")).set_duration(duration)

    # Load the logo and create an ImageClip
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((500, 500))  # Resize logo to fit in the corners
    logo_array = np.array(logo)
    logo_clip = ImageClip(logo_array).set_position(("center", "center")).set_duration(duration)

    # Combine everything into one clip, including the beeps
    final_clip = CompositeVideoClip([background_clip, countdown_text_clip, top_text_clip, logo_clip])
    if beeps:
        final_clip = final_clip.set_audio(beeps[0])  # Use the single beep audio

    return final_clip

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
    clip = VideoFileClip(file_path).without_audio()  # Remove the audio from the clip
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
warmup_clip = create_countdown_screen(120, "Warm-\nup", BLACK)

# Create get to your stations screen
stations_clip = create_countdown_screen(20, "Get\nready!", ORANGE)

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
    else:
        # If rest time is 0, it's a water break
        water_break_clip = create_countdown_screen(60, "Water", BLUE)
        workout_clips.append(water_break_clip)

workout_sequence = concatenate_videoclips(workout_clips)

# Cooldown screen
cooldown_clip = create_countdown_screen(60, "Great Job!", BLACK)

# Final video
final_video = concatenate_videoclips([
    welcome_clip, demo_clip, warmup_clip, stations_clip,
    workout_sequence, cooldown_clip
])

# Apply debug speed-up if DEBUG is True
if DEBUG:
    final_video = final_video.fx(vfx.speedx, 100)

# Export video
final_video.write_videofile("workout_video.mp4", fps=24)
