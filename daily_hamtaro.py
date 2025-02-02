from apis import reddit, instagram
from utils.dir_manager import create_directory, delete_directory
from utils.image_viewer import open_image_viewer

# Check folder images
dir_path = create_directory("images")

# Download images from Reddit
num_posts = int(input("How many images do you want to download from each subreddit (max. 100)? "))
reddit.download_images(dir_path, num_posts)

# All photos are displayed for selection
open_image_viewer(dir_path)

upload = input("Do you want to upload all images to Instagram? (if no, type 'no' or 'n') ")
if not upload in ["no", "n"]:
    image_files = instagram.upload_images(dir_path)
    delete_directory(dir_path, image_files)

print("Bye!")
