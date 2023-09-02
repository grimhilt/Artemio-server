from api import create_api
from screen.ScreenManager import ScreenManager

#api = create_api()
#screen_manager = ScreenManager().getInstance()

if __name__ == '__main__':
    #api.run(host="0.0.0.0", port=5500, debug=True)
    #api.run(host="0.0.0.0", port=5500)
    from screen.SlideShow import SlideShow
    import tkinter as tk
    import mpv
    import imageio
    #player = mpv.MPV(ytdl=True)
    #player.play("./data/VID_20230403_143809.mp4")
    #video_file_path = "./data/VID_20230403_143809.mp4"
    #video = imageio.get_reader(video_file_path, "ffmpeg")

# Get the number of frames and the frame rate
    #num_frames = len(video)
    #frame_rate = video.get_meta_data()['fps']

# Calculate the duration in seconds
    #duration = num_frames / frame_rate
    #print(duration)
    root = tk.Tk()
    root.title("Slideshow")
    files = [
            {"name": "VID_20230403_143809.mp4", "type":"video/mp4", "seconds":0},
            {"name": "egg.jpg", "type":"image/jpg", "seconds":7},
            ]
    SlideShow(root, files)
    root.mainloop()


