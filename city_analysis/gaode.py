import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd

def get_html():
    resp = requests.get('http://www.autonavi.com/V4.html')
    data = resp.content.decode('utf-8')
    return data


def parse_html(data):
    if data == '' or data is None:
        return
    soup = BeautifulSoup(data, 'lxml')
    data = soup.find_all('ul', class_='county')

    t_list = []
    for item in data[1:]:
        province = str(item.a.string)
        cities = item.find_all('a', class_='active',
                               href=re.compile("http://mapdownload.autonavi.com/mobilemap/mapdatav4/*"))

        for city in cities:
            print(city)
            groups = re.match('(\w+)\((\d+\.\d)M\)', str(city.string))
            city_name = groups[1]
            city_map_size = groups[2]
            t_list.append([city_name, city_map_size, province])

    # zhixia city.
    zhixia = data[0].find_all('a', class_='active',
                              href=re.compile("http://mapdownload.autonavi.com/mobilemap/mapdatav4/*"))
    for city in zhixia[2:6]:
        print(city)
        groups = re.match('(\w+)\((\d+\.\d)M\)', str(city.string))
        city_name = groups[1]
        city_map_size = groups[2]
        t_list.append([city_name, city_map_size, city_name])

    return t_list


def save_to_csv(data):
    if not isinstance(data, list) and len(data) <= 0:
        return

    with open('./city__map_size.csv', 'w', newline='') as fp:
        my_wirter = csv.writer(fp)
        my_wirter.writerow(['city', 'size', 'province'])
        for item in data:
            my_wirter.writerow(item)


def analysis_data():
    df_city = pd.read_csv('./city__map_size.csv', encoding='gbk')


if __name__ == '__main__':
    html = get_html()
    city_list = parse_html(html)
    save_to_csv(city_list)
    # analysis_data()
