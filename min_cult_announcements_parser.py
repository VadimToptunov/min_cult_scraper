import json
import re
import requests_html
from bs4 import BeautifulSoup


def write_data_to_json(session, url, last_page):
    with open("min_cult_announcements_data.json", "w") as min_cult_data_file:
        parse_announcements(session, url, min_cult_data_file, last_page)


def get_last_page(soup):
    spans = soup.find_all('a', {'class': 'b-pager__link'})
    match = re.search("\\d{1,4}<", str(spans[-1])).group(0)
    return int(match.strip("<"))


def parse_announcements(session, main_url, json_file, last_page):
    objects = []
    for i in range(1, last_page):
        response = session.get(f'{main_url}?PAGEN_1={i}')
        soup = BeautifulSoup(response.content, 'html.parser')
        for i in soup.find_all('div', {'class': 'b-article__main'}):
            a = i.find_all('a', {'class': 'b-news-list__item'})
            for j in a:
                object = {
                    "url": f'{main_url}{j["href"]}',
                    "date": str(j.find('div', {'class': 'b-article__date'}).text).strip(),
                    "title": str(j.find('div', {'class': 'b-default__title'}).text).strip()
                }
                objects.append(object)
    json.dump(objects, json_file, indent=4, sort_keys=True, ensure_ascii=False)


def get_data():
    url = "https://culture.gov.ru/press/announcement/"
    session = requests_html.HTMLSession()
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    last_page = get_last_page(soup)
    write_data_to_json(session, url, last_page)


if __name__ == "__main__":
    get_data()
