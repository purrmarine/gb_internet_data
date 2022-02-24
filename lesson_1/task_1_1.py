import requests
import json

user = 'torvalds'

repos = requests.get(f'https://api.github.com/users/{user}/repos')
j_repos = repos.json()

for rep in j_repos:
    print(rep.get('name'))

with open('json_data.json', 'w') as outfile:
    json.dump(j_repos, outfile)
