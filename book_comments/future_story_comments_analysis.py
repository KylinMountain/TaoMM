import csv


with open('./future_story.csv', newline='', encoding='utf-8') as fp:
    comments_reader = csv.reader(fp, delimiter=',', quotechar='|')

    stars = 0
    count = 0
    next(comments_reader)
    for row in comments_reader:
        star = row[2]
        print('debug: star: ', star)
        if star == '' or not isinstance(star, str):
            star = '0'
        star = int(star)
        stars += star
        count += 1

    print('总评分：', stars, '平均分： ', stars / count)

