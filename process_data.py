import json
import os
import requests
from xt_decode import cookie_global
import time

"""
用来处理随时需要的一些临时数据
"""

def process_xt_car_talent():
    """
    处理要增加到系统中的50个汽车类别的达人
    :return:
    """
    car_nick_name_list = []
    with open('data/xt_car_talent_50.json') as f:
        json_obj = json.loads(f.read())
        stars = json_obj.get('stars')
        for i in range(len(stars)):
            car_nick_name_list.append(stars[i].get('nick_name'))
            print(stars[i].get('nick_name'))
        print(car_nick_name_list)

def prepare_fans_data():
    """
    处理500个汽车达人的粉丝数据，并准备好数据计算假粉率
    :return:
    """
    file_dir = '/Users/liuliujie/douyin/car_500_data/data/fans_data/'
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if 'json' not in file:
                continue
            with open(file_dir + file, 'r', encoding='utf-8') as input_file:
                json_obj = json.loads(input_file.read())
                # print(json_obj)
                uid = file.split('.')[0]
                with open('./cal_fake_fans/临时数据/fans_' + str(uid) + '.txt', 'a+', encoding='utf-8') as f:
                    index = 0
                    for key in json_obj.keys():
                        try:
                            # print(key)
                            # 获取假粉判别所需要的数据
                            temp_list = [str(index)]
                            index += 1
                            # 结果全部预设为0
                            temp_list.append('0')
                            nick_name = json_obj.get(key).get('nick_name').replace(',', '').replace('"','').replace('\'','')
                            temp_list.append(str(nick_name))
                            like = json_obj.get(key).get('like')
                            temp_list.append(str(like))
                            follow_count = json_obj.get(key).get('follow_count')
                            temp_list.append(str(follow_count))
                            fans = json_obj.get(key).get('fans')
                            temp_list.append(str(fans))
                            work = json_obj.get(key).get('work')
                            temp_list.append(str(work))
                            dongtai = 1
                            temp_list.append(str(dongtai))
                            love = json_obj.get(key).get('love')
                            temp_list.append(str(love))
                            description = json_obj.get(key).get('describe').replace(',', '').replace('"','').replace('\'','')
                            description_flag = '0' if description == '' else '1'
                            temp_list.append(description_flag)
                            temp_list.append(str(description))

                            for i in range(3, 9):
                                if 'w' in temp_list[i]:
                                    temp_list[i] = str(int(float(temp_list[i][:-1])*10000))
                                if temp_list[i] == '':
                                    temp_list[i] = '0'

                            f.write(','.join(temp_list) + '\n')
                        except:
                            continue

            # print(file)
            print('finished scrawl data of ' + str(uid))


def get_car_talent_info_one_page(page):
    """
    获取星图上所有汽车类别达人的信息(一页)
    2020.7.3 liujie
    :return:
    """
    url = "https://star.toutiao.com/v/api/demand/author_list/"
    param = {
    'limit': 20,
    'need_detail': 'true',
    'page': page,
    'platform_source': 1,
    'task_category': 1,
    'tag': 31,
    'order_by': 'score',
    'disable_replace_keyword': 'false'
    }
    hearder = {
        'Host': 'star.toutiao.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'X-CSRFToken': 'fAojBqYYDpDtta7uyvbdEmL9BFksQH0g',
        'Connection': 'keep-alive',
        'Referer': 'https://star.toutiao.com/ad',
        'cookie': cookie_global,
        'TE': 'Trailers'
    }
    response = requests.get(url, params=param, headers=hearder)
    response = json.loads(response.text.replace(r'\\u', r'\u'))
    print(response)

    # 组装数据
    page = response.get('data').get('pagination').get('page')
    next_page_flag = response.get('data').get('pagination').get('has_more')
    authors = response.get('data').get('authors')
    with open('./data/xt_car_talent_all.txt', 'a+', encoding='utf-8') as f:
        for i in range(len(authors)):
            # 顺序是预计播放量、粉丝、平均播放量、星图id、城市、预计cpm、下单数量、昵称、头像地址、抖音号
            temp_list = []

            expected_play_num = authors[i].get('expected_play_num')
            temp_list.append(str(expected_play_num))
            follower = authors[i].get('follower')
            temp_list.append(str(follower))
            avg_play = authors[i].get('avg_play')
            temp_list.append(str(avg_play))
            id = authors[i].get('id')
            temp_list.append(str(id))
            city = authors[i].get('city')
            temp_list.append(str(city))
            expected_cpm = authors[i].get('expected_cpm')
            temp_list.append(str(expected_cpm))
            order_cnt = authors[i].get('order_cnt')
            temp_list.append(str(order_cnt))
            nick_name = authors[i].get('nick_name')
            temp_list.append(str(nick_name))
            avatar_url = authors[i].get('avartar_url')
            temp_list.append(str(avatar_url))
            unique_id = authors[i].get('unique_id')
            temp_list.append(str(unique_id))

            f.write(','.join(temp_list)+'\n')

    if next_page_flag == True:
        return int(page) + 1
    else:
        return 0

def get_all_car_talent_info():
    """
    # 爬取星图上目前所有的汽车达人信息
    :return:
    """
    flag = 1
    while flag != 0:
        flag = get_car_talent_info_one_page(flag)
        print('finished ' + str(flag-1) + ' page')
        time.sleep(1)
    print('finished all car talent info in star toutiao!')




if __name__ == '__main__':
    process_xt_car_talent()
    # prepare_fans_data()
    # get_all_car_talent_info()



