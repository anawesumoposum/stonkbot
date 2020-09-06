import yfinance as yf
import requests
from bs4 import BeautifulSoup
import csv
from csv import writer
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import time
from time import sleep
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
import os
import datetime


#update current working directory
os.chdir("G:\\Dropbox\\Code\\Stonks\\")
print(os.getcwd())

#format todays date
currentdate = datetime.datetime.today()
today = (str(currentdate.month),'.',str(currentdate.day),'.',str(currentdate.year),'.csv')
today = ''.join([a for a in today]) \
    .replace(",", "-")
print(today)

#website URL's
website_url = "https://www.google.com/"
response = urlopen('https://www.google.com/')

#selenium options
options = Options()
options.add_argument('--disable-gpu')
options.add_argument("Set-Cookie")
options.add_argument("HttpOnly;")
options.add_argument('SameSite=Strict')

#pandas read stock names
nasdaq = pd.read_csv("G:\\Dropbox\\Code\\Stonks\\companylist.csv") 
nasdaq_df = pd.DataFrame(nasdaq, columns=['Symbol','Name', 'LastSale', 'MarketCap', 'IPOyear', 'Setor', 'industry', 'Summary Quote'])
nasdaq_list_of_names = nasdaq_df['Symbol'].to_list()

#navigate selenium
driver = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=options)
driver.get(website_url)
driver.implicitly_wait(1)
element = driver.find_element_by_xpath("/html/body/div/div[5]/form/div[2]/div[1]/div[1]/div/div[2]/input[1]")
element.send_keys("cheap stocks to buy now")
element.send_keys(Keys.RETURN)
driver.implicitly_wait(1)
driver.find_element_by_xpath('/html/body/div[9]/div[3]/div[3]/div/div/div[1]/div/div/div[2]/a').click()
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[9]/div[3]/div[3]/div/div/div[2]/div/div[2]').click()
driver.find_element_by_xpath('/html/body/div[9]/div[3]/div[3]/div/div/div[2]/div/ul[1]/li[3]/a').click()
time.sleep(1)

#declare empty lists
links = []
hits = []
d = dict()

#bs4 html source
page = driver.page_source
soup = BeautifulSoup(page, 'lxml')

#quit driver
driver.quit()
#soup finding 'regular search results'
srg = soup.find("div", {"id": "search"})
#iterate each <a> link and append links list
for link in srg.findAll('a'):
    links.append(link.get('href'))

#request page source from links
a=0
for individual_link in links:

    if individual_link.startswith('https'):

        #try except to pass on error
        try:
            page = requests.get(individual_link, allow_redirects=True)
            soup = BeautifulSoup(page.text, 'lxml')
            text = soup.get_text()
            with open('G:\\Dropbox\\Code\\Stonks\\temp.txt', 'w+',newline='\n',encoding='utf-8') as writeFile:
                writeFile.write(text)
            writeFile.close()
            text = open('G:\\Dropbox\\Code\\Stonks\\temp.txt','r',encoding='utf-8')
            #iterate through each line
            for line in text:
                print(line)
                for i in nasdaq_list_of_names:
                    x = re.search(i,line)
                    if x:
                        #count occurences
                        if i in d:
                            d[i] = d[i]+1
                        else:
                            d[i] = 1
                    else:
                        pass
            text.close()
        except requests.ConnectionError:
            pass
    else:
        pass

    a+=1
    print(a)

#write list on temp
os.chdir("G:\\Dropbox\\Code\\Stonks\\datatables")
with open(today,'w+',newline='\n',encoding='utf-8') as graphingData:
    for key in list(d.keys()):
        graphingData.write(str(key))
        graphingData.write(", ") 
        graphingData.write(str(d[key]))
        graphingData.write('\n')
graphingData.close()




    
