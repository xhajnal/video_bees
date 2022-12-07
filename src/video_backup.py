import vlc
from tkinter import *
import time

# DEPRECATED
# def play_tk_opencv(input_video, frame_range, fps, speed):
#     root = Tk()
#     root.geometry("600x600")
#     video = cv2.VideoCapture(input_video)
#     # window name and size
#     cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
#     while video.isOpened():
#         # Read video capture
#         ret, frame = video.read()
#         # Display each frame
#         cv2.imshow("video", frame)
#
#     def on_closing():
#         video.release()
#         root.destroy()
#     root.protocol("WM_DELETE_WINDOW", on_closing)
#     root.mainloop()
#
#     try:
#         # Release capture object
#         video.release()
#         # Exit and destroy all windows
#         cv2.destroyAllWindows()
#     except OSError:
#         pass


# DEPRECATED
# def play_tk_vlc(input_video, frame_range, fps, speed):
#     os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
#     root = Tk()
#     root.geometry("600x600")
#     instance = vlc.Instance()
#     player = instance.media_player_new()
#     player.set_hwnd(root.winfo_id())
#     player.set_media(instance.media_new(input_video))
#     player.set_rate(speed)
#
#     player.play()
#     if frame_range:
#         new_time = frame_range[0] * int(1000 // fps)
#         player.set_time(new_time)
#
#     def on_closing():
#         player.stop()
#         player.get_media().release()
#         player.release()
#         player.get_instance().release()
#         root.destroy()
#
#     root.protocol("WM_DELETE_WINDOW", on_closing)
#     root.mainloop()
#
#     try:
#         player.stop()
#         player.get_media().release()
#         player.release()
#         player.get_instance().release()
#     except OSError:
#         pass


# DEPRECATED
# def play_vlc(input_video, frame_range):
#     os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
#     player = vlc.MediaPlayer(input_video)
#     player.play()
#     if frame_range:
#         new_time = frame_range[0] * int(1000 // 100)
#         player.set_time(new_time)
#         time.sleep((frame_range[1] - frame_range[0]) / 100)
#         player.pause()
#         ## TODO slow down the video
#         # player.stop()
#         # player.get_media().release()
#         # player.release()
#         # player.get_instance().release()


# DEPRECATED
# def play_vlc2(input_video, frame_range):
#     # creating an instance of vlc
#     os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
#     vlc_obj = vlc.Instance()
#
#     # creating a media player
#     vlcplayer = vlc_obj.media_player_new()
#
#     # creating a media
#     vlcmedia = vlc_obj.media_new(input_video)
#
#     # setting media to the player
#     vlcplayer.set_media(vlcmedia)
#
#     # playing the video
#     vlcplayer.play()

#
#
# def show_video(input_video, frame_range=(), video_speed=0.1, wait=False, points=()):
#     """ Shows given video.
#
#         :arg input_video: (Path or str): path to the input video
#         :arg frame_range: (list or tuple): if set shows only given frame range of the video
#         :arg video_speed: (float): ratio of rate, hence default speed is 1
#         :arg wait: (bool): if True it will wait for the end of the video
#         :arg points: (tuple of points): points to be shown over the video
#     """
#     vid_capture = cv2.VideoCapture(input_video)
#
#     if vid_capture.isOpened() is False:
#         print("Error opening the video file: ", input_video)
#         return
#     # Read fps and frame count
#     else:
#         # Get frame rate information
#         # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
#         fps = vid_capture.get(5)
#         # print("fps", fps)
#     vid_capture.release()
#
#     # vid_capture = cv2.VideoCapture(input_video)
#     #
#     # if (vid_capture.isOpened() == False):
#     #     print("Error opening the video file")
#     #
#     # while (vid_capture.isOpened()):
#     #     # vid_capture.read() methods returns a tuple, first element is a bool
#     #     # and the second is frame
#     #     ret, frame = vid_capture.read()
#     #
#     #     frame_number = int(vid_capture.get(1))
#     #
#     #     if ret is True:
#     #         if frame_range:
#     #             assert isinstance(frame_range, tuple) or isinstance(frame_range, list)
#     #             if frame_range[0] <= frame_number <= frame_range[1]:
#     #                 cv2.imshow('Frame', frame)
#     #             else:
#     #                 continue
#     #         else:
#     #             cv2.imshow('Frame', frame)
#     #     else:
#     #         break
#     #
#     # vid_capture.release()
#     # # Closes all the frames
#     # cv2.destroyAllWindows()
#
#     ## B
#     # os.add_dll_directory('D:\\VLC')
#     # media_player = MediaPlayer()
#     # media = Media("VID.mp4")
#     # media_player.set_media(media)
#     # media_player.play()
#
#     ## C
#     # play_vlc(input_video, frame_range)
#     #
#     ## make offset to capture right frame
#     # if frame_range:
#     #     if frame_range[0] > 50:
#     #         frame_range = [frame_range[0] + 50, frame_range[1] + 56]
#
#     p = Process(target=play_opencv, args=(input_video, frame_range, fps, video_speed, points,))
#     p.start()
#     if wait:
#         p.join()
#     # if frame_range:
#     #     time.sleep((frame_range[1] - frame_range[0]) / (fps * video_speed))
#     #     # time.sleep(max(5, (frame_range[1] - frame_range[0]) / (fps * video_speed)))
#     #     p.terminate()
#
#     ## D
#     # play_vlc(input_video, frame_range)
#
#     ## NOT WORKING
#     # p = Process(target=play_vlc, args=(input_video, frame_range,))
#     # p.start()
#     # p.join()
#     # print("hello")
#
#     # E
#     # play_vlc2(input_video, frame_range)
#
#     ## NOT WORKING
#     # p = Process(target=play_vlc2, args=(input_video, frame_range,))
#     # p.start()
#     # p.join()
#     # print("hello")