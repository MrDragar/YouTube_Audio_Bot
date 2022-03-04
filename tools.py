import os
from moviepy.editor import AudioFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


max_audio_size = 45 * 1024 * 1024


def split_audio(path, name):
    paths = []
    audio_size = os.path.getsize(path)
    if audio_size < max_audio_size:
        paths.append([path, name])
        return paths
    count_audio = audio_size // max_audio_size + 1
    clip = AudioFileClip(path)
    sound_len = clip.duration
    sound_part_len = round(sound_len / count_audio)
    for i in range(count_audio):
        starttime = sound_part_len * i

        if i == count_audio - 1:
            endtime = sound_len
        else:
            endtime = sound_part_len * (i + 1)

        new_audio_path = path + "_" + str(i+1) + ".mp4"
        ffmpeg_extract_subclip(path, starttime, endtime,
                               targetname=new_audio_path)

        paths.append([new_audio_path, f"{name}   | {i + 1} Часть"])
    return paths
