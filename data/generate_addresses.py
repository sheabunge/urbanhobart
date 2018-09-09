import json
from artwork import Artwork
import requests

GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyBWyV1hr17E7QnvQ-837US6nVHZWKs5tSw&region=AU'

with open('artwork.json', 'r') as json_file:
	records = json.load(json_file)

for i, record in enumerate(records):
	artwork = Artwork(record)

	if artwork.precise_address:
		continue

	response = None

	if artwork.lat and artwork.long:
		response = requests.get(GEOCODE_URL + '&latlng=' + requests.utils.quote(artwork.lat + ',' + artwork.long))
	elif artwork.address:
		response = requests.get(GEOCODE_URL + '&address=' + requests.utils.quote(artwork.address))

	if response:
		response = json.loads(response.text)

		if response['status'] == 'OK':
			result = response['results'][0]
			print(result)
			artwork.precise_address = result['formatted_address']
			artwork.precise_lat = result['geometry']['location']['lat']
			artwork.precise_long = result['geometry']['location']['lng']
			artwork.place_id = result['place_id']

	records[i] = artwork.get_fields()

with open('artwork.json', 'w') as outfile:
	json.dump(records, outfile, indent=4)
