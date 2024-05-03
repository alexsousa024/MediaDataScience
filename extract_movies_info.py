import requests
import re
import json
from tqdm import tqdm

# Metacritic API url
url = "https://mcgqlapi.com/api"

# Using readlines()
movies_file = open('movies.txt', 'r')
movies_lines = movies_file.readlines()

movies = {}



# Obtain information using metacritic API
# https://mcgqlapi.com/docs/movieinfo.doc.html
for movie_line in tqdm(movies_lines, desc='Querying MetacriticAPI...', total=len(movies_lines)): 
    title, year = re.findall('(.*) \((.*)\)', movie_line)[0]
    query = (
      'query {',
      'movie(input: {',
      f'  title: "{title}",',
      f'  year: "{year}"',
      '}) {',
      '  title',
      '  criticScore',
      '  year',
      '  director',
      '  releaseDate',
      '  genres',
      '  cast',
      '  rating',
      '  runtime',
      '  summary',
      '  numOfCriticReviews',
      ' }',
      '}'
    )
    query = '\n'.join(query)
    response = requests.post(url=url, json={"query": query})
    if response.status_code == 200:
        movies[title] = response.json()

with open('movies.json', 'w') as output_file:
     output_file.write(json.dumps(movies))
