from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import time
import warnings

warnings.filterwarnings('ignore')

def book_scraping():
    driver = webdriver.Chrome()
    driver.get("http://books.toscrape.com/")
    book_list = pd.DataFrame(columns = ['Title','Price','Rating','Available'])

    n_pages = (int(driver.find_element_by_class_name('current').text[-2:]))

    for i in range(n_pages):
        driver.implicitly_wait(4)
        soup = bs(driver.page_source, parser="lxml")
        for book in soup.find("ol", class_="row").find_all("li"):

            book_name = book.find("article", class_="product_pod").find("h3").a["title"]
            book_price = (book.find("article", class_="product_pod").find("div", class_="product_price").p.text)
            book_rating = book.find("article", class_="product_pod").p["class"][1]
            book_available = (book.find("article", class_="product_pod")
                              .find("div", class_="product_price")
                              .find("p", class_="instock availability")
                              .text.lstrip("\n\n    \n        ").rstrip("\n    \n"))

            book_list = book_list.append({'Title':book_name, 'Price':book_price, 'Rating':book_rating, 'Available':book_available}, ignore_index = True)
        print('Scraped page ', i+1)

        if i < n_pages-1:
            driver.find_element_by_class_name('next').find_element_by_tag_name('a').click()
            
    return book_list