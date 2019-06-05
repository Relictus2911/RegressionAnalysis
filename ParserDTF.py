import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv


def get_full_page(link):
    driver = webdriver.Chrome("chromedriver")
    driver.get(link)
    i=0
    pause_time = 3
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        if i == 1000:
            break
        i+=1
    time.sleep(pause_time)
    soup = BeautifulSoup(driver.page_source, "lxml")
    return soup


def get_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_text_size(html):
    elements = html.find_all("a", class_="entry_content__link")
    text_size = []
    pause_time = 60
    i = 0
    for elem in elements:
        if i % 500 == 0:
            time.sleep(pause_time)
        i += 1
        new_html = get_html(elem.get('href'))
        try:
            texts = new_html.find("div", class_="b-article").find_all('p')
            text_length = 0
            for text in texts:
                text_length += len(str(text))
        except AttributeError:
            text_length = 0
        text_size.append(text_length)
    return text_size


def get_variables(html):
    elements = html.find_all("div", class_="entry_footer entry_footer--short l-pt-16 l-pb-16 lm-pt-12 lm-pb-14")
    all_variables = []
    text_size = get_text_size(html)
    i = 0
    for elem in elements:
        try:
            likes = elem.find("span", class_="vote__value__v vote__value__v--real").text
            likes = likes.replace(" ", '')
            likes = int(likes)
        except ValueError:
            likes = 0
        try:
            comments = elem.find("span", class_="comments_counter__count__value l-inline-block l-va-middle").text
            comments = comments.replace(" ", '')
        except AttributeError:
            comments = 0
        try:
            favorite = elem.find("div", class_="favorite_marker__count").text
            favorite = favorite.replace(" ", '')
        except AttributeError:
            favorite = 0
        result = {'likes': likes, 'comments': comments, 'favorite': favorite, 'size': text_size[i]}
        i += 1
        all_variables.append(result)
    return all_variables


def write_to_file(variables):
    i = 0;
    name_of_rows = {1: 'likes', 2: 'coms', 3: 'favs', 4: 'size'}
    for variable in variables:
        with open('main.tsv', 'a') as f:
            writer = csv.writer(f, delimiter='\t')
            if i == 0:
                writer.writerow((name_of_rows[1],
                                 name_of_rows[2],
                                 name_of_rows[3],
                                 name_of_rows[4]))
                i = 1
            writer.writerow((variable['likes'],
                             variable['comments'],
                             variable['favorite'],
                             variable['size']))
            # print(variable['likes'], variable['comments'], variable['favorite'], variable['size'])

link = 'https://dtf.ru'
#link = 'https://dtf.ru/u/3351-vadim-elistratov'
# link = 'https://dtf.ru/u/10527-semen-kostin'
page = get_full_page(link)
write_to_file(get_variables(page))
