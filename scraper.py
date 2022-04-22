from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
import warnings

warnings.filterwarnings('ignore')


def book_scraping():
    driver = webdriver.Chrome()
    driver.get("http://books.toscrape.com/")
    driver.implicitly_wait(4)
    book_list = pd.DataFrame(columns=['Title', 'Price', 'Rating', 'Available'])

    n_pages = (int(driver.find_element_by_class_name('current').text[-2:]))

    for i in range(n_pages):
        soup = bs(driver.page_source, parser="lxml")
        for book in soup.find("ol", class_="row").find_all("li"):

            book_name = book.find("article", class_="product_pod").find("h3").a["title"]
            book_price = book.find("article", class_="product_pod").find("div", class_="product_price").p.text
            book_rating = book.find("article", class_="product_pod").p["class"][1]
            book_available = (book.find("article", class_="product_pod")
                              .find("div", class_="product_price")
                              .find("p", class_="instock availability")
                              .text.lstrip("\n\n    \n        ").rstrip("\n    \n"))

            book_list = book_list.append({'Title': book_name, 'Price': book_price, 'Rating': book_rating, 'Available': book_available}, ignore_index=True)
        print('Scraped page ', i+1)

        if i < n_pages-1:
            driver.find_element_by_class_name('next').find_element_by_tag_name('a').click()
    print('Done!')
    print('Collecting Genres...')
    book_list = genre_classification(book_list, driver)
    print('Done!')
    print('Closing Application...')
    driver.quit()

    return book_list


def genre_classification(book_list, driver):
    
    book_list['Genre'] = 'Other'
    
    for cat in range(len(driver.find_element_by_class_name('side_categories').find_element_by_tag_name('ul').find_element_by_tag_name('ul').find_elements_by_tag_name('li'))):
        cur_cat = driver.find_element_by_class_name('side_categories').find_element_by_tag_name('ul').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[cat]
        category = cur_cat.find_element_by_tag_name('a').text
        
        cur_cat.find_element_by_tag_name('a').click()

        soup = bs(driver.page_source, 'lxml')
        
        for book in soup.find("ol", class_="row").find_all("li"):
            
            book_name = book.find("article", class_="product_pod").find("h3").a["title"]
            book_list.loc[book_list.Title == book_name, 'Genre'] = category
            
    return book_list


def run():

    try:
        book_csv = pd.read_csv('/home/gabriel/Desktop/Projetos/BookClub/book_lista.csv')
    except:
        pass

    book_list = book_scraping()
    
    if 'book_csv' in vars():

        book_csv = book_csv.append(book_list)
        book_csv.to_csv('/home/gabriel/Desktop/Projetos/BookClub/book_lista.csv')
    else:

        book_list.to_csv('/home/gabriel/Desktop/Projetos/BookClub/book_lista.csv')


if __name__ == '__main__':
    run()
