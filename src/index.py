import tkinter as tk
from PIL import ImageTk, Image
import os
import time


class SlideshowApp:
    def __init__(self, root, image_paths):
        self.root = root
        self.paths = image_paths
        self.idx = 0

        self.image_label = tk.Label(root)
        self.image_label.pack()
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.show_next_image()

    def show_next_image(self):
        img_path = self.paths[self.idx]
        image = Image.open(img_path)

        # Get root window width and height
        screen_width = self.root.winfo_width()
        screen_height = self.root.winfo_height()

        # Resize the image to fit the screen
        image = image.resize((screen_width, screen_height), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        self.idx = (self.idx + 1) % len(self.paths)
        self.root.after(2000, self.show_next_image)

def main():
    root = tk.Tk()
    root.title("Image Slideshow")


    img_paths = ["./data/960x0-1053101061.jpg", "./data/my-linux-desktop-1131547615.png", "./data/glzrkk83f4621-1200x671-54057802.jpg", "./data/yjdoiycuw04lvrebijtw-605729284.jpg"]
    app = SlideshowApp(root, img_paths)
    root.mainloop()

if __name__ == "__main__":
    main()
