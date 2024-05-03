import requests
import re
import json
from tqdm import tqdm

# Metacritic API url
url = "https://mcgqlapi.com/api"

# Using readlines()
shows_file = open('tv-shows.txt', 'r')
shows_lines = shows_file.readlines()

shows = {}

def extract_title(line):
    # Try to match the first type of line
    match = re.search('(.*) \(.*\)', line)
    if match:
        return match.group(1)
    
    # Try to match the second type of line
    match = re.search('"(.*)" .*', line)
    if match:
        return match.group(1)
    return ''
# Obtain information using metacritic API
for show_line in tqdm(shows_lines, desc='Querying MetacriticAPI...', total=len(shows_lines)): 
    
    title = extract_title(show_line)
    title = title.replace('"', '')
    title = json.dumps(title)
    title = title[1:-1]
    
    query = (
      'query {',
      'tvshow(input: {',
      f'  title: "{title}",',
      '}) {',
      '  title',
      '  criticScore',
      '  releaseDate',
      '  genres',
      '  summary',
      '  numOfCriticReviews',
      ' }',
      '}'
    )
    query = '\n'.join(query)
    response = requests.post(url=url, json={"query": query})
    
    

    if response.status_code == 200:
        response_json = response.json()
        if 'errors' in response_json:  # If there are errors in the response
            shows[title] = {
                'title': title,
                'criticScore': None,
                'releaseDate': None,
                'genres': None,
                'summary': None,
                'numOfCriticReviews': None,
            }
          
        else:
            shows[title] = response_json
    else:
        print(" ERROR:", response.status_code)
        print(" Error details:", response.text)

with open('tv-shows.json', 'w') as output_file:
     
     output_file.write(json.dumps(shows))
