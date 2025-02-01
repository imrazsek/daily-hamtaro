import os.path

import praw
import requests
import cv2
import numpy

from auth import auth

MAX_POST = 10
IMAGE_EXTENSIONS = ["jpg", "png", "jpeg"]

def download_images(dir_path):
    # Get credentials.
    CREDENTIALS = auth.get_credentials()

    # Create Reddit instance.
    reddit = praw.Reddit(client_id=CREDENTIALS['client_id'],
                         client_secret=CREDENTIALS['client_secret'],
                         user_agent=CREDENTIALS['user_agent'],
                         username=CREDENTIALS['username'],
                         password=CREDENTIALS['password'])
    print('User logged in: ' + str(reddit.user.me()))

    # Read subreddits list file
    subr_list = open("subreddits.txt", "r")
    for line in subr_list:
        subreddit = reddit.subreddit(line.strip())
        print(f'Subreddit r\\{line.strip()} opened')

        for post in subreddit.hot(limit=MAX_POST):
            if any(extension in post.url.lower() for extension in IMAGE_EXTENSIONS):
                try:
                    resp = requests.get(post.url.lower(), stream=True).raw
                    image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                    # Save image if not exist
                    if not os.path.exists(f"{dir_path}/{line.strip()}-{post.id}.JPG"):
                        print(f"Image saved - {post.id}")
                        cv2.imwrite(f"{dir_path}/{line.strip()}-{post.id}.JPG", image)
                    else:
                        print(f"Image already saved - {post.id}")

                except Exception as e:
                    print(f"Image download failed {post.url.lower()}")
                    print(e)
