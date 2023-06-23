from moviepy.editor import VideoFileClip
import os

def generate_thumbnail(video_path, thumbnail_path):
    clip = VideoFileClip(video_path)
    thumbnail = clip.save_frame(thumbnail_path, t=(clip.duration/2)) # save frame at half the clip's duration
