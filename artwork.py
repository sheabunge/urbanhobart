import re


def create_slug(string):
	return re.sub(r'[\W]+', '-', string.lower().replace('\'', '')).strip('-')


class Artwork:

	def __init__(self, fields=None):

		self.lat = self.long = None

		self.title = ''
		self.id = ''

		self.artist = ''

		self.material = ''
		self.address = ''
		self.description = ''
		self.type = ''

		self.year = None
		self.date = None

		self.link_url = ''
		self.images = []

		if fields:
			self.set_fields(fields)

	def add_image(self, image_url):
		self.images.append(image_url)

	def get_field(self, field, value=None):
		return self.__dict__[field] if field in self.__dict__ else value

	def get_fields(self):
		return {field: value for field, value in self.__dict__.items() if value}

	def set_fields(self, fields):
		for field, value in fields.items():
			if value and field in self.__dict__:
				self.__dict__[field] = value
