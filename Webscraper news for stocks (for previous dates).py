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
import progressbar


#update current working directory
#os.chdir("G:\\Dropbox\\Code\\Stonks\\")
cur_dir = os.getcwd()

#website URL's
website_url = "https://www.google.com/"
response = urlopen('https://www.google.com/')

#selenium options
options = Options()
options.add_argument('--disable-gpu')
options.add_argument("Set-Cookie")
options.add_argument("HttpOnly;")
options.add_argument('SameSite=Strict')
options.add_argument('--headless')

#pandas read stock names
#NASDAQ:
nasdaq = pd.read_csv("companylistNASDAQ.csv") 
nasdaq_df = pd.DataFrame(nasdaq, columns=['Symbol','Name', 'LastSale', 'MarketCap', 'IPOyear', 'Setor', 'industry', 'Summary Quote'])
nasdaq_symbols = nasdaq_df['Symbol'].to_list()
#add prefix
string = 'NASDAQ: '
nasdaq_list = [string + x for x in nasdaq_symbols]

#AMEX:
amex = pd.read_csv("companylistAMEX.csv") 
amex_df = pd.DataFrame(amex, columns=['Symbol','Name', 'LastSale', 'MarketCap', 'IPOyear', 'Setor', 'industry', 'Summary Quote'])
amex_symbols = amex_df['Symbol'].to_list()
#add prefix
string = 'AMEX: '
amex_list = [string + x for x in amex_symbols]

#NYSE:
nyse = pd.read_csv("companylistNYSE.csv") 
nyse_df = pd.DataFrame(nyse, columns=['Symbol','Name', 'LastSale', 'MarketCap', 'IPOyear', 'Setor', 'industry', 'Summary Quote'])
nyse_symbols = nyse_df['Symbol'].to_list()
#add prefix
string = 'NYSE: '
nyse_list = [string + x for x in nyse_symbols]

iter_one_day = 1
stock_groups = ['NYSE','NASDAQ','AMEX']

while iter_one_day < 2:#29:

    #declare empty lists/dicts
    links = []
    hits = []
    d = dict()

    os.chdir(cur_dir)

    #iterate days for selenium
    str_one_day = str(iter_one_day)
    day = ("3/%s/2020"%str_one_day)
    
    #navigate selenium
    options = webdriver.ChromeOptions()     #eric's shit to make it work
    options.add_argument('--ignore- certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chromedriver = dir_path + "/chromedriver"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chrome_options=options, executable_path=chromedriver)

    #driver = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=options)
    
    driver.get(website_url)
    time.sleep(1)
    element = driver.find_element_by_xpath("/html/body/div/div[5]/form/div[2]/div[1]/div[1]/div/div[2]/input[1]")
    element.send_keys("cheap stocks to buy now")
    element.send_keys(Keys.RETURN)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[9]/div[3]/div[3]/div/div/div[1]/div/div/div[2]/a').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[9]/div[3]/div[3]/div/div/div[2]/div/div[2]').click()
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[9]/div[3]/div[3]/div/div/div[2]/div/ul[1]/li[7]/div/span').click()
    time.sleep(1)
    element = driver.find_element_by_xpath("/html/body/div[9]/div[3]/div[3]/div[2]/div[2]/div[3]/form/input[5]")
    element.send_keys(day)
    time.sleep(1)
    element = driver.find_element_by_xpath("/html/body/div[9]/div[3]/div[3]/div[2]/div[2]/div[3]/form/input[6]")
    time.sleep(1)
    element.send_keys(day)
    time.sleep(1)
    element.send_keys(Keys.RETURN)
    time.sleep(1)
    #bs4 html source
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')
    #quit driver
    driver.quit()
    
    print(day)
    
    #soup finding 'regular search results'
    srg = soup.find("div", {"id": "search"})
    for link in srg.findAll('a'):
        links.append(link.get('href'))
    
    #request page source from links
    for individual_link in links:

        if individual_link.startswith('https'):

            #try except to pass on error
            try:
                print(individual_link)
                res = requests.get(individual_link)
                html_page = res.content
                soup = BeautifulSoup(html_page, 'html.parser')
                text = soup.find_all(text=True)

                #remove html jargon
                output = ''
                blacklist = [
                    '[document]',
                    'noscript',
                    'header',
                    'html',
                    'meta',
                    'head', 
                    'input',
                    'script',
                ]
                for t in text:
                    if t.parent.name not in blacklist:
                        output += '{} '.format(t)

                print(output)
                '''
                #write output to temp
                with open('temp.txt', 'w+',newline='\n',encoding='utf-8') as writeFile:
                    #print(output)
                    writeFile.write(output)
                writeFile.close()

                # Weed out blank lines with filter
                #read
                fh = open("temp.txt", "r",encoding="utf-8")
                lines = fh.readlines()
                fh.close()
                lines = filter(lambda x: not x.isspace(), lines)
                # Write
                fh = open("output.txt", "w",encoding="utf-8")
                fh.write("".join(lines))
                fh.close()
                text = open('output.txt','r',encoding='utf-8')

                #iterate through each line
                #search each line
                for line in text:
                    
                    #search for stock group
                    for u in stock_groups:
                        y = re.search(u,line)
                        #if success, then search for all symbols
                        if y:
                            #nasdaq
                            for i in nasdaq_list:

                                x = re.search(i,line)
                                if x:
                                    #count occurences
                                    if i in d:
                                        d[i] = d[i]+1
                                    else:
                                        d[i] = 1
                                else:
                                    pass
                            #amex
                            for i in amex_list:
                                x = re.search(i,line)
                                if x:
                                    #count occurences
                                    if i in d:
                                        d[i] = d[i]+1
                                    else:
                                        d[i] = 1
                                else:
                                    pass
                            #nyse
                            for i in nyse_list:
                                x = re.search(i,line)
                                if x:
                                    #count occurences
                                    if i in d:
                                        d[i] = d[i]+1
                                    else:
                                        d[i] = 1
                                else:
                                    pass
                        else:
                            pass
                
                text.close()
                '''
            except requests.ConnectionError:
                pass
        else:
            pass
    
   #assign title for day and format
    day = ''.join([a for a in day]) \
        .replace("/", ".")
    day = str('%s.csv'%day)

    #write list on temp
    os.chdir("datatables")
    with open(day,'w+',newline='\n',encoding='utf-8') as graphingData:
        for key in list(d.keys()):
            graphingData.write(str(key))
            graphingData.write(", ") 
            graphingData.write(str(d[key]))
            graphingData.write('\n')
    graphingData.close()

    #iter add day
    iter_one_day += 1




    
