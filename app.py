from flask import Flask, render_template
import json
from artwork import Artwork, create_slug
from random import shuffle
import requests.utils

app = Flask(__name__)

artwork_list = {}
materials = {''}
artists = {''}
types = {''}


def map_slugs(list):
	return {create_slug(name): name for name in sorted(list)}


def load_json():
	global artwork_list, materials, artists, types

	with open('data/artwork.json', 'r') as datafile:
		for record in json.load(datafile):
			record = Artwork(record)

			if not record.images:
				continue

			artwork_list[record.id] = record

			materials.update(record.material.split(', '))
			artists.update(record.artist.split(', '))
			types.update(record.type.split(', '))

	materials = map_slugs(materials)
	artists = map_slugs(artists)
	types = map_slugs(types)

	del materials['']
	del artists['']
	del types['']


load_json()

global_context = {
	'materials': materials,
	'artists': artists,
	'types': types
}


@app.template_filter('heading')
def create_link_list(value):
	value = value.title()

	for word in ('and', 'of', 'in'):
		value = value.replace(f' {word.title()} ', f' {word} ')

	return value


@app.template_filter('slug')
def create_link_list(value):
	return create_slug(value)


@app.template_filter('link_list')
def create_link_list(values, url_base):
	links = []

	for value in values.split(', '):
		links.append(f'<a href="/{url_base}/{create_slug(value)}">{value}</a>')

	return ', '.join(links)


@app.route('/')
def render_index():
	artwork = list(artwork_list.values())
	shuffle(artwork)

	return render_template('index.html', artworks=artwork, **global_context)


@app.route(r'/artwork/<artwork_id>')
def render_artwork(artwork_id):
	artwork = artwork_list[artwork_id]
	print(artwork.get_fields())

	map_url = ''
	address_overrides = {
		'Marieville esplanade foreshore': 'Marieville Esplanade, Sandy Bay TAS',
		'Derwent Lane jetty': 'Derwent Lane, Battery Point TAS'
	}

	url_base = 'https://www.google.com/maps/embed/v1/search?key=AIzaSyDHcTEGDOEvnSfv7oQbEcGxzIWFxPVDeM4'

	if artwork.lat and artwork.long:
		map_url = url_base + '&q=' + requests.utils.quote(f'{artwork.lat},{artwork.long}')
	if artwork.address:
		map_url = url_base + '&q=' + requests.utils.quote(artwork.address)

	return render_template('artwork.html', artwork=artwork, map_url=map_url, **global_context)


def render_filtered_index(field, search_value):
	results = []
	search_value = create_slug(search_value)

	for artwork in artwork_list.values():
		current_value = artwork.__dict__[field]

		if ', ' in current_value:
			values = list(map(create_slug, current_value.split(', ')))
			if search_value not in values and search_value != current_value:
				continue
		elif search_value != create_slug(current_value):
			continue

		results.append(artwork)

	shuffle(results)
	return render_template('index.html', filter=field, filter_value=search_value, artworks=results, **global_context)


@app.route('/artist/<artist>')
def render_artist(artist):
	return render_filtered_index('artist', artist)


@app.route('/type/<artwork_type>')
def render_artwork_type(artwork_type):
	return render_filtered_index('type', artwork_type)


@app.route('/material/<material>')
def render_material(material):
	return render_filtered_index('material', material)


if __name__ == '__main__':
	app.run(debug=True)
