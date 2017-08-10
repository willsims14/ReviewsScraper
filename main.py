# Module Imports
import pandas as pd
from selenium import webdriver

# Local Imports
import scraper
from states import states


# List of reviews
reviews = list()
num_pages = 78

# Initialize Scraping Driver
driver = webdriver.Chrome()

# Call scraper login function
driver = scraper.login(driver)

page_num = 1
while(page_num < num_pages):
	print("------- STARTING TO SCRAPE PAGE {} -------".format(str(page_num)))
	temp_reviews = scraper.scrape_page(driver)
	reviews.extend(temp_reviews)
	scraper.go_to_next_page(driver)
	page_num = int(scraper.get_current_page(driver))

driver.close()
print("--- DONE SCRAPING ---")




# Create DataFrame
df = pd.DataFrame([vars(review) for review in reviews], columns=['title', 'subtitle','star_rating','author','location','text', 'date', 'time', 'page_num'])
# Rename CSV Columns
df.rename(columns={'title':'Title', 'subtitle':'Subtitle','star_rating':'Star Rating','author':'Author Name','location':'Author Location','text':'Review Body','page_num':'Page Number'}, inplace=True)

# Pickle DataFrame for backup
df.to_pickle("pickled_reviews")

# Write DataFrame to CSV file
df.to_csv('spreadsheets/FINAL_reviews.csv')
print("--- DONE WRITING TO CSV ---")

