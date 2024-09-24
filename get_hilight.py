
import requests
import sys
from debug import my_print 

def get_sponsor_segments(video_id):
    my_print('Getting sponsor segments...', 'green')

    url = "https://sponsor.ajay.app/api/skipSegments"
    params = {'videoID': video_id}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        my_print('Sponsor segments received', 'green')
        return response.json()
    else:
        my_print('Failed to get sponsor segments', 'red')
        my_print(f"Error: {response.status_code}", 'red')
        return None

def mostReplayed(video_id, nb_clip):
    res = get_sponsor_segments(video_id)
    ignore_between = [0, 0]

    if res is not None:
        ignore_between = res[0]['segment']


    ignore_between_with_marg = [ignore_between[0] - 10, ignore_between[1] + 20]

    my_print('Getting most replayed...', 'green')
    linkapi = f'https://yt.lemnoslife.com/videos?part=mostReplayed&id={video_id}'

    response = requests.get(linkapi)

    if response.status_code != 200:
        my_print('Failed to get most replayed', 'red')
        my_print(f"Error: {response.status_code}", 'red')
        return None
    
    my_print('Most replayed received', 'green')

    data = response.json()
    mostReplayed = data['items'][0]['mostReplayed']['markers']

    sorted_mostReplayed = sorted(mostReplayed, key=lambda x: x['intensityScoreNormalized'], reverse=True)

    top_4 = []

    for i in range(len(sorted_mostReplayed)):
        current_item = sorted_mostReplayed[i]

        if current_item['startMillis'] > ignore_between_with_marg[0] * 1000 and current_item['startMillis'] < ignore_between_with_marg[1] * 1000:
            continue

        if current_item['startMillis'] < 60000:
            continue

        skip = False
        for top_item in top_4:
            if abs(current_item['startMillis'] - top_item['startMillis']) < 60000:
                skip = True
                break

        if skip:
            continue

        top_4.append(current_item)
        if len(top_4) == nb_clip:
            break

    my_return = []
    for item in top_4:
        my_return.append(item['startMillis']/1000)

    return my_return