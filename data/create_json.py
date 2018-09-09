
import csv
import json
import os
from os import path
from artwork import Artwork, create_slug
from urllib.request import urlretrieve
from urllib.error import HTTPError


DOWNLOAD_IMAGES = True

with open('urban_art.csv', mode='r', encoding='utf-8-sig') as csv_file:
	reader = csv.DictReader(csv_file)
	records = list(reader)

with open('urban_art_walls.csv', mode='r', encoding='utf-8-sig') as csv_file:
	reader = csv.DictReader(csv_file)
	records.extend(reader)

image_dir = path.join(path.dirname(path.abspath(path.curdir)), 'static', 'images', 'full')

if not path.exists(image_dir):
	os.makedirs(image_dir)

artwork_ids = set()
artworks = []
data = []

for record in records:
	artwork = Artwork()

	fields = ['Artist', 'Title', 'Address', 'Description', 'Type', 'Link_URL']

	for field in fields:
		if record.get(field):
			artwork.__setattr__(field.lower(), record[field])

	if artwork.type == 'Aluminium bands bearing text on walls':
		artwork.type = 'Aluminium'

	if record.get('X'):
		artwork.long = record.get('X')

	if record.get('Y'):
		artwork.lat = record.get('Y')

	if record.get('Materials'):
		artwork.material = record['Materials']

	if record.get('Date'):
		artwork.year = record['Date']

	if record.get('Date_'):
		artwork.year = record['Date_']

	if record.get('Date_Painted'):
		artwork.date = record['Date_Painted']

	uid = slug = create_slug(artwork.title)
	i = 1

	while uid in artwork_ids:
		uid = f'{slug}-{i}'
		print('id conflict', uid)
		i += 1

	artwork_ids.add(uid)
	artwork.id = uid

	image_urls = []

	image = 1
	while record.get(f'URL_{image}'):
		image_urls.append(record[f'URL_{image}'])
		image += 1

	image = 0
	for image_url in image_urls:
		suffix = '' if image == 0 else '-alt'
		suffix += '' if image <= 1 else str(image)

		_, ext = path.splitext(image_url)
		ext = ext.lower()
		ext = '.jpg' if ext == '.jpeg' else ext

		filename = artwork.id + suffix + ext

		if path.exists(filename):
			print(f'{filename} already exists')
		else:
			print(f'downloading {image_url} to {filename}')

			try:
				urlretrieve(image_url, path.join(image_dir, filename))
			except HTTPError as e:
				print(e.msg)
				continue

		artwork.remote_images.append(image_url)
		artwork.add_image(filename)
		image += 1

	artworks.append(artwork)
	data.append(artwork.get_fields())

with open('artwork.json', 'w') as outfile:
	json.dump(data, outfile, indent=4)
