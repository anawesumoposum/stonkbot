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

website_url = "https://www.marketwatch.com/tools/stockresearch/screener/"
response = urlopen('https://www.marketwatch.com/tools/stockresearch/screener/')

options = Options()
options.add_argument('--disable-gpu')
options.add_argument("Set-Cookie")
options.add_argument("HttpOnly;")
options.add_argument('SameSite=Strict')

#pandas read stock names
nasdaq = pd.read_csv("D:\\Dropbox\\Code\\Stonks\\companylist.csv") 
nasdaq_df = pd.DataFrame(nasdaq, columns=['Symbol','Name', 'LastSale', 'MarketCap', 'IPOyear', 'Setor', 'industry', 'Summary Quote'])
list_of_names = nasdaq_df['Symbol'].to_list()
print(list_of_names)
#navigate selenium
driver = webdriver.Chrome(executable_path='D:\\Dropbox\\Code\\Stonks\\chromedriver.exe',chrome_options=options)
driver.get(website_url)
driver.implicitly_wait(1)
driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[1]/form/div[2]/div[4]/input[1]").click()
element = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[1]/form/div[2]/div[5]/input[1]")
element.send_keys(".01")
element = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[1]/form/div[2]/div[5]/input[2]")
element.send_keys("3")
driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[1]/form/div[2]/div[7]/input[1]").click()
element = driver.find_element_by_id("PriceDirPct")
element.send_keys("3")
driver.find_element_by_id("submit").click()
#driver.get(website_url)
time.sleep(3)
driver.find_element_by_id("submit").click()
driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/div[5]/table/thead/tr/th[4]/a").click()
driver.implicitly_wait(1)
driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div[1]/div[5]/table/thead/tr/th[4]/a").click()
i=0
while i > 50:
    time.sleep(10)

page = driver.page_source
time.sleep(5)
driver.quit()
soup = BeautifulSoup(page, 'lxml')

with open("D:\\Dropbox\\Code\\Stonks\\output.html", 'w+') as appendFile:
    appendFile.write(str(page))
    
