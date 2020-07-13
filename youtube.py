import re
import os.path
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import config
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import urllib
import json


class Youtube:
    def get_all_video_in_channel(channel_id):
        api_key = config.YTtoken
        base_video_url = 'https://www.youtube.com/watch?v='
        base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
        first_url = base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key,
                                                                                                            channel_id)
        video_links = []
        url = first_url
        k = 0
        bool = True
        while bool:
            with urllib.request.urlopen(url) as inp:
                resp = json.load(inp)
            for i in resp['items']:
                if i['id']['kind'] == "youtube#video":
                    video_links.append(base_video_url + i['id']['videoId'])
                    k += 1
                    if k == 3:
                        bool = False
        data = video_links
        with open('data.json', 'w') as file:
            json.dump(data, file)
        return video_links

