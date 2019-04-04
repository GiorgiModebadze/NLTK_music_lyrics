import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from os import listdir

file_list = listdir('lyrics_by_artist')

with open('all_songs.json') as file:
    all_artists = json.load(file)

for artist in all_artists:

    if "/" in artist['artist']:
        file_name = artist['artist'].replace("/","-") + ".json"
    else:
        file_name = artist['artist'] + ".json"

    if file_name not in file_list:

        print(file_name)

        for album in artist['career']:
            for song in album['songs']:

                href = song['lyrics_href']
                del song['lyrics_href']

                try:
                    uClient = uReq(href)
                    page_html = uClient.read()
                    page_soup = soup(page_html, "html.parser")
                    containers = page_soup.find("pre", {"class": "lyrics"})

                    song['text'] = containers.text.rstrip()
                    song['text'] = song['text'].strip()
                    song['text'] = song['text'].replace('\r\n', " ")
                    song['text'] = song['text'].replace('\n', " ")

                except:
                    pass

        del artist['link']

        with open("lyrics_by_artist/" + file_name, 'w') as fp:
            json.dump(artist, fp)

