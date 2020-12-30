from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import re
import requests
from itertools import zip_longest
from webdriver_manager.chrome import ChromeDriverManager

pages = ['10818853?page=1', 
         '10818853?page=2']

lists = []
books = []
# First-page site URL: https://www.goodreads.com/shelf/show/business?page=1
for page in pages:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.goodreads.com/list/book/" + str(page))
    
    
    try: # Taking list
        html = driver.page_source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for name_box in soup.find_all('a', class_='listTitle'):
                name = name_box.text.strip()
                lists.append(name)

                #print(lists)
    
    except:
            lists.append("Blank")


    try: # Taking list
        html = driver.page_source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for name_box in soup.find_all('a', class_='listTitle'):
                book = name_box['href']
                books.append(book)
                #print(lists)
    
    except:

            books.append("Blank")
            

    driver.close()

final = pd.DataFrame(list(zip(books, lists)))
final = final.rename(columns={0: 'Link', 1: 'List'})

