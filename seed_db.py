"""Script to seed database."""

import os
import crud
import model
import server
import requests

os.system('dropdb backlogs')
os.system('createdb backlogs')

model.connect_to_db(server.app)
model.db.create_all()


#want to get all the genres and add to database

url = 'https://api.rawg.io/api/genres'
payload = {'key': os.environ['RAWG_KEY']}
res = requests.get(url, params=payload)
data = res.json()
genres = data["results"]

for genre in genres:
	added_genre = model.Genre(name = genre["name"])
	model.db.session.add(added_genre)
	model.db.session.commit()

