# Module Imports
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Local Import
from review import Review


from states import states


def scrape_page(driver):
	# Get the table of reviews
	table = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.ID, 'ctl00_masterContent_grdReviews')))
	# Get two sets of reviews and put them into master_rows list
	rows = table.find_elements_by_class_name('grid-view-row')
	alt_rows = table.find_elements_by_class_name('grid-view-row-alt')
	master_rows = rows + alt_rows

	# Variables
	i = 0
	temp_item = {}
	reviews = list()
	valid_star_rating_image_path = "../../app_themes/soft-blue/images/icons/ico-star-full.gif"

	for row in master_rows:
		try:
			title = row.find_element_by_css_selector('h3')
			subtitle = row.find_element_by_css_selector('h5')
			author = row.find_element_by_xpath('.//span[@class="small-text"]')
			body = row.find_element_by_xpath('.//div[@style="margin-top:10px"]')
			date = row.find_element_by_xpath('.//strong')
			stars = row.find_elements_by_xpath('.//img[@src="{}"]'.format(valid_star_rating_image_path))
		except:
			print(" - ERROR - (1)")

		try:
			star_rating = len(stars)
		except:
			star_rating = "N/A"
			print(" - ERROR - (2)")

		if '2016' in date.text or '2017' in date.text or '2015' in date.text:
			space_index = date.text.index(' ')
			new_date = date.text[0:space_index]
			new_time = date.text[space_index + 1:]
		else:
			new_date = 'N/A'
			new_time = 'N/A'

		if '(' in author.text and ')' in author.text:
			first_paren_index  = author.text.index('(')
			second_paren_index = author.text.index(')')

			new_author = author.text[0:first_paren_index]
			new_location = author.text[first_paren_index+1:second_paren_index]
		else:
			new_author = author.text
			new_location = author.text

		try:
			if states[new_location]:
				new_location = new_location.replace(new_location, states[new_location])
		except:
			pass

		review = Review()
		review.title = title.text
		review.subtitle = subtitle.text.title()
		review.author = new_author
		review.location = new_location
		review.star_rating = str(star_rating)
		review.text = body.text
		review.date = new_date
		review.time = new_time
		review.page_num = int(get_current_page(driver))

		reviews.append(review)
		print "({})Scraped: {} ({})".format(i, review.author, review.location)
		i += 1
	return reviews

def go_to_next_page(driver):
	next_page_button = driver.find_element_by_id("ctl00_masterContent_grdReviews_ctl28_nextImage").click()

def get_current_page(driver):
	page_num_div = driver.find_element_by_xpath('//*[@id="ctl00_masterContent_grdReviews_ctl28_pageCell"]/span')
	current_page_num = page_num_div.find_element_by_css_selector('#ctl00_masterContent_grdReviews_ctl28_pages > option[selected="selected"]')
	return str(current_page_num.text).lstrip()

def login(driver):
	driver.get("<URL_TO_ADMIN_PANEL_GOES_HERE>")

	# Login Elements
	username_input = driver.find_element_by_xpath('//*[@id="txtUserName"]')
	password_input = driver.find_element_by_xpath('//*[@id="txtPassWord"]')
	# Login
	username_input.send_keys("<USERNAME_GOES_HERE>")
	username_input.send_keys(Keys.TAB)
	password_input.send_keys("<PASSWORD_GOES HERE>")
	password_input.send_keys(Keys.RETURN)
	return driver
