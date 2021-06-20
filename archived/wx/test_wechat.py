import requests
import json
import threading

# 字典all_users用于存储 由 索引名和openID构成的键值对
# 微信关注‘测试号’时，会生成openID用于与对应微信账号通讯
# 索引名 是为了便于自己识别和管理而对openID起的别名

all_users = {
    'dsb': 'otcrosj_vQhkmHLEGKt1KhclMISE',
    'xsb': 'otcrosvVnZr7UYrEzREK_7dFyg5A',
}


def users_to(users=None):
    if users is None:
        return all_users['dsb']
    elif users == "All":
        return ','.join(set(all_users.values()))
    else:
        if isinstance(users, list):
            users_info = []
            for user in users:
                users_info.append(all_users[user])
            return ','.join(set(users_info))
        else:
            print("'users' must be a list!")
            return


def json_post_data_generator(content='Hi! 你好！', users=None):
    msg_content = {'content': content}

    post_data = {
        'text': msg_content,
        'touser': "%s" % users_to(users),
        'toparty': '',
        'msgtype': 'text',
        'agentid': '9',
        'safe': '0',
    }
    # 由于字典格式不能被识别，需要转换成json然后在作post请求
    # 注：如果要发送的消息内容有中文的话，第三个参数一定要设为False
    return json.dumps(post_data)


def get_app_info():
    app_id = "wx99d481e0293e4432"
    app_secret = "3dcac65627791c943fcc5857feae7ce6"
    return (app_id, app_secret)


def get_token_info():
    app_info = get_app_info()
    r = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % app_info)
    print("Accessing %s" % r.url)
    res = r.json()
    if "errcode" not in res:
        access_token = res["access_token"]
        expires_in = res["expires_in"]
        return access_token, expires_in
    else:
        print("Can not get the access_token")
        print(res)
        quit()


post_url_freshing = ['']


def post_url():
    access_token, expires_in = get_token_info()
    print("token expires_in:%s" % expires_in)
    timer = threading.Timer((expires_in - 200), post_url)
    timer.start()
    post_url_freshing[0] = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % access_token


post_url()


def sender(text_str, user_list=None):
    post_url = post_url_freshing[0]
    post_data = json_post_data_generator(content=text_str, users=user_list)
    r = requests.post(post_url, data=post_data)
    result = r.json()
    if result["errcode"] == 0:
        print("Sent successfully")
    else:
        print(result["errmsg"])


if __name__ == "__main__":
    text_str = "你好"
    user_lis = None
    sender(text_str, user_lis)
