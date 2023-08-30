import tkinter as tk
import cv2
from PIL import Image, ImageTk, Image
from tkvideo import tkvideo
import time
import imageio

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
            case "image/gif":
                self.gif_player()
            case "image/jpeg" | "image/jpg":
                self.image_player()
            case "video/mp4":
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

    def gif_player(self):
        gif_player = GIFPlayer(self.parent, self.file)
        self.time = gif_player.time

class VideoPlayer:
    def __init__(self, parent, file):
        self.file = file
        self.parent = parent
        self.path = './data/' + self.file['name']
        
        self.cap = cv2.VideoCapture(self.path)
        
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.time = int(self.total_frames * ((int(1000/self.fps)+1)))
        self.delay = int(1000/self.fps)
        self.i = -1
        self.frames = []
        self.preload()
        self.update()

    def preload(self):
        isPlaying = True
        while isPlaying:
            ret, frame = self.cap.read()
            if ret:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                image = self.parent.resize_full_screen(image)
                photo = ImageTk.PhotoImage(image=image)
                self.frames.append(photo)
            else:
                self.cap.release()
                isPlaying = False


    def update(self):
        self.i += 1
        if self.i < len(self.frames):
            self.parent.show_image(self.frames[self.i])
            self.parent.root.after(int(self.delay), self.update)
        else:
            self.frames = []

class GIFPlayer():
    def __init__(self, parent, file):
        self.parent = parent
        self.file = file
        self.path = './data/' + self.file['name']
        self.current_frame = 0
        self.time = 0
        self.play_gif()


    def load_gif_frames(self):
        gif = Image.open(self.path)
        frames = []
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(frames))  # Move to the next frame
        except EOFError:
            pass  # Reached the end of the GIF

        return frames

    def play_gif(self):
        try:
            frame = ImageTk.PhotoImage(file=self.path, format="gif -index %i" %(self.current_frame))
            self.parent.label.config(image=frame)
            self.parent.label.image = frame

            self.current_frame = self.current_frame + 1
            self.after((100), self.play_gif)
        except:
            pass
