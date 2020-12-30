from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import pandas as pd
import time
import re
import requests
from itertools import zip_longest
from webdriver_manager.chrome import ChromeDriverManager

pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
title = []
author = []
rating = []
desc = []
ratingcount = []
yearpub = []
series = []

for page in pages:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # Reading the second page
    driver.get("https://www.goodreads.com/user/sign_in")
    driver.find_element_by_css_selector("#user_email").send_keys("emailid")
    driver.find_element_by_css_selector("#user_password").send_keys("password")
    driver.find_element_by_xpath("//input[@type='submit' and @value='Sign in']").click()
    driver.get("https://www.goodreads.com/shelf/show/erotica?page=" +str(page))
    time.sleep(3)
    
    
    summaryItems = driver.find_elements_by_xpath("//a[contains(@class, 'bookTitle')]")
    job_links = [summaryItem.get_attribute("href") for summaryItem in summaryItems]
    
    
    for job_link in job_links:
        driver.get(job_link)
    
        #Closing the pop-up window
        try:
            close = driver.find_elements_by_class_name('gr-iconButton')
            close.click()
    
        except:
    
            close = "None"
        try:
            # Taking book description
            more = driver.find_element_by_css_selector("#description > a:nth-child(3)").click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            #for item in soup.findAll("span", id=re.compile("^freeText"))[:2]:
            #    print(item.text)
            sections = soup.findAll("span", id=re.compile("^freeText"))[:2]
            print("message ")
            i = 0
            for item in soup.findAll("span", id=re.compile("^freeText"))[:2]:
                i = i+1
                if i == 2:
                    desc.append(item.text)
    
        except:
    
            desc.append("Blank")
        
    
    
        try: # Taking book title
                   # time.sleep(2)
            job_title = driver.find_element_by_xpath("//h1[@class='gr-h1 gr-h1--serif']").text
                    #job_title = driver.find_element_by_id('bookTitle').find_element_by_class_name('gr-h1 gr-h1--serif').text
            title.append(job_title)
                    #print(title)
    
        except:
            title.append("Blank")
    
        try: # Taking book series
                   # time.sleep(2)
            bookseries = driver.find_element_by_xpath("//a[@class='greyText']").text
                    #job_title = driver.find_element_by_id('bookTitle').find_element_by_class_name('gr-h1 gr-h1--serif').text
            series.append(bookseries)
                    #print(title)
    
        except:
            series.append("Blank")
            #Taking Author name
    
        try:
                   # time.sleep(2)
            authors = driver.find_element_by_xpath("//a[@class='authorName']").text
            author.append(authors)
                        #print(author)
    
        except:
            author.append("Blank")
    
            #Taking Ratings
    
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
        
            rate = soup.find("span", itemprop="ratingValue").text.strip()
            rates = rate.replace('\n','')
        
            rating.append(rates)
        
        except:
            rating.append("Blank")

            
    
             #Taking Ratings count
    
        try:
                   # time.sleep(2)
            ratecount = driver.find_element_by_xpath("//a[@class='gr-hyperlink']").text
            ratingcount.append(ratecount)
                        #print(author)
    
        except:
            ratingcount.append("Blank")
    
           #Taking Ratings count
    
        try:
                   # time.sleep(2)
            
            divs = soup.find_all('div', {'class':'row'})
            div = divs[1]
            yearpub.append(div)
                        #print(author)
    
        except:
            yearpub.append("Blank")
    
    driver.close()

final = pd.DataFrame(list(zip(author, title, desc, rating, ratingcount, yearpub, series)))


