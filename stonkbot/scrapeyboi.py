from bs4 import BeautifulSoup
import requests
import csv


if __name__ == "__main__":
    link = 'https://www.marketbeat.com/market-data/most-volatile-stocks/'
    response = requests.get(link, timeout = 2)
    content = BeautifulSoup(response.content, "html.parser")
    #print(content)
    #table = content.find(class_='scroll-table-wrapper')
    tables = content.findAll("table")[0].findAll("tbody")[0].findAll("tr")
    print(tables)