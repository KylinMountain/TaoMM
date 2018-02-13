import requests
import json
import re
import pandas as pd
import traceback
import csv

URL = 'https://finance.yahoo.com/quote/AXP/history'
def get_year_stock(stock='AXP'):
    mparams = {'p': stock}
    rep = requests.get(URL, mparams)
    try:
        if rep.status_code == requests.codes.ok:
            patt = '"HistoricalPriceStore":{"prices":(.*),"isPending"'
            m = re.findall(patt, rep.text)
        else:
            rep.raise_for_status()
        if m:
            datas = json.loads(m[0])
            # reverse, from old to new.
            datas = datas[::-1]
            print(datas)

    except Exception as err:
        print(err)
        traceback.print_exc()
    # 去掉那些分页的数据
    return [item for item in datas if 'type' not in item]

if __name__ == '__main__':
    stock = 'AAPL'
    datas = get_year_stock(stock)
    axp_stock = pd.DataFrame(datas)
    # with open('axp_stock.csv', 'w', encoding='utf-8', newline='') as fp:
    #     mwriter = csv.writer(fp, delimiter=',')
    file_prefix = 'axp'
    if stock != '':
        file_prefix = stock;
    axp_stock.to_csv('./' + file_prefix + '_stock.csv', sep=',')