import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

# Paths to the input videos
video1_path = "video1.mp4"
video2_path = "video2.mp4"
video3_path = "video3.mp4"
video4_path = "video4.mp4"
output_merged_path = "video24.mp4"
final_output_path = "final_video.mp4"

# Function to merge video2 and video4 side-by-side
def merge_side_by_side(video2_path, video4_path, output_path):
    # Load video clips
    video2 = VideoFileClip(video2_path)
    video4 = VideoFileClip(video4_path)

    # Ensure both videos have the same height
    video_height = min(video2.size[1], video4.size[1])
    video2 = video2.resize(height=video_height)
    video4 = video4.resize(height=video_height)

    # Set the width of each video
    merged_width = video2.size[0] + video4.size[0]

    # Create a composite video clip side-by-side
    merged_clip = CompositeVideoClip([video2.set_position(("left", "center")), 
                                      video4.set_position((video2.size[0], "center"))],
                                     size=(merged_width, video_height))

    # Write the merged video to a file
    merged_clip.write_videofile(output_path, fps=24)

# Function to concatenate video1, video24, and video3
def concatenate_videos(video1_path, video24_path, video3_path, output_path):
    # Load video clips
    video1 = VideoFileClip(video1_path)
    video24 = VideoFileClip(video24_path)
    video3 = VideoFileClip(video3_path)

    # Concatenate the videos
    final_clip = concatenate_videoclips([video1, video24, video3])

    # Write the final concatenated video to a file
    final_clip.write_videofile(output_path, fps=24)

# Main script
if __name__ == "__main__":
    # Merge video2 and video4 side-by-side
    merge_side_by_side(video2_path, video4_path, output_merged_path)

    # Concatenate video1, video24, and video3
    concatenate_videos(video1_path, output_merged_path, video3_path, final_output_path)

    print(f"Final video saved as {final_output_path}")
