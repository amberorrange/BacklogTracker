"""Script to seed database."""

import os
import crud
import server
import requests
from model import db, User, Game, Genre, Review, Backlog, Platform, connect_to_db

os.system('dropdb backlogs')
os.system('createdb backlogs')

connect_to_db(server.app)
db.create_all()

#get all the genres and add to db
url = 'https://api.rawg.io/api/genres'
payload = {'key': os.environ['RAWG_KEY']}
res = requests.get(url, params=payload)
data = res.json()
genres = data["results"]

for genre in genres:
	added_genre = Genre(name = genre["name"])
	db.session.add(added_genre)
	db.session.commit()


#add platforms to db
platforms = [ "PC",
            "PlayStation 5",
            "PlayStation 4",
          	"Xbox One",
            "Xbox Series S/X",
         	"Nintendo Switch",
      		"iOS",
    		"Android",
          	"Nintendo 3DS",
         	"Nintendo DS",
          	"macOS",
         	"Linux",
          	"Xbox 360",
          	"Xbox",
          	"PlayStation 3",
          	"PlayStation 2",
			"PlayStation",
          	"PS Vita",
          	"PSP",
        	"Wii U",
         	"Wii",
          	"GameCube",
         	"Nintendo 64",
       		"Game Boy Advance",
       		"Game Boy",
			"Other"]

for platform in platforms:
	added_platform =  Platform(name = platform)
	db.session.add(added_platform)
	db.session.commit()

#create 10 users
for n in range(10):
	fname = f"test{n + 1}"
	lname = f"test{n + 1}"
	email = f"test{n + 1}@test.test"
	password = "testpw!!"

	crud.create_user(fname, lname, email, password)

