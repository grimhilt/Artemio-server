import tkinter as tk
from .SlideShow import SlideShow
from api.dao.Playlist import PlaylistDao
from multiprocessing import Process

def create_slideshow(files):
    root = tk.Tk()
    root.title("Slideshow")
    SlideShow(root, files)
    root.mainloop()

class ScreenManager:
    __instance = None
    __slideshow_process = None

    @staticmethod
    def getInstance():
        if ScreenManager.__instance == None:
            SreenManager()
        return ScreenManager.__instance

    def __init__(self):
        if ScreenManager.__instance != None:
            raise Exception("Screen manager already exists!")
        else:
            ScreenManager.__instance = self
    
    def activate_playlist(self, playlist_id):
        (_, files) = PlaylistDao.get_playlist(playlist_id)
        self.disactivate_playlist()
        x = Process(target=create_slideshow, args=(files,))
        x.start()
        self.__slideshow_process = x

    def disactivate_playlist(self):
        if self.__slideshow_process:
            self.__slideshow_process.terminate()
            self.__slideshow_process = None
