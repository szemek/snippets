# https://github.com/kkroening/ffmpeg-python
# pip install ffmpeg-python

import ffmpeg
from glob import glob

videos = sorted(glob("**/*.mp4", recursive=True))

for video in videos:
    video_streams = ffmpeg.probe(video, select_streams = "v")

    stream = video_streams['streams'][0]
    width = stream['width']
    height = stream['height']

    print(f"{video}: {width}x{height}")
