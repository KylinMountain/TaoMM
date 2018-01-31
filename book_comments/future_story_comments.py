
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
        while True:
            if page == 1:
                mparams = ''
            else:
                mparams = {'p': str(page)}
            res = requests.get(URL, params=mparams)
            print('kylin url is ', res.url)
            if res.status_code == 200:
                parse_comments(res.text)
            page += 1
            time.sleep(4)

            if page >= 249:
                break
    except Exception as err:
        print('kylin error', err)
        traceback.print_exc()


def parse_comments(html):
    soup = BeautifulSoup(html, 'lxml')
    comment_full = soup.find_all('li', 'comment-item')
    for user_comment in comment_full:
        user = user_comment.find_all('a', title=re.compile('.*'))
        if len(user) > 0:
            user = user[0]['title']
        else:
            user = ''

        comment = user_comment.find_all('p', 'comment-content')
        if len(comment) > 0:
            comment = comment[0].string
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

        dates = user_comment.find_all('span', text=re.compile('[\d|-]{5,10}'))
        if len(dates) > 0:
            dates = dates[0].string
        else:
            dates = ''

        print("write row : ", user, votes, stars, dates, comment)
        csv_writer.writerow([user, votes, stars, dates, comment])


def init_csv():
    file = open('./future_story.csv', 'w', encoding='utf-8', newline='')
    mwriter = csv.writer(file)
    file_header = ['user', 'vote', 'star', 'date', 'comments']
    mwriter.writerow(file_header)
    return mwriter, file


if __name__ == '__main__':
    csv_writer, csv_file = init_csv()
    get_html()
    csv_file.close()