import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import string

all_artists = list()

pages = list(string.ascii_lowercase)
# special case for artists starting with number
pages.append("09")

## source for lyrics: Easy for scraping
my_url_Page = 'http://www.alivelyrics.com'

for letter in pages:

    page_url = my_url_Page+"/"+letter
    uClient = uReq(page_url)
    page_html = uClient.read()
    page_soup = soup(page_html, "html.parser")
    artists_list_page = page_soup.findAll("div", style="padding: 8px;")

    i = 0
    for artist_list in artists_list_page:
        artists = artist_list.findAll('a', href = True)
        for artist in artists:
            artist_dict = dict()
            artist_dict['artist_name'] = artist.text
            artist_dict['artist_link'] = my_url_Page + artist['href']
            all_artists.append(artist_dict)

with open('all_artists.json', 'w') as fp:
    json.dump(all_artists, fp)
