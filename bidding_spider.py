
from urllib import request, parse
from bs4 import BeautifulSoup
from datetime import datetime
import random
import re
import csv


URL = 'https://www.ciac.sh.cn/XmZtbbaWeb/gsqk/ZbjgGkList.aspx'
user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    ]

def get_pages():
    req = request.Request(URL)
    req.add_header('user-agent', random.choice(user_agent_list))
    # 获得某几个固定参数
    with request.urlopen(req) as res:
        print('get pages status:', res.status, res.reason)

        html = res.read()
        view_state, view_state_generator, event_validation = get_valid_params(html)

    # 查询某段时间内的数据
    html = my_request('', '', view_state, view_state_generator, event_validation,
                      txtzbrqbegin='2016-01-01', txtzbrqend=str(datetime.date(datetime.now())))
    # 首页的contract
    print('get pages:', 1)      # 'data: ', html)
    status = get_contract(html)

    # 首页出错, 立刻退出
    if not status:
        print('''There's somthing wrong, please check it manually''')
        return

    # 获取其他页的contract
    page = 2
    while True:
        view_state, view_state_generator, event_validation = get_valid_params(html)
        html = my_request('gvZbjgGkList', 'Page$'+str(page), view_state, view_state_generator, event_validation)
        print('get pages:', page)
        status = get_contract(html)
        if status:
            page = page + 1
        else:
            print('All pages has queried done')
            break


def get_valid_params(html):
    soup = BeautifulSoup(html, 'lxml')
    # pages = soup.find_all(href=re.compile('Page'))[-1].string
    view_state = soup.find_all('input', attrs={'name': '__VIEWSTATE'})[0]['value']
    event_validation = soup.find_all('input', attrs={'name': '__EVENTVALIDATION'})[0]['value']
    view_state_generator = soup.find_all('input', attrs={'name': '__VIEWSTATEGENERATOR'})[0]['value']
    return view_state, view_state_generator, event_validation


def get_contract(html):
    # 获取当前页的数据
    soup = BeautifulSoup(html, 'lxml')

    # 执行出错
    if soup.form['action'] == '../ErrMsg.aspx':
        return False

    info = soup.find_all('a', id=re.compile('gvZbjgGkList*'))
    view_state, view_state_generator, event_validation = get_valid_params(html)
    for contract in info:
        c_id = contract['href'].split('\'')[1]
        html = my_request(c_id, '', view_state, view_state_generator, event_validation)
        # print('contract data\n', html)
        parse_save_contract(html)
    # 执行成功
    return True


def parse_save_contract(html):
    soup = BeautifulSoup(html, 'lxml')
    project_name = soup.find_all('span', attrs={'classatt': 'tab_zbb_ybs_zbjg_gk.xmmc'})[0].string
    bidding_type = soup.find_all('span', attrs={'classatt': 'tab_zbb_ybs_zbjg_gk.zblx'})[0].string
    bidding_winner = soup.find_all('span', attrs={'classatt': 'tab_zbb_ybs_zbjg_gk.zbdw'})[0].string
    bidding_date = soup.find_all('span', attrs={'classatt': 'tab_zbb_ybs_zbjg_gk.zbrq'})[0].string
    bidding_cost = soup.find_all('span', attrs={'classatt': 'tab_zbb_ybs_zbjg_gk.zbj'})[0].string

    # 我们可以过滤一下，project name，如果包含公租房，或者其他需要的字段再存储，否则跳过。
    print(project_name, bidding_type, bidding_winner, bidding_date, bidding_cost)

    if str(project_name).rfind('公租房') >= 0:
        csv_writer.writerow([bidding_date, project_name, bidding_type, bidding_winner, bidding_cost])
    else:
        return


# it could be used to open contract, and open next page if we fill different params
def my_request(target, argument, viewstate, viewstategenerator, eventvalidation,
               ddlzblx='', txtzbrqbegin='', txtzbrqend='', txtzbr='', url = URL):
    params = {'__EVENTTARGET': target, '__EVENTARGUMENT': argument, '__VIEWSTATE': viewstate,
              '__VIEWSTATEGENERATOR': viewstategenerator, '__EVENTVALIDATION': eventvalidation,
              'ddlZblx':ddlzblx, 'txtZbrqBegin':txtzbrqbegin, 'txtZbrqEnd':txtzbrqend, 'txtZbr': txtzbr}
    data = parse.urlencode(params)

    req = request.Request(url)
    print(data)
    req.add_header('User-Agent', random.choice(user_agent_list))
    with request.urlopen(req, data=data.encode('utf-8')) as res:
        print('my_request: ', res.status, res.reason)
        if res.status == 200:
            html = res.read().decode('utf-8')
            return html

        # 看起来我们不需要手动处理HTTP 302这种，文件位置移动的case
        # elif res.status == 302:
        #     path = res.getheaders()['Location']
        #     return bytes.decode(path)


def init_csv():
    mcsv_file = open('./gzf_zb/gzf_zb.csv', 'w', newline='')
    mwriter = csv.writer(mcsv_file)
    file_header = ['中标日期', '项目名称', '招标类型', '中标单位', '中标价格']
    mwriter.writerow(file_header)
    return mwriter, mcsv_file

# 主程序入口
if __name__ == '__main__':
    start = datetime.now();
    csv_writer, csv_file_f = init_csv()
    get_pages()
    csv_file_f.close()
    print('程序耗时：', str(datetime.now() - start))
