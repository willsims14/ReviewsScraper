class Review(object):
	title = ""
	sub_title = ""
	star_rating = ""
	author = ""
	text = ""
	date = ""
	time = ""
	page_num = ""
	location = ""

	def __init__(self):
		self.title = ""
		self.sub_title = ""
		self.star_rating = ""
		self.author = ""
		self.text = ""
		self.date = ""
		self.time = ""
		self.page_num = ""
		self.location = ""

	def __str__(self):
		return " ({}): ".format(str(self.page_num)) + " - {}".format(self.author) 