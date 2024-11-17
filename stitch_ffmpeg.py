import subprocess

# Paths to the input videos
video1_path = "video1.mp4"
video24_path = "video24.mp4"
video3_path = "video3.mp4"
output_path = "final_video1.mp4"

# Create a text file listing the videos for ffmpeg
with open("concat_list.txt", "w") as f:
    f.write(f"file '{video1_path}'\n")
    f.write(f"file '{video24_path}'\n")
    f.write(f"file '{video3_path}'\n")

# Call ffmpeg to concatenate the videos
ffmpeg_command = [
    "ffmpeg", "-f", "concat", "-safe", "0", "-i", "concat_list.txt",
    "-c", "copy", output_path
]

# Run the command and capture any output or errors
subprocess.run(ffmpeg_command, check=True)

print(f"Final video saved as {output_path}")
