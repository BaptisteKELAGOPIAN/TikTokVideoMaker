from get_hilight import mostReplayed
from debug import my_print
from montage import combine_videos, upload_video
from datetime import date, timedelta
import os
import random
import yt_dlp

class video:
    def __init__(self, url, add_days):
        self.url = url
        self.video_id = self.extract_video_id()
        self.number_of_clips = 4
        self.clip_duration = 30
        self.most_four_replayed = mostReplayed(self.video_id, self.number_of_clips)
        self.add_days = add_days
        self.video_name = self.download_video()
        self.video_name_no_ext = os.path.splitext(os.path.basename(self.video_name))[0]
        self.hashtags = ['#fun', '#viral', '#fyp']
        self.post_timings = ['06:00', '10:00', '18:00', '22:00']
        self.trash_video = self.get_random_trash_video()

    def __str__(self):
        return f'Video: {self.video_name}\nVideo ID: {self.video_id}\nMost replayed: {self.most_four_replayed}'

    def extract_video_id(self):
        video_id = self.url.split('v=')[1]
        if '&' in video_id:
            video_id = video_id.split('&')[0]
        return video_id

    def download_video(self, output_template = '%(title)s.%(ext)s'):
        my_print('Starting the download...', 'green')
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
        }

        file_name = ''

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
            file_name = ydl.prepare_filename(ydl.extract_info(url, download=False))
        my_print('Download done', 'green')

        return file_name

    def get_random_trash_video(self):
        files = [f for f in os.listdir('trashVideo') if os.path.isfile(os.path.join('trashVideo', f))]

        if not files:
            print("No files found in the folder.")
            return None

        random_file = "trashVideo/" + random.choice(files)

        return random_file

    def clear_temp(self):
        os.remove('temp_output.mp4')


    def clear_full(self):
        try:
            os.remove(self.video_name)
            print(f"Fichier {self.video_name} supprimé avec succès.")
        except PermissionError as e:
            print(f"Erreur de suppression du fichier {self.video_name}: {e}")

    def combine_videos_and_upload(self):
        next_days = date.today() + timedelta(days=self.add_days)
        day_upload = next_days.strftime('%d')
        for i in range(len(self.most_four_replayed)):
            combine_videos(self, i, self.clip_duration)
            upload_video('tiktoktv', 'temp_output.mp4', f"{self.video_name_no_ext} clip#{i+1}", day_upload, self.post_timings[i], self.hashtags)
            self.clear_temp()
        self.clear_full()
    

if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=tyuBNZ_yAQ8&ab_channel=McflyetCarlito'
    add_days = 2
    video_info = video(url, add_days)
    video_info.combine_videos_and_upload()

    url = 'https://www.youtube.com/watch?v=UqHf1k4vMA4&ab_channel=StationService'
    add_days = 3
    video_info = video(url, add_days)
    video_info.combine_videos_and_upload()

    url = 'https://www.youtube.com/watch?v=dWbPdqns5Xk&t=1s&ab_channel=SQUEEZIE'
    add_days = 4
    video_info = video(url, add_days)
    video_info.combine_videos_and_upload()

    url = 'https://www.youtube.com/watch?v=8app7ymDevA&t=146s&ab_channel=McflyetCarlito'
    add_days = 5
    video_info = video(url, add_days)
    video_info.combine_videos_and_upload()
