
import requests
from bs4 import BeautifulSoup
import csv
import time
import re
import traceback

URL = 'https://book.douban.com/subject/26943161/comments/new'

# ?p=2


def get_html():
    try:
        page = 1
        user_agent = {'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

        while True:
            if page == 1:
                mparams = ''
            else:
                mparams = {'p': str(page)}
            res = requests.get(URL, params=mparams, headers=user_agent)
            print('kylin url is ', res.url)
            if res.status_code == requests.codes.ok:
                parse_comments(res.text)
            else:
                res.raise_for_status()
            page += 1
            time.sleep(5)

            if page >= 249:
                break
    except Exception as err:
        print('kylin error', err)
        traceback.print_exc()


def parse_comments(html):
    soup = BeautifulSoup(html, 'lxml')
    comment_full = soup.find_all('li', 'comment-item')

    username_pattern = re.compile('.*')
    dates_pattern = re.compile('[\d|-]{5,10}')

    for user_comment in comment_full:
        user = user_comment.find_all('a', title=username_pattern)
        if len(user) > 0:
            user = user[0]['title']
        else:
            user = ''

        comment = user_comment.find_all('p', 'comment-content')
        if len(comment) > 0:
            comment = comment[0].string
            comment = ''.join([x for x in comment if x not in '\n !'])
            comment.replace(',', '，')
        else:
            comment = ''

        votes = user_comment.find_all('span', 'vote-count')
        if len(votes) > 0:
            votes = int(votes[0].string)
        else:
            votes = 0

        stars = user_comment.find_all('span', class_='user-stars')
        if len(stars) > 0:
            stars = stars[0]['class'][1].split('allstar')[1]
        else:
            stars = 0
        stars = int(stars) // 10

        dates = user_comment.find_all('span', text=dates_pattern)
        if len(dates) > 0:
            dates = dates[0].string
        else:
            dates = ''

        print("write row : ", user, votes, stars, dates, comment)
        csv_writer.writerow([user, votes, stars, dates, comment])


def init_csv():
    file = open('./future_story.csv', 'w', encoding='utf-8', newline='')
    mwriter = csv.writer(file, delimiter=',')
    file_header = ['user', 'vote', 'star', 'date', 'comments']
    mwriter.writerow(file_header)
    return mwriter, file


if __name__ == '__main__':
    csv_writer, csv_file = init_csv()
    get_html()
    csv_file.close()