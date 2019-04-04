from os import listdir, getcwd
import json

print(getcwd())

path = 'lyrics_by_artist'
all_artist = listdir(path)

all_lyrics_combined = list()

for artist in all_artist:

    file = path + '/' + artist

    try:
        with open(file) as file:
            current_artist_lyrics = json.load(file)

    except:
        continue

    all_lyrics_combined.append(current_artist_lyrics)

with open('all_lyrics.json', 'w') as fp:
    json.dump(all_lyrics_combined, fp, indent=4, sort_keys=True)
