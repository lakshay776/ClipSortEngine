import ffmpeg

def extract_audio(video):
    audio=video.replace(".mp4",".aac")
    (
        ffmpeg
        .input(video)
        .output(audio,acodec="copy",vn=None)
        .run(overwrite_output=True)
    )

extract_audio(video="../Assets/videoplayback2.mp4")