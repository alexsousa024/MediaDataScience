import requests
import re
import json
from tqdm import tqdm

# Metacritic API url
url = "https://mcgqlapi.com/api"

# Using readlines()
albums_file = open('albums.txt', 'r')
albums_lines = albums_file.readlines()

albums = {}

# Obtain information using metacritic API
# https://mcgqlapi.com/docs/albuminfo.doc.html
for album_line in tqdm(albums_lines, desc='Querying MetacriticAPI...', total=len(albums_lines)): 
    # Adjust the regex to match the format of your album data
    matches = re.findall('(.*) - (.*) \((.*)\) - (.*) - (.*) - (.*) million', album_line)
    if matches:  # Check if any matches were found
        title, artist, genre, year, label, sales = matches[0]
        query = (
          'query {',
          'album(input: {',
          f'  artist: "{artist}",',
          f'  album: "{title}",',
          '}) {',
          '  album',
          '  artist',
          '  criticScore',
          '  releaseDate',
          '  genres',
          '  publisher',
          '  numOfCriticReviews',
          ' }',
          '}'
        )
        query = '\n'.join(query)
        response = requests.post(url=url, json={"query": query})
        if response.status_code == 200:
            response_json = response.json()
            if 'errors' in response_json:  # If there are errors in the response
                albums[title] = {
                    'album': title,
                    'artist': artist,
                    'criticScore': None,
                    'releaseDate': year,
                    'genres': [genre],
                    'publisher': label,
                    'numOfCriticReviews': None,
                }
            else:
                albums[title] = response_json
        else:
            print(f"Error with album '{title}' by '{artist}': {response.status_code}")

with open('albums.json', 'w') as output_file:
     output_file.write(json.dumps(albums))