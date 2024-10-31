import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

# Directory containing exercise clips
EXERCISES_DIR = "exercises"

# List of exercise video files in order
exercise_files = [
    "(1) Hip Escape.mp4",
    "(2) Slamball Over the Shoulder.mp4",
    "(3) Russian Kettlebell Swing.mp4",
    "(4) Sit Through.mp4",
    "(5) Med Ball Oblique Slams.mp4",
    "(6) Burpee Sprawl.mp4",
    "(8) Bear Crawl mp4.mp4"
]

# Desired screen size (larger than the largest clip)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Load and center exercise clips
exercise_clips = []
for file in exercise_files:
    file_path = os.path.join(EXERCISES_DIR, file)
    if os.path.exists(file_path):
        clip = VideoFileClip(file_path)
        # Center the clip on a larger screen
        centered_clip = CompositeVideoClip([clip.set_position("center")], size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        exercise_clips.append(centered_clip)
    else:
        print(f"File not found: {file_path}")

# Concatenate the clips together
final_video = concatenate_videoclips(exercise_clips)

# Export the final merged video
final_video.write_videofile("merged_exercise_clips.mp4", fps=24)
