from apis import reddit
from utils.dir_manager import create_directory

# Check folder images.
dir_path = create_directory("images")

# Download images from Reddit
reddit.download_images(dir_path)
