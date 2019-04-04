import json
import re
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

with open("all_artists.json") as file:
    all_artists = json.load(file)

print(len(all_artists))


def get_all_albums(album_names, pattern):
    studio_albums = list()

    for album in album_names:
        if ("\"" in album.text):
            album_name = re.search(pattern, album.text)
            studio_albums.append(album_name.group(0).replace("\"", ""))
        elif ("Miscellaneous songs" in album.text):
            studio_albums.append('Miscellaneous songs')

    return studio_albums


all_songs = list()

for artist in all_artists:
    try:
        artist_work = dict()
        artist_work['artist'] = artist['artist_name']

        my_url_Page = artist["artist_link"]

        artist_work['link'] = my_url_Page

        uClient = uReq(my_url_Page)
        page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")

        album_names = page_soup.findAll('h2')
        pattern = r'\"(.*?)\"'

        studio_albums = get_all_albums(album_names, pattern)

        tables = page_soup.findAll("table", {"class": "tracklist"})

        album_number = 0

        album_list = list()

        for table in tables:
            album_name = studio_albums[album_number]
            rows = table.findAll("tr")

            song_list = list()
            album = dict()
            track_number = 0
            album['album_name'] = album_name
            album["album_number"] = album_number + 1

            for row in rows:
                song = dict()

                try:
                    track_name = row.find('a')

                    # to avoid tracks without lyrics
                    if track_name == None:
                        continue

                    link = row.find('a', href=True)

                    song["track_number"] = track_number + 1
                    song["track_name"] = track_name.text

                    try:
                        song["lyrics_href"] = my_url_Page + link['href']
                    except:
                        song["lyrics_href"] = 'no lyrics'

                    song_list.append(song)
                except:
                    pass

                track_number += 1

            album['songs'] = song_list

            album_number += 1
            album_list.append(album)

        artist_work['career'] = album_list
        print(artist_work['artist'])
        all_songs.append(artist_work)

    except:
        pass

with open('all_songs.json', 'w') as fp:
    json.dump(all_songs, fp)
