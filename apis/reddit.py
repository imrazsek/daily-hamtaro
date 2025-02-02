import os.path
import praw
import requests
import cv2
import numpy

from auth import auth

MAX_POST = 100  # Max number of items to be collected from the subreddit (max. 100)
IMAGE_EXTENSIONS = ["jpg", "png", "jpeg"]


def download_images(dir_path, num_posts):
    if num_posts > 100:
        num_posts = MAX_POST

    # Get credentials
    credentials = auth.get_credentials()

    # Create Reddit instance
    reddit = praw.Reddit(client_id=credentials['client_id'],
                         client_secret=credentials['client_secret'],
                         user_agent=credentials['user_agent'],
                         username=credentials['username'],
                         password=credentials['password'])
    print('User logged in: ' + str(reddit.user.me()))

    # Read subreddits list file
    subr_list = open("subreddits.txt", "r")
    for line in subr_list:
        subreddit = reddit.subreddit(line.strip())
        print(f'Subreddit r\\{line.strip()} opened')

        images_saved = 0
        for post in subreddit.hot(limit=num_posts):
            if any(extension in post.url.lower() for extension in IMAGE_EXTENSIONS):
                try:
                    # Download image
                    resp = requests.get(post.url.lower(), stream=True).raw
                    image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                    # Save image if not exist
                    if not os.path.exists(f"{dir_path}/{line.strip()}-{post.id}.JPG"):
                        cv2.imwrite(f"{dir_path}/{line.strip()}-{post.id}.JPG", image)
                        images_saved += 1
                    else:
                        print(f"Image already saved - {line.strip()}-{post.id}")

                except Exception as e:
                    print(f"Error downloading {post.url.lower()}: {e}")

        print(f"Images saved of subreddit {line.strip()} {images_saved}")
