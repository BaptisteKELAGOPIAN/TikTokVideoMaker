from moviepy.editor import VideoFileClip, clips_array, vfx, TextClip, CompositeVideoClip, ColorClip
from tiktokautouploader import upload_tiktok

def split_text_intelligently(text, max_length):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return '\n'.join(lines)

def combine_videos(video_info, i, clip_duration):
    with VideoFileClip(video_info.video_name) as video1:
        with VideoFileClip(video_info.trash_video) as video2:

            total_duration = video1.duration

            start_time = video_info.most_four_replayed[i]

            video1 = video1.subclip(start_time, start_time + clip_duration)
            video2 = video2.subclip(clip_duration*i, clip_duration*i+clip_duration)

            video2 = video2.set_audio(None)

            width = 1080
            height = 1920

            video1_resized = video1.resize(height=height * 0.5)
            video2_resized = video2.resize(height=height * 0.5)

            letterbox_width = (height * 0.5) * (video1.w / video1.h)

            video1_letterboxed = vfx.crop(video1_resized, x1=(letterbox_width - width) / 2, x2=(letterbox_width + width) / 2)
            video2_letterboxed = vfx.crop(video2_resized, x1=(letterbox_width - width) / 2, x2=(letterbox_width + width) / 2)

            final_video = clips_array([[video1_letterboxed], [video2_letterboxed]])

            video_name_without_ext = video_info.video_name_no_ext

            text = f"{video_name_without_ext} #{i + 1}"
            text = split_text_intelligently(text, 22)

            txt_clip = TextClip(text, fontsize=70, color='black')
            txt_clip = txt_clip.set_pos('center').set_duration('6')

            bg_clip = ColorClip(size=(txt_clip.w + 20, txt_clip.h + 20), color=(255, 255, 255), duration=6)
            bg_clip = bg_clip.set_pos('center')

            final_video_with_text = CompositeVideoClip([final_video, bg_clip, txt_clip])

            final_video_with_text.write_videofile(f"temp_output.mp4", codec="libx264", fps=video1.fps)

            video1.close()

def upload_video(username, video_path, title, day, schedule, hashtags):
    upload_tiktok(
        video=video_path,
        description=title,
        accountname= username,
        hashtags=hashtags,
        schedule=schedule,
        day=day
    )
