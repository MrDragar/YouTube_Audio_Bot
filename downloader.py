import pytube


def download(url: str, media_type: str):
    yt = pytube.YouTube(url)
    video_name = yt.title
    name = yt.video_id
    if media_type == "Audio":
        stream = yt.streams.filter(only_audio=True).first()
        stream.download("./audio/", filename=name)
        media_path = "./audio/" + name
    elif media_type == "Video":
        stream = yt.streams.filter(only_video=True).first()
        stream.download("./video/", filename=name)
        media_path = "./video/" + name
    return media_path, video_name

