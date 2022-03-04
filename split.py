from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Replace the filename below.
required_video_file = "./audio/lHnEoU_4JJo"

times = [[10, 15], [20, 40]]

for time in times:
  starttime = int(time[0])
  endtime = int(time[1])
  ffmpeg_extract_subclip(required_video_file, starttime, endtime, targetname=str(times.index(time)+1)+".mp4")