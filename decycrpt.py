import hashlib

"""
解密星图的sign参数
"""

def get_sign(params):
    s = ""
    #params按key排序
    keys = sorted(params.keys())
    for key in keys:
        if key=="recommend":
            value = "recommend"
        else:
            value = params[key]
        s += key + value
    salt = "e39539b8836fb99e1538974d3ac1fe98"
    s += salt

    sign = hashlib.md5(s.encode()).hexdigest()
    return sign


def main():
    params = {
        "o_author_id":"6638478067830358029",
        "platform_source":"1",
        "platform_channel":"1",
        "recommend":"false",
        "service_name":"author.AdStarAuthorService",
        "service_method":"GetAuthorBaseInfo",
    }
    get_sign(params)



if __name__ == '__main__':
    main()