import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class ImageViewer:
    def __init__(self, image_folder):
        self.image_folder = image_folder
        self.images_to_delete = set()
        self.current_index = 0

        # Get list of images
        self.image_files = [f for f in os.listdir(image_folder)
                            if f.lower().endswith('.jpg')]

        # Create main window
        self.root = tk.Tk()
        self.root.title("Image Viewer")
        self.root.geometry("800x600")

        # Main frame.
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for images.
        self.canvas = tk.Canvas(self.main_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Frame for buttons.
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        # Buttons.
        ttk.Button(self.button_frame, text="Previous", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Next", command=self.next_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.button_frame, text="Mark to delete", command=self.toggle_delete).pack(side=tk.LEFT,
                                                                                              padx=5)
        ttk.Button(self.button_frame, text="Finish", command=self.finish).pack(side=tk.RIGHT, padx=5)

        # Status label.
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.pack(pady=5)

        # Ensure the window is visible and has focus.
        self.root.deiconify()
        self.root.focus_force()

        # Show first image
        if self.image_files:
            self.root.update()
            self.root.after(100, self.show_current_image)

    def show_current_image(self):
        if 0 <= self.current_index < len(self.image_files):
            # Load and resize image
            image_path = os.path.join(self.image_folder, self.image_files[self.current_index])
            image = Image.open(image_path)

            # Calculate dimensions to fit the canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Resize maintaining proportion
            image.thumbnail((canvas_width, canvas_height))

            # Convert for tkinter
            self.photo = ImageTk.PhotoImage(image)

            # Show on canvas
            self.canvas.delete("all")
            self.canvas.create_image(
                canvas_width // 2, canvas_height // 2,
                image=self.photo, anchor="center"
            )

            # Update status
            status = f"Image {self.current_index + 1} of {len(self.image_files)}"
            if self.image_files[self.current_index] in self.images_to_delete:
                status += " (Marked for deletion)"
            self.status_label.config(text=status)

    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.show_current_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_current_image()

    def toggle_delete(self):
        current_image = self.image_files[self.current_index]
        if current_image in self.images_to_delete:
            self.images_to_delete.remove(current_image)
        else:
            self.images_to_delete.add(current_image)
        self.show_current_image()

    def finish(self):
        self.root.destroy()

    def run(self):
        """Run the viewer and return the list of images to be deleted"""
        self.root.mainloop()
        return self.images_to_delete


def open_image_viewer(folder_path):
    """Open a ImageViewer to show all the images with the possibility of deleting unwanted images"""
    viewer = ImageViewer(folder_path)
    images_to_delete = viewer.run()

    # Process deletions after the window is closed
    deleted_count = 0
    for image in images_to_delete:
        file_path = os.path.join(folder_path, image)
        try:
            os.remove(file_path)
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting {image}: {e}")

    print(f"Deleted {deleted_count} images")
