import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import pandas

# Get hold of the website
driver = webdriver.Chrome()
driver.get(
    "https://www.audible.in/?&source_code=AUDPP30DTRIAL44911252200DX&gclid=Cj0KCQjw_O2lBhCFARIsAB0E8B8mNmlfU"
    "-d_xqfxCqdtvY-nn6pxZWyBQ0rUXOjNbUhe_iln_3ON-PEaAl8HEALw_wcB")

# Navigate to best sellers
browse = driver.find_element(By.LINK_TEXT, "Browse")
browse.click()
time.sleep(2)
best_sellers = driver.find_element(By.LINK_TEXT, "Best Sellers")
best_sellers.click()
time.sleep(5)

# Change number of books displayed to 50
dropdown_element = driver.find_element(By.CSS_SELECTOR, "select.bc-input.refinementFormDropDown")
dropdown = Select(dropdown_element)
dropdown.select_by_value("50")
time.sleep(5)


def get_book_datas(file_name):
    """Creates a csv file with all the books in the particular category.\n
          parameter:
                file_name (file name for the csv)"""
    names = []
    writers = []
    narrators = []
    durations = []
    release_dates = []
    languages = []
    all_ratings = []
    second_page = True
    for i in range(2):
        books_list = driver.find_elements(By.CLASS_NAME, "productListItem")
        for book in books_list:
            try:
                name = book.find_element(By.CSS_SELECTOR, "h3 a").text
                writer = book.find_element(By.CLASS_NAME, "authorLabel").text
                narrator = book.find_element(By.CLASS_NAME, "narratorLabel").text
                duration = book.find_element(By.CLASS_NAME, "runtimeLabel").text
                release_date = book.find_element(By.CLASS_NAME, "releaseDateLabel").text
                lang = book.find_element(By.CLASS_NAME, "languageLabel").text
                ratings = book.find_element(By.CLASS_NAME, "ratingsLabel").text
                names.append(name)
                writers.append(writer)
                narrators.append(narrator)
                durations.append(duration)
                release_dates.append(release_date)
                languages.append(lang)
                all_ratings.append(ratings)
            except selenium.common.exceptions.NoSuchElementException:
                pass
        if second_page:
            next_page = driver.find_element(By.LINK_TEXT, "Go forward a page")
            driver.execute_script("arguments[0].scrollIntoView();", next_page)
            next_page.click()
            time.sleep(5)
            second_page = False

    top_sellers = {
        "Name": names,
        "Written_by": writers,
        "Narrated_by": narrators,
        "Duration": durations,
        "Release_Date": release_dates,
        "Language": languages,
        "Rating": all_ratings
    }

    df = pandas.DataFrame(top_sellers)
    df.index = df.index + 1
    df.to_csv(f"top_sellers/{file_name}")


# Get hold of all the categories
categories = driver.find_elements(By.CSS_SELECTOR, "div.linkListWrapper.categories li")
category_list = [name.text for name in categories]

# Creates a csv for each category
for category in category_list[::-1]:
    category_name = driver.find_element(By.LINK_TEXT, category)
    category_name.click()
    time.sleep(8)
    get_book_datas(f"Audible Top Sellers in {category}")

