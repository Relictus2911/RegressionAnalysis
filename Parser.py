import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_links(html):
    soup = BeautifulSoup()
    soup = BeautifulSoup(html, 'lxml')

    elements = soup.find_all("div", class_="entry_footer entry_footer--short l-pt-16 l-pb-16 lm-pt-12 lm-pb-14")
    links = []
    for elem in elements:
        links.append( elem.find("div", class_="favorite_marker__count").text)
    return links

def get_info(html):
    soup = BeautifulSoup(html,'lxml')
    date = soup.find("div", class_="finance-currency-plate__col--date").find("div",class_="finance-currency-plate__value").text
    name = soup.find("h1", class_="finance__header").text
    value = soup.find("div",class_="finance-currency-plate__col--value-tomorrow").find("div", class_="finance-currency-plate__currency").text
    result ={'date': date, 'name': name, 'value': value}
    return  result

def write_in_file(i,result):
    with open('result.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((result['date'],
                         result['name'],
                         result['value']))
        print(i,result['name'],'bla')

url = 'https://dtf.ru/u/3792-artemiy-leonov'
print(requests.get(url).text)
all_links = get_links(get_html(url))
for i,link  in enumerate(all_links):
    #print(i)
    #sleep(2)
    write_in_file(i,get_info( get_html(link)))


