import numpy as np
from PIL import Image
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip

# Constants for screen size
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
LOGO_PATH = "logo.webp"  # Update to your logo path

# Test function to create a countdown screen and export a single frame
def create_countdown_screen(duration, text, color):
    # Calculate font sizes
    main_font_size = int(SCREEN_HEIGHT * 0.125)  # Countdown font size: 12.5% of the screen height
    top_font_size = int(SCREEN_HEIGHT * 0.125)  # Top text font size: 12.5% (1/8) of the screen height

    # Create the background screen
    img = Image.new("RGB", (SCREEN_WIDTH, SCREEN_HEIGHT), color)
    img.save("temp_countdown.png")  # Save the image as a temporary file

    # Create ImageClip for the background
    background_clip = ImageClip("temp_countdown.png", duration=duration)

    # Create a TextClip for the countdown text
    countdown_text_clip = TextClip(
        txt="10s",  # Example countdown text
        fontsize=main_font_size,
        color="white",
        align="center"
    ).set_position(("center", "center")).set_duration(1)  # Center the countdown text

    # Create a TextClip for the top text
    top_text_clip = TextClip(
        txt=text,
        fontsize=top_font_size,
        color="white",
        align="center"
    ).set_position(("center", "top")).set_duration(1)

    # Load the logo and create an ImageClip
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((150, 150))  # Resize logo to fit in the corners
    logo_array = np.array(logo)
    logo_clip = ImageClip(logo_array).set_position(("right", "top")).set_duration(1)

    # Combine everything into one clip
    final_clip = CompositeVideoClip([background_clip, countdown_text_clip, top_text_clip, logo_clip])

    # Export a single frame as an image
    frame = final_clip.get_frame(0)  # Get the first frame
    result_image = Image.fromarray(frame)
    result_image.save("test_frame.png")  # Save the frame as an image

# Run the test function
create_countdown_screen(1, "Warmup", (0, 0, 0))
