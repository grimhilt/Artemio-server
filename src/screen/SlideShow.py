import tkinter as tk
import cv2
from PIL import Image, ImageTk, Image
from tkvideo import tkvideo
import time
import imageio
import mpv

class SlideShow:
    def __init__(self, root, files):
        print(files)
        self.root = root
        self.files = files
        self.idx = -1

        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.pack()
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.pack_propagate(False)

        self.root.after(100, self.next_file)

    def next_file(self):
        media = None
        while media is None or not media.supported:
            self.idx = (self.idx + 1) % len(self.files)
            file = self.files[self.idx]
            media = MediaFactory(self, file)

        print(media.time)
        print(self.idx)

        self.root.after(media.time, self.next_file)

    def resize_full_screen(self, image):
        # Get root window width and height
        screen_width = self.root.winfo_width()
        screen_height = self.root.winfo_height()

        # Resize the image to fit the screen
        return image.resize((screen_width, screen_height), Image.BICUBIC)

    def show_image(self, image):
        self.image = image
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

class MediaFactory:
    def __init__(self, parent, file):
        self.parent = parent
        self.file = file
        print(self.file)
        self.supported = True
        match file['type']:
            case "image/jpeg" | "image/jpg":
                self.image_player()
            case "video/mp4" | "image/gif":
                self.video_player()
            case _:
                print(file['type'], " not supported")
                self.supported = False

    def image_player(self):
        print("image player")
        path = './data/' + self.file['name']
        image = Image.open(path)

        image = self.parent.resize_full_screen(image)
        photo = ImageTk.PhotoImage(image=image)
        self.parent.show_image(photo)
        self.time = self.file['seconds'] * 1000

    def video_player(self):
        video_player = VideoPlayer(self.parent, self.file)
        self.time = video_player.time

class VideoPlayer:
    def __init__(self, parent, file):
        self.file = file
        self.parent = parent
        self.path = './data/' + self.file['name']
        self.mpv_instance = mpv.MPV(wid=str(self.parent.canvas.winfo_id()))
        
        self.cap = cv2.VideoCapture(self.path)
        
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.time = int(self.total_frames * ((int(1000/self.fps))))

        self.mpv_instance.play(self.path)
