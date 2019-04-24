#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as BS
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import re

# Task1
release_tags = {}
# Put in the Pathline for the chromedriver
driver = webdriver.Chrome('C:\\Users\\paul2\\Downloads\\chromedriver')
driver.implicitly_wait(30)
# dictionary for the three open source projects and its unique page
scraping_url = {'kafka': 'apache/kafka','tensorflow':'tensorflow/tensorflow','django':'django/django'}
for key in scraping_url:
    driver.get('https://github.com/{}/tags'.format(scraping_url[key]))
    list_release_tag = []
    # creating a loop that first extract data from the current page of the chromedriver then go to the next page 
    while True:
        data_html =BS(driver.page_source,'html.parser')
        all_tags = data_html.find_all('div', class_="Box-row position-relative d-flex")
        for x in all_tags:
            cleanse_tag = re.match(r"\s+(.*)\n",x.find_all('a', href=True)[0].text).group(1)
            list_release_tag.append(cleanse_tag)
        # there is two xpath that lead to the next page so created a way to catch them
        try:
            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Next')]")))
            sleep(5)
            element.click()
        except StaleElementReferenceException:
            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[4]/div[1]/main[1]/div[2]/div[1]/div[3]/div[1]/a[2]")))
            sleep(5)
            element.click
        except:
            break
        r = { key : list_release_tag}
        release_tags.update(r)
driver.close()
# Extracting the dictonary to a json file
with open("result_task1.json", "w") as f: # writing/ rewriting the file name result.json
    for key, item in release_tags.items():      
        json.dump(str(key)+':'+str(item), f) 
        f.write("\n") # adding a new line to each key so that it is easier to see
# Task 2
for key,items in release_tags.items():
    cleanse_list = []
    for x in items:
        try:
            # cleaning the list to standardize them with digits as the first elements
            cleanse_list.append(re.search(r'(\d.*)',x).group(1))
        except AttributeError:
            cleanse_list.append(x)
    release_tags[key] = cleanse_list
# Extracting the dictonary to a json file
with open("result_task2.json", "w") as f: # writing/ rewriting the file name result.json
    for key, item in release_tags.items():      
        json.dump(str(key)+':'+str(item), f) 
        f.write("\n") # adding a new line to each key so that it is easier to see