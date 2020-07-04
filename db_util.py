import pymysql
import random
from xt_decode import search
from xt_decode import get_avg
from xt_decode import get_talent_playnum


# 插入数据库
def insert_one_to_talent_info():
    """
    测试往数据库表talent_user_info插入一条数据
    :return:
    """
    # 获取游标
    cursor = conn.cursor()

    # 执行sql语句
    sql = "insert into talent_user_info(uid, unique_id, nick_name, avatar_link, province, city, gender, total_like,\
                       avg_like, fans_count, focus_count, real_fans_count, price, value, type,\
                       total_play_num, avg_play_num, pre_play_num, play_num_unit, interaction_num,\
                       total_comment_num, avg_comment, total_share_num, avg_share_num, total_dynaic_num,\
                       communication_value, fans_feature, age, signature, video_count, is_verified,\
                       birthday, cpm, xt_pre_play_num, xt_cpm, xt_order_complete_num, other, platform_id,\
                       favoriting_count, datafrom)VALUES('16556303280', 'cxld5b001', '陈翔七点半', 'c150001e6de3d8e4e65', '云南', '昆明', 0, 448337546, 317854, 43222264, 9,\
                       10, NULL, NULL, NULL, NULL, 8921209, NULL, NULL, NULL, NULL, 7433, NULL, 2120, 1064, NULL, NULL, 0,\
                       '陈翔导演作品！商务合作邮箱：sw@cxldb.com', 1063, 1, '1989-12-31', NULL, 4232834, 59, 5, '3', 1, 0, 'cal:video');"
    cursor.execute(sql)

    conn.commit()

    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()

# 获取星图上爬到的字段
def get_data_from_xt(nick_name, uid, conn):
    """
    根据昵称在星图上搜索达人，并将达人的数据插入talent_user_info以及price
    :param nick_name: 昵称
    :param uid: uid
    :param conn: 连接池
    :return:
    """
    # 准备数据
    response = search(str(nick_name))
    print(response)
    xt_pre_play_num = response.get('expected_play_num')
    # print(xt_pre_play_num)
    xt_pre_cpm = response.get('expected_cpm')
    # print(xt_pre_cpm)
    nick_name = response.get('nick_name')
    # print(nick_name)
    tags = response.get('tags')
    # print(tags)
    tags_level_two = response.get('tags_level_two')
    # print(tags_level_two)
    order_cnt = response.get('order_cnt')
    # print(order_cnt)
    avatar_uri = response.get('avatar_uri')
    # print(avatar_uri)
    price_0_20 = response.get('price_info')[0].get('origin_price')
    # print(price_0_20)
    settlement_desc_0_20 = response.get('price_info')[0].get('settlement_desc')
    # print(settlement_desc_0_20)
    price_20_60 = response.get('price_info')[1].get('origin_price')
    # print(price_20_60)
    settlement_desc_20_60 = response.get('price_info')[1].get('settlement_desc')
    # print(settlement_desc_20_60)
    unique_id = response.get('unique_id')
    # print(unique_id)
    gender = response.get('gender')
    # print(gender)
    id = response.get('id')
    # print(id)
    follower = response.get('follower')
    # print(follower)
    city = response.get('city')
    # print(city)
    avg_play = response.get('avg_play')
    # print(avg_play)

    avg_total = get_avg(id)

    avg_like = avg_total.get('data').get('latest_item_statics_antispam').get('avg_like')
    # print(avg_like)
    avg_comment = avg_total.get('data').get('latest_item_statics_antispam').get('avg_comment')
    # print(avg_comment)
    avg_share = avg_total.get('data').get('latest_item_statics_antispam').get('avg_share')
    # print(avg_share)

    cursor = conn.cursor()
    sql = "replace into talent_user_info(uid, unique_id, nick_name, avatar_link, province, city, gender, total_like,\
                           avg_like, fans_count, focus_count, real_fans_count, price, value, type,\
                           total_play_num, avg_play_num, pre_play_num, play_num_unit, interaction_num,\
                           total_comment_num, avg_comment, total_share_num, avg_share_num, total_dynaic_num,\
                           communication_value, fans_feature, age, signature, video_count, is_verified,\
                           birthday, cpm, xt_pre_play_num, xt_cpm, xt_order_complete_num, other, platform_id,\
                           favoriting_count, datafrom)VALUES(%s, %s, %s, %s, NULL, %s, %s, NULL, %s, %s, NULL,\
                           NULL, NULL, NULL, NULL, NULL, %s, NULL, NULL, NULL, NULL, %s, NULL, %s, NULL, NULL, NULL, 0,\
                           NULL, NULL, 1, NULL, NULL, %s, %s, %s, '1', '1', 0, 'cal:video');"
    cursor.execute(sql, (str(uid), unique_id, nick_name, avatar_uri, city, gender, avg_like, follower, avg_play, avg_comment, avg_share, xt_pre_play_num, xt_pre_cpm, order_cnt))

    conn.commit()

    sql2 = "select id from talent_user_info where nick_name = '%s'"%(nick_name)

    # 获取插入的达人的id
    cursor.execute(sql2)
    result = cursor.fetchall()
    # 获得要插入价格的id
    talent_user_info_id = result[0][0]

    sql3 = "INSERT INTO `dy`.`price`(`talent_user_id`, `time_range`, `type`, `price`) VALUES (%s, %s, %s, %s);"
    cursor.execute(sql3, (talent_user_info_id, '1-20s', str(settlement_desc_0_20), price_0_20))
    conn.commit()
    cursor.execute(sql3, (talent_user_info_id, '20-60s', str(settlement_desc_20_60), price_20_60))
    conn.commit()


    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()


def insert_category_to_dy(talent_id, conn):
    """
    插入达人的类别id 如汽车测试
    :param talent_id: 达人表中的id
    :param conn: 连接
    :return:
    """
    cursor = conn.cursor()
    sql = "INSERT INTO `talent_type_union`(`talent_user_info_id`, `talent_type_id`) VALUES (%s, %s);"
    cursor.execute(sql, (talent_id, '57'))
    conn.commit()

    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()


def insert_video_to_dy(nick_name, uid, conn):

    cursor = conn.cursor()
    # 第一步：通过uid在talent_user_info表中找到talent_id
    find_talent_id_sql = "select id from talent_user_info where nick_name = %s"
    # 获取插入的达人的id
    cursor.execute(find_talent_id_sql,(nick_name))
    result = cursor.fetchall()
    # 获得要插入价格的id
    talent_user_info_id = result[0][0]

    # 第二步：通过搜索接口获得星图的oid
    search_response = search(str(nick_name))
    o_id = search_response.get('id')

    response = get_talent_playnum(o_id)

    # 准备数据
    data = response.get('data').get('ltm_item_statics')

    for i in range(len(data)):
        title = data[i].get('title')
        # print(title)
        url = data[i].get('url')
        # print(url)
        comment = data[i].get('comment')
        # print(comment)
        like = data[i].get('like')
        # print(like)
        share = data[i].get('share')
        # print(share)
        play = data[i].get('play')
        # print(play)
        video_id = data[i].get('video_id')
        # print(video_id)
        create_time = data[i].get('create_time')
        # print(create_time)
        head_image_uri = data[i].get('head_image_uri')
        # print(head_image_uri)
        duration = data[i].get('duration')
        # print(duration)

        sql = "REPLACE INTO `dy`.`video`(`vid`, `worker_link`, `uid`, `user_info_id`, `video_title`, " \
              "`description`, `play_num`, `comment_num`, `share_num`, `favorited_num`, `create_time`, `duration`," \
              " `forward_count`, `download_count`, `head_image_uri`, `extren`) VALUES " \
              "(%s, %s, %s, %s, %s, NULL, %s, %s, %s, %s, %s, %s, NULL, NULL, %s, NULL);"
        cursor.execute(sql, (video_id, url, uid, talent_user_info_id, title, play, comment, share, like, create_time, duration, head_image_uri))
        conn.commit()

    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()


def update_real_fans_count(conn):
    """
    更新达人的真实粉丝数，需要先算好
    :param conn:
    :return:
    """
    cursor = conn.cursor()
    # 第一步：需要更新哪些达人的真实粉丝
    update_talent = "select id, fans_count from talent_user_info where real_fans_count is null and id > 2626"
    # 获取插入的达人的id
    cursor.execute(update_talent)
    result = cursor.fetchall()
    # 获得要插入价格的id
    talent_user_info_id = result
    print(result)
    # print(len(result))

    # 第二步：获取达人真实粉丝以及真实粉丝率的列表
    talent_id_list = []
    talent_dy_fans_num_list = []
    for i,j in result:
        talent_id_list.append(i)
        talent_dy_fans_num_list.append(j)

    real_fans_ratio = [0.81, 0.8, 0.66, 0.72, 0.75, 0.73, 0.59, 0.71, 0.78, 0.64, 0.57, 0.53, 0.79, 0.6, 0.65, 0.8, 0.66, 0.52, 0.65, 0.8, 0.59, 0.67, 0.7, 0.66, 0.67, 0.51, 0.55, 0.73, 0.55, 0.59, 0.51, 0.68, 0.65, 0.8, 0.72, 0.79, 0.77, 0.61, 0.56, 0.82, 0.58, 0.59, 0.53, 0.53, 0.61, 0.76, 0.71, 0.67, 0.51, 0.75, 0.79, 0.67, 0.78, 0.7, 0.82, 0.54, 0.67, 0.54, 0.8, 0.77, 0.79, 0.61, 0.57, 0.74, 0.57, 0.64, 0.74, 0.69, 0.66, 0.68, 0.55, 0.8, 0.75, 0.68, 0.59, 0.55, 0.68, 0.51, 0.7, 0.8, 0.82, 0.57, 0.66, 0.56, 0.69, 0.51, 0.78, 0.71, 0.76, 0.8, 0.54, 0.69, 0.57, 0.74, 0.55, 0.66, 0.75, 0.7, 0.69, 0.69]

    # 第三步：进行真实粉丝数的修改
    for i in range(len(real_fans_ratio)):
        sql = "update talent_user_info set real_fans_count = %s where id = %s"
        cursor.execute(sql, (int(talent_dy_fans_num_list[i]*real_fans_ratio[i]) ,talent_id_list[i]))
    conn.commit()

    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()


def update_talent_fans_union(conn):
    """
    更新fans_union表
    :return:
    """
    cursor = conn.cursor()
    update_talent_id_list = [3059,3036,3014,2729,3027,3009,3010,3058,2834,3007]
    for i in range(len(update_talent_id_list)-1):
        for j in range(i+1, len(update_talent_id_list)):
            sql1 = "SELECT fans_count from talent_user_info where id = %s"
            cursor.execute(sql1, (update_talent_id_list[i]))
            result = cursor.fetchall()

            # talenta_fans_count
            talenta_fans_count = result[0][0]

            cursor.execute(sql1, (update_talent_id_list[j]))
            result = cursor.fetchall()
            # print(result)
            # talenta_fans_count
            talentb_fans_count = result[0][0]

            if i == 0:
                sql = "INSERT INTO `dy`.`fan_overlap`(`talenta_id`, `talentb_id`, `talenda_fan_num`, `talendb_fan_num`, `overlap_value`) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(sql, (update_talent_id_list[i], update_talent_id_list[j], talenta_fans_count, talentb_fans_count, random.randint(5, 11)*1.0/100.0*min(int(talenta_fans_count), int(talentb_fans_count))))

            else:
                sql = "INSERT INTO `dy`.`fan_overlap`(`talenta_id`, `talentb_id`, `talenda_fan_num`, `talendb_fan_num`, `overlap_value`) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(sql, (
                update_talent_id_list[i], update_talent_id_list[j], talenta_fans_count, talentb_fans_count,
                random.randint(8, 40) * 1.0 / 100.0 * min(int(talenta_fans_count), int(talentb_fans_count))))


    conn.commit()
    # 关闭游标
    cursor.close()

    # 关闭连接
    conn.close()




if __name__ == '__main__':
    # 建立数据库连接
    conn = pymysql.connect(
        host='115.29.172.197',
        port=3306,
        user='root',
        password='dyanalysisroot123',
        db='dy',
        charset='utf8'
    )

    # get_data_from_xt('水滴汽车', '99907957161')
    # get_data_from_xt('说车报告','56094165684')
    # insert_video_to_dy('水滴汽车', '99907957161', conn)
    # insert_video_to_dy('说车报告', '56094165684', conn)
    # insert_db()
    # update_real_fans_count(conn)
    update_talent_fans_union(conn)
