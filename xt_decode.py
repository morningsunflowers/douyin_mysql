import requests
import json
import time
from decycrpt import get_sign

# 由于只有一个账号，cookie时限的原因，定义全局的cookie
cookie_global = 'csrftoken=fAojBqYYDpDtta7uyvbdEmL9BFksQH0g; tt_webid=6844538766415447559; gftoken=MTcyMjQ1MTMxM3wxNTkzNjE4MzgxOTJ8fDAGBgYGBgY; gr_user_id=157a5576-f9a4-4b60-ba11-9c757256a191; grwng_uid=3cea4078-6734-4c60-8c99-8e93bed751a4; s_v_web_id=kc3j8q4s_9uqYRGKK_Bija_4SpH_89SO_rakswLIAPHem; 8632e941eb705978_gr_session_id=19ecd31a-4d68-4f31-a554-28b849d062bb; 8632e941eb705978_gr_session_id_0dff46d7-34d5-4706-bd73-8d6208a362e6=true; star_sessionid=724a724fffec37f53eed1b646789423f; SLARDAR_WEB_ID=6707515503771910155'


def search(key):
    """
    搜索星图上的达人
    :param key: 关键字/词
    :return: 找到的符合条件的达人列表（找不到即为空）
    """
    url = "https://star.toutiao.com/v/api/demand/author_list/?limit=20&need_detail=true&page=1&platform_source=1&key="+str(key)+"&task_category=1&order_by=score&disable_replace_keyword=false&only_nick_name=true"

    header = {
    'authority': 'star.toutiao.com',
    'method': 'GET',
    'path': '/v/api/demand/author_list/?limit=20&need_detail=true&page=1&platform_source=1&key=%E6%9C%B1%E4%B8%80%E6%97%A6&task_category=1&order_by=score&disable_replace_keyword=false&only_nick_name=true',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': cookie_global,
    'referer': 'https://star.toutiao.com/ad',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'x-csrftoken': 'Qd9y6Y6niAqE5hENmcxaNn7JYwDR9T3D'
    }

    # 换成json就不会有Unicode编码了
    response = requests.get(url, headers=header).text.replace(r'\\u', r'\u')
    # print(response)
    # print(type(response))

    return json.loads(response).get('data').get('authors')[0]


def get_talent_playnum(o_id):
    """
    获得星图上达人最近15个视频的播放量等信息
    :param o_id: 传入的用户id
    :return: 最近15个视频的播放量
    """
    # url = "https://star.toutiao.com/h/api/gateway/handler_get/?o_author_id=6702544657877827598&platform_source=1&platform_channel=1&limit=15&service_name=author.AdStarAuthorService&service_method=GetAuthorLatestItems&sign=588909f69daf10ef448e594f0c7009e9"
    url = "https://star.toutiao.com/h/api/gateway/handler_get/"
    params = {
        "o_author_id":str(o_id),
        "platform_source":"1",
        "platform_channel":"1",
        "limit": '15',
        # "recommend":"false",
        "service_name":"author.AdStarAuthorService",
        "service_method":"GetAuthorLatestItems",
    }
    sign = get_sign(params)
    params.update({
        'sign': sign
    })
    # print(params)

    header = {
    'authority': 'star.toutiao.com',
    'method': 'GET',
    'path': '/h/api/gateway/handler_get/?o_author_id='+str(o_id)+'&platform_source=1&platform_channel=1&limit=15&service_name=author.AdStarAuthorService&service_method=GetAuthorLatestItems&sign='+str(sign),
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip,deflate,br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': cookie_global,
    'referer': 'https://star.toutiao.com/ad',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'x-csrftoken': 'Qd9y6Y6niAqE5hENmcxaNn7JYwDR9T3D',
    'x-star-service-method': 'GetAuthorLatestItems',
    'x-star-service-name': 'author.AdStarAuthorService'
    }
    response = requests.get(url, headers=header, params=params).text
    # print(json.loads(response))
    return json.loads(response)


def get_talent_fanschange_num(o_id):
    """
    获得达人近三个月的粉丝变化情况，日期需要自己修改，上线之后可以直接从抖音获取
    :param o_id: 用户id
    :return: 粉丝变化列表json
    """
    url = "https://star.toutiao.com/h/api/gateway/handler_get/"
    params = {
        "o_author_id":str(o_id),
        "platform_source":"1",
        "platform_channel":"1",
        "author_type": '1',
        'start_date':'2020-04-01',
        'end_date': '2020-07-01',
        "service_name":"data.AdStarDataService",
        "service_method":"GetAuthorDailyFansV2",
    }
    sign = get_sign(params)
    params.update({
        'sign': sign
    })
    print(params)

    header = {
    'authority': 'star.toutiao.com',
    'method': 'GET',
    'path': '/h/api/gateway/handler_get/?o_author_id='+str(o_id)+'&platform_source=1&platform_channel=1&author_type=1&start_date=2020-04-01&end_date=2020-07-01&service_name=data.AdStarDataService&service_method=GetAuthorDailyFansV2&sign='+str(sign),
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip,deflate,br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': cookie_global,
    'referer': 'https://star.toutiao.com/ad',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'x-csrftoken': 'Qd9y6Y6niAqE5hENmcxaNn7JYwDR9T3D',
    'x-star-service-method': 'GetAuthorLatestItems',
    'x-star-service-name': 'author.AdStarAuthorService'
    }
    response = requests.get(url, headers=header, params=params).text
    print(json.loads(response))


def get_talent_ad_price(o_id):
    """
    获得达人的视频推广价格
    :param o_id: 达人id
    :return: 达人的两种视频价格 0-20s以及60s
    """
    url = "https://star.toutiao.com/h/api/gateway/handler_get/"
    params = {
        "o_author_id":str(o_id),
        "platform_source":"1",
        "platform_channel":"1",
        "author_type": '1',
        "service_name":"author.AdStarAuthorService",
        "service_method":"GetAuthorMarketingInfo",
    }
    sign = get_sign(params)
    params.update({
        'sign': sign
    })
    print(params)

    header = {
    'authority': 'star.toutiao.com',
    'method': 'GET',
    'path': '/h/api/gateway/handler_get/?o_author_id='+str(o_id)+'&platform_source=1&platform_channel=1&service_name=author.AdStarAuthorService&service_method=GetAuthorMarketingInfo&sign='+str(sign),
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip,deflate,br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': cookie_global,
    'referer': 'https://star.toutiao.com/ad',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'x-csrftoken': 'Qd9y6Y6niAqE5hENmcxaNn7JYwDR9T3D',
    'x-star-service-method': 'GetAuthorMarketingInfo',
    'x-star-service-name': 'author.AdStarAuthorService'
    }
    response = requests.get(url, headers=header, params=params).text
    print(json.loads(response))


def get_avg(o_id):
    """
    获得达人的平均点赞、转发以及评论
    :param o_id: 达人id
    :return: 达人的平均点赞、转发以及评论
    """
    url = "https://star.toutiao.com/h/api/gateway/handler_get/"
    params = {
        "o_author_id":str(o_id),
        "platform_source":"1",
        "platform_channel":"1",
        "service_name":"author.AdStarAuthorService",
        "service_method":"GetAuthorShowItems",
    }
    sign = get_sign(params)
    params.update({
        'sign': sign
    })
    # print(params)

    header = {
    'authority': 'star.toutiao.com',
    'method': 'GET',
    'path': '/h/api/gateway/handler_get/?o_author_id='+str(o_id)+'&platform_source=1&platform_channel=1&service_name=author.AdStarAuthorService&service_method=GetAuthorShowItems&sign='+sign,
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip,deflate,br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': cookie_global,
    'referer': 'https://star.toutiao.com/ad',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'x-csrftoken': 'Qd9y6Y6niAqE5hENmcxaNn7JYwDR9T3D',
    'x-star-service-method': 'GetAuthorShowItems',
    'x-star-service-name': 'author.AdStarAuthorService'
    }
    response = requests.get(url, headers=header, params=params).text
    return json.loads(response)



if __name__ == '__main__':
    # ans = search('八戒')
    # print(ans)
    # get_avg(6629723437017333768)
    get_talent_playnum(6629723437017333768)
    # get_talent_fanschange_num(6629723437017333768)
    # for i in range(50):
    #     print(i)
    #     get_talent_ad_price(6629723437017333768)
    #     time.sleep(1.5)

