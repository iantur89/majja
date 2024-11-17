from moviepy.config import get_setting

try:
    imagemagick_path = get_setting("IMAGEMAGICK_BINARY")
    print(f"ImageMagick path set to: {imagemagick_path}")
except Exception as e:
    print(f"Error: {e}")
