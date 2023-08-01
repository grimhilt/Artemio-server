import tkinter as tk
from PIL import ImageTk, Image
import time

class SlideShow:
    def __init__(self, root, files):
        self.root = root
        self.files = files
        self.idx = 0

        self.image_label = tk.Label(root)
        self.image_label.pack()
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.root.after(100, self.next_file)

    def next_file(self):
        file = self.files[self.idx]
        path = './data/' + file['name']
        image = Image.open(path)

        # Get root window width and height
        screen_width = self.root.winfo_width()
        screen_height = self.root.winfo_height()

        # Resize the image to fit the screen
        image = image.resize((screen_width, screen_height), Image.ANTIALIAS)

        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

        self.idx = (self.idx + 1) % len(self.files)
        self.root.after(file['seconds'] * 1000, self.next_file)

