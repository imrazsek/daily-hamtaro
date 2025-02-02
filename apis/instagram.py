from instagrapi import Client
import json
import os

CAPTION_TEXT = "#anime #memes #animememes #funnymemes"


class InstagramUploader:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = Client()
        self.session_file = f"session_{username}.json"

    def handle_challenge(self, username):
        """Handles Instagram verification challenge"""
        while True:
            try:
                code = input("Enter the verification code sent to your email/phone: ")
                self.client.challenge_code(code)
                break
            except Exception as e:
                print(f"Incorrect code or error: {e}")
                retry = input("Do you want to try another code? (y/n): ")
                if retry.lower() != 'y':
                    raise

    def load_session(self):
        """Loads a previously saved session"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    return self.client.load_settings(json.load(f))
            return False
        except Exception as e:
            print(f"Error loading session: {e}")
            return False

    def save_session(self):
        """Saves the current session"""
        try:
            session_data = self.client.get_settings()
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f)
            print("Session saved successfully")
        except Exception as e:
            print(f"Error saving session: {e}")

    def login(self):
        """Handles the login process with challenge handling"""
        try:
            # Try to load existing session
            if self.load_session():
                print("Session loaded successfully")
                return True

            print("Starting new login...")
            login_success = False

            # First attempt: basic login
            try:
                login_success = self.client.login(self.username, self.password)
            except Exception as e:
                print(f"Error in initial login: {e}")

            # Second attempt: with verification code if needed
            if not login_success:
                try:
                    code = input("Enter two-factor authentication code: ")
                    login_success = self.client.login(self.username, self.password, verification_code=code)
                except Exception as e:
                    print(f"Error in 2FA login: {e}")

            # If login was successful, save the session
            if login_success:
                self.save_session()
                return True

            return False

        except Exception as e:
            print(f"Error in login process: {e}")
            return False

    def upload_album(self, dir_path, caption):
        """Uploads a photo album to Instagram"""
        try:
            # Check if directory exists
            if not os.path.exists(dir_path):
                raise Exception(f"Directory {dir_path} does not exist")

            # Get list of images
            image_files = [
                os.path.join(dir_path, f) for f in os.listdir(dir_path)
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))
            ]

            if not image_files:
                raise Exception("No images found in directory")

            # Limit to 10 images (Instagram's limit)
            if len(image_files) > 10:
                print("WARNING: Instagram allows maximum 10 images per carousel. Using first 10.")
                image_files = image_files[:10]

            # Upload the album
            media = self.client.album_upload(
                image_files,
                caption=caption
            )

            print("Album uploaded successfully")
            return image_files

        except Exception as e:
            print(f"Error uploading album: {e}")
            return None


def upload_images(dir_path):
    # Configuration
    username = "daily.hamtaro"
    password = "VSfP,Mn:G,4Ji3R"

    # Create uploader instance
    uploader = InstagramUploader(username, password)

    # Attempt login
    if uploader.login():
        # If login successful, upload the album
        return uploader.upload_album(dir_path, CAPTION_TEXT)
    else:
        print("Could not complete login")
