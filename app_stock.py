import os
import json
import datetime
from flask import Flask, request, jsonify

from tools.util_crypto import auth_decode, auth_encode

app = Flask(__name__)

cache_path = '_data/cache.json'
cache = {}

content_path = '_data/content_{}.html'
content = None


@app.route('/', methods=['get'])
def root():
    return 'OK'


# POST接口，用于上传页面内容
@app.route('/html/upload_webpage/<key>', methods=['POST'])
def upload_content(key):
    global content
    content = request.data.decode('utf-8')  # 从请求中获取内容

    with open(content_path.format(key), 'w') as f:
        f.write(content)
    return "Content uploaded successfully"


# GET接口，用于展示缓存的内容
@app.route('/html/display_webpage/<key>', methods=['GET'])
def display_content(key):
    global content
    if content is None:
        if os.path.exists(content_path.format(key)):
            with open(content_path.format(key), 'r') as f:
                content = f.read()

    if content is None:
        return "No content available"
    else:
        return content


# 将缓存数据保存到本地文件
def save_cache():
    global cache

    json_cache = {}
    for key in cache:
        json_cache[key] = list(cache[key])

    with open(cache_path, 'w') as f:
        json.dump(json_cache, f, indent=4)


# 从本地文件加载缓存数据
def load_cache():
    global cache
    try:
        with open(cache_path, 'r') as f:
            json_cache = json.load(f)
        for key in json_cache:
            cache[key] = set(json_cache[key])
    except FileNotFoundError:
        cache = {}


@app.route('/get_key/<key>', methods=['GET'])
def get_key(key):
    apply = request.args.get('apply')
    if apply is None:
        return jsonify({'error': 'Miss parameter'}), 404
    elif key in ['silver6wings']:
        return auth_encode(apply)
    else:
        return jsonify({'error': 'No permission'}), 404


# 从缓存中获取指定 key 对应的集合
@app.route('/get_set/<key>', methods=['GET'])
def get_set(key):
    auth = request.args.get('auth')
    today = datetime.datetime.today().strftime('%Y%m%d')
    if today > auth_decode(auth)[:8]:
        return jsonify({'error': 'Auth out of date'}), 404

    if key in cache:
        return jsonify(list(cache[key]))
    else:
        return jsonify({'error': 'Key not found'}), 404


# 更新缓存中指定 key 对应的集合
@app.route('/update_set/<key>', methods=['POST'])
def update_set(key):
    data = request.get_json()
    if key in cache:
        # cache[key].update(data['value'])
        cache[key] = set(data['value'])
    else:
        cache[key] = set(data['value'])
    save_cache()
    return jsonify({'message': 'Set updated successfully'})


if __name__ == '__main__':
    load_cache()  # 加载缓存数据
    app.run(debug=True, host="0.0.0.0", port=5000)
