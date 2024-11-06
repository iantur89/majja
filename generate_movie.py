import json
import os
import sys
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip, concatenate_videoclips, ImageClip, CompositeVideoClip, CompositeAudioClip, TextClip, vfx, AudioFileClip
from moviepy.audio.AudioClip import AudioClip, concatenate_audioclips

# Debug mode: Set to True to increase video speed by 40x for quick review
DEBUG = False

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

# Desired screen size for landscape and portrait
LANDSCAPE_WIDTH = 1920
LANDSCAPE_HEIGHT = 1080
PORTRAIT_WIDTH = 1080
PORTRAIT_HEIGHT = 1920

work_intervals = [
    (75, 35), (75, 35), (75, 35), (75, 35),
    (75, 35), (75, 35), (75, 35), (75, 35),
    (60, 0), (60, 30), (60, 30), (60, 30),
    (60, 30), (60, 30), (60, 30), (60, 30),
    (60, 0), (45, 25), (45, 25), (45, 25),
    (45, 25), (45, 25), (45, 25), (45, 25),
    (60, 0)
]

# Helper function to create a countdown screen with logo, visible timer, and beeps
def create_countdown_screen(duration, text, color, width, height):
    # Calculate font sizes
    main_font_size = int(height * 0.33)  # Countdown font size
    top_font_size = int(height * 0.175)  # Top text font size

    # Create the background screen
    img = Image.new("RGB", (width, height), color)
    img.save("temp_countdown.png")  # Save the image as a temporary file

    # Create ImageClip for the background
    background_clip = ImageClip("temp_countdown.png", duration=duration)

    # Create a TextClip for each second of the countdown
    silence_duration = duration - 3.5
    silent_clip = AudioClip(lambda t: 0, duration=silence_duration)  # Creates silent audio
    countdown_clips = []
    try:
        beep_audio = AudioFileClip(BEEP_PATH)
    except OSError:
        print("Error loading beep audio file. Check the file path and format.")
        beep_audio = None  # Fallback in case the audio file cannot be loaded

    full_audio = concatenate_audioclips([silent_clip, beep_audio])

    # Add countdown text clips for each second
    for t in range(int(duration)):
        countdown_text = f"{int(duration - t)}s"
        countdown_text_clip = TextClip(
            txt=countdown_text,
            fontsize=main_font_size,
            color="white",
            align="center"
        ).set_duration(1).set_position(("center", "center"))
        countdown_clips.append(countdown_text_clip)

    # Concatenate countdown clips into one
    countdown_text_clip = concatenate_videoclips(countdown_clips)

    # Create a TextClip for the top text
    top_text_clip = TextClip(
        txt=text,
        fontsize=top_font_size,
        color="white",
        align="center"
    ).set_position(("center", "bottom")).set_duration(duration)

    # Load the logo and create an ImageClip
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((300, 300))  # Resize logo to fit in the corners
    logo_array = np.array(logo)
    logo_clip = ImageClip(logo_array).set_position(("center", "center")).set_duration(duration)

    # Combine everything into one clip
    final_clip = CompositeVideoClip([background_clip, countdown_text_clip, top_text_clip, logo_clip], size=(width, height))
    final_clip = final_clip.set_audio(full_audio)

    # Only add beep audio if not in DEBUG mode
    # if beep_audio and not DEBUG:
    #     final_clip = final_clip.set_audio(beep_audio.set_start(duration - 3.5))

    return final_clip

# Function to create the demo clip with exercise videos
def create_demo_clip():
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
        centered_clip = CompositeVideoClip([clip.set_position("center")], size=(LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT))
        exercise_clips.append(centered_clip)

    # Concatenate all exercise clips to form the demo clip
    return concatenate_videoclips(exercise_clips).set_duration(90)

# Function to create and export videos
def create_videos(videos_to_make):
    LANDSCAPE_WIDTH = 1920
    LANDSCAPE_HEIGHT = 1080
    PORTRAIT_WIDTH = 1080
    PORTRAIT_HEIGHT = 1920
    if "video1" in videos_to_make:
        welcome_clip = create_countdown_screen(15, "Welcome!", BLACK, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT)
        demo_clip = create_demo_clip()
        warmup_clip = create_countdown_screen(120, "Warm-\nup", BLACK, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT)
        stations_clip = create_countdown_screen(20, "Get\nready!", ORANGE, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT)
        video1 = concatenate_videoclips([welcome_clip, demo_clip, warmup_clip, stations_clip])
        if DEBUG:
            video1 = video1.fx(vfx.speedx, 40)
        video1.write_videofile("video1.mp4", fps=24)

    if "video2" in videos_to_make:
        workout_clips = []
        for work, rest in work_intervals:
            work_clip = create_countdown_screen(work, "Work", GREEN, PORTRAIT_WIDTH, PORTRAIT_HEIGHT)
            workout_clips.append(work_clip)
            
            if rest > 0:
                rest_clip = create_countdown_screen(rest, "Rest", RED, PORTRAIT_WIDTH, PORTRAIT_HEIGHT)
                workout_clips.append(rest_clip)
            else:
                water_break_clip = create_countdown_screen(60, "Water", BLUE, PORTRAIT_WIDTH, PORTRAIT_HEIGHT)
                workout_clips.append(water_break_clip)
        
        workout_sequence = concatenate_videoclips(workout_clips)
        video2 = workout_sequence
        if DEBUG:
            video2 = video2.fx(vfx.speedx, 40)
        video2.write_videofile("video2.mp4", fps=24)

    if "video3" in videos_to_make:
        cooldown_clip = create_countdown_screen(60, "Great Job!", BLACK, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT)
        video3 = cooldown_clip
        if DEBUG:
            video3 = video3.fx(vfx.speedx, 40)
        video3.write_videofile("video3.mp4", fps=24)

    if "video4" in videos_to_make:
        # Calculate the total duration of the workout sequence
        exercise_duration = sum(work + rest for work, rest in work_intervals)

        # Set up the portrait orientation
        PORTRAIT_WIDTH = 1080
        PORTRAIT_HEIGHT = 1920

        # Grid layout: 4 rows, 2 columns
        rows, cols = 4, 2
        cell_width = PORTRAIT_WIDTH // cols
        cell_height = PORTRAIT_HEIGHT // rows

        exercise_clips = []
        for i, file in enumerate([
            "(1) Hip Escape.mp4",
            "(2) Slamball Over the Shoulder.mp4",
            "(3) Russian Kettlebell Swing.mp4",
            "(4) Sit Through.mp4",
            "(5) Med Ball Oblique Slams.mp4",
            "(6) Burpee Sprawl.mp4",
            "(7) Med Ball Russian Twist.mp4",
            "(8) Bear Crawl mp4.mp4"
        ]):
            file_path = os.path.join(EXERCISES_DIR, file)
            clip = VideoFileClip(file_path).without_audio()

            # Calculate the scaling factor to maintain aspect ratio
            scale_factor = min(cell_width / clip.size[0], cell_height / clip.size[1])
            clip = clip.resize(scale_factor)

            # Loop the clip to match the total exercise duration
            clip = clip.loop(duration=exercise_duration)

            # Create a label for the exercise with the exercise number and name
            label_text = f"{i + 1}"
            label_clip = TextClip(
                txt=label_text,
                fontsize=120,
                color="white",
                bg_color="black"
            ).set_duration(exercise_duration)

            # Position the label at the top of each cell
            x_pos = (i % cols) * cell_width + (cell_width - clip.size[0]) // 2
            y_pos = (i // cols) * cell_height + (cell_height - clip.size[1]) // 2
            label_pos = (x_pos+10, y_pos + 10)  # Adjust to place label above the video

            # Combine the video clip and label into a single composite clip
            combined_clip = CompositeVideoClip([clip.set_position((x_pos, y_pos)), label_clip.set_position(label_pos)], 
                                               size=(PORTRAIT_WIDTH, PORTRAIT_HEIGHT)).set_duration(exercise_duration)
            exercise_clips.append(combined_clip)

            # Save a sample frame from this clip as a PNG for debugging
            sample_frame = combined_clip.get_frame(0).astype('uint8')  # Convert to uint8 for compatibility
            frame_image = Image.fromarray(sample_frame)
            frame_image.save(f"sample_frame_{i + 1}.png")

        # Create the grid of videos
        exercise_grid = CompositeVideoClip(exercise_clips, size=(PORTRAIT_WIDTH, PORTRAIT_HEIGHT)).set_duration(exercise_duration)
        video4 = exercise_grid

        # Save additional frames at specific intervals if debugging
        if DEBUG:
            for t in [0, exercise_duration // 3, 2 * exercise_duration // 3, exercise_duration - 1]:
                debug_frame = exercise_grid.get_frame(t).astype('uint8')  # Convert to uint8 for compatibility
                debug_image = Image.fromarray(debug_frame)
                debug_image.save(f"debug_frame_{t}.png")

            # Speed up for quick review
            video4 = video4.fx(vfx.speedx, 40)

        video4.write_videofile("video4.mp4", fps=24)



# Main function to handle CLI arguments
if __name__ == "__main__":
    videos_to_make = sys.argv[1:]  # Get the list of videos to create from CLI arguments
    if not videos_to_make:
        print("Please specify which videos to make: video1, video2, video3, video4, or all")
    elif "all" in videos_to_make:
        create_videos(["video1", "video2", "video3", "video4"])
    else:
        create_videos(videos_to_make)
