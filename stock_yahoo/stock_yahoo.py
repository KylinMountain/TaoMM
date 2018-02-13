import requests
from bs4 import BeautifulSoup
import csv

URL = 'http://money.cnn.com/data/dow30/'


rep = requests.get(URL)

if rep.status_code == 200:
    soup = BeautifulSoup(rep.text, 'lxml')
    names = soup.find_all('td', class_='wsod_firstCol')
    # name.a.string, name.span.string

    others = soup.find_all('td', class_ = 'wsod_aRight')
    prices = others[0::5]
    changes = others[1::5]
    change_pers = others[2::5]
    volumes = others[3::5]
    ytd_changes = others[4::5]
    # prices[0].span.string

    with open('./stock_yahoo.csv', 'w', newline='', encoding='utf-8') as fp:
        mwriter = csv.writer(fp, delimiter=',')
        mwriter.writerow(['company_srt', 'company', 'price', 'change', 'change_per', 'volume', 'ytd_change'])

        for name, price, change, change_per, volume, ytd_change in zip(names, prices, changes, change_pers, volumes, ytd_changes):
            company_srt = name.a.string
            company = name.span.string

            price = price.span.string
            change = change.span.span.string
            change_per = change_per.span.span.string
            volume = volume.string
            ytd_change = ytd_change.span.string

            mwriter.writerow([company_srt, company, price, change, change_per, volume, ytd_change])

