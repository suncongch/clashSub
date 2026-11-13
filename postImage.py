import time
from datetime import datetime, timezone, timedelta
import json
import os
from random import randint, random
import threading
from threading import Thread
import base64
import re
import requests
import urllib
import yaml


from flask_cors import CORS

from urllib.parse import quote

from flask import Flask, jsonify, request, send_from_directory,render_template,send_file
from werkzeug.utils import secure_filename

from urlConfig import *
from function import *
from shadowrocket_cache import get_shadowrocket_config
from pathlib import Path


CACHE_FILE = Path("data/node_cache.json")
LOCK = threading.Lock()
CACHE_TTL = 18 * 60   # 18 分钟


# 当前脚本所在目录（绝对路径）
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['UPLOAD_FOLDER'] = 'img/'
app.config['DOWNLOAD_FOLDER'] = 'img/'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif','mp4'])

app1 = Flask('selfbloc')



#路由函数已不使用
@app1.route('/')
def home():
    return render_template('index.html')
#Thread(target=lambda:app1.run(port=80)).start()

# For a given file, return whether it's an allowed type or notpip
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream

@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('videos', filename)

#路由下载函数
@app.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        # if os.path.isfile(os.path.join('upload', filename)):
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)
        pass

#接受函数上传图片文件函数已不使用
@app.route('/uploadabandon', methods=['POST'])
def uploadabandon():
    #print(request.headers,request)
    upload_file = request.files['image01']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        # upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], "up.jpg"))
        from sprateImage import separateNormal
        separateNormal()
        from main import whole
        whole()
        return 'hello, ' + request.form.get('name', 'little apple') + '. success'
    else:
        return 'hello, ' + request.form.get('name', 'little apple') + '. failed'

#接受函数上传图片文件函数已不使用
@app.route('/upload', methods=['POST','PUT'])
def upload():
    upload_file = request.files['image01']
    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        # upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        upload_file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], "up.jpg"))
        
        return 'hello, '
    else:
        return 'hello, '

#软件程序加密函数
@app.route('/encrytion', methods=['POST','GET'])
def encrytion():
    if request.method == "POST":
        request_data = request.json
        mac = request_data['mac']
        if mac == "1A-95-DD-15-A9-5A" or  mac == "00-E0-70-DE-08-80" or mac == "00-E0-70-DE-02-8E"or mac == "00-E0-70-DE-07-59"or mac =="00-E0-70-DE-01-89":
            endTime = "2022-11-30"
            print(mac)
            endTime = datetime.strptime(endTime,"%Y-%m-%d")
            macLocalTime = datetime.strptime(request_data['time'],"%Y-%m-%d")
            lastTime = (endTime-macLocalTime).days
            reutrnData = {
                          "play":True,
                          "lastTime":lastTime
                        }
            if lastTime >= 0:
                
                return json.dumps(reutrnData,sort_keys=True,indent=2,separators=(',',':'))
            else:
                reutrnData['play'] = False
                return json.dumps(reutrnData,sort_keys=True,indent=2,separators=(',',':'))
        else:
            print(mac)
            reutrnData = {
                          "play":False,
                          "lastTime":lastTime
                        }
            return json.dumps(reutrnData,sort_keys=True,indent=2,separators=(',',':'))
    if request.method == "GET":
        request_data = request.json
        ip = request_data['ip']
        print(ip)
        return str(ip)
    else:
        return "none post"

#netflix订阅文件暂已不再维护
@app.route('/netflix', methods=['POST','GET'])
def netflix():
    token = request.args.get("token")
    ua = request.headers.get('User-Agent', '').lower()
    if  token == "jan" or token == "this" or token == "just":
        return_text = ''
        appClient = detect_client(ua)
        print(ua,appClient)
        if appClient == "clash":
            return_text = netflixReturn(token,'clash')
        elif appClient == "shadowRocket":
            return_text = get_nodes(token,'clash')
        else:
            return_text = v2rayReturn(token)
        return return_text
    else:
        return "token error"

#clash路由配置
@app.route('/ini', methods=['POST','GET'])
def ini():
    return iniReturn()

@app.route('/iniMobile', methods=['POST','GET'])
def iniMobile():
    return iniReturn_mobile()

#clash路由配置
@app.route('/netflixIni', methods=['POST','GET'])
def netflixIni():
    return netflixIniReturn()

#网络连接测试页
@app.route('/net')
def net():
    html_text = """<html>
<head>
<meta http-equiv="Content-Language" content="zh-CN">
<meta HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=gb2312">
<script>
	function open_web(){
        <!--window.location.href="https://youtube.com"; -->
        window.open("https://youtube.com");
        window.open("http://ip111.cn");
        window.open("https://google.com");
		window.open("https://instagram.com");
		window.open("https://behance.net");
		window.open("https://pinterest.com");
		window.open("https://artsation.com");
		window.open("https://vimeo.com");
	}
<!-- window.onload = open_web(); -->
</script>
</head>
<body>
<button onclick = "open_web()"> 跳转测试网站 </button>
</body>"""
    return html_text

#v2ray shadowrocket clash分流订阅函数
@app.route('/sub')
def sub():
    token = request.args.get("token")
    ua = request.headers.get('User-Agent', '').lower()
    if request.args.get("type")=="vless":
        vlessFlag = True
    else:
        vlessFlag = False
    if  token == "jan" or token == "this" or token == "just":
        return_text = ''
        appClient = detect_client(ua)
        print(ua,appClient)
        if appClient == "clash":
            return_text = get_nodes(token,'clash',vless=vlessFlag)
        elif appClient == "shadowRocket":
            return_text = get_nodes(token,'clash',vless=vlessFlag)
        else:
            return_text = v2rayReturn(token)
        return return_text
    else:
        return "token error"

#3x-ui 出站订阅接口：3x-ui 请求本接口，返回分享链接订阅（Base64）
#节点来源与筛选沿用 /sub 的 get_nodes 流程，参数与 /sub 相同：token、type
@app.route('/xui3Sub')
def xui3Sub():
    token = request.args.get("token")
    if token not in ("jan", "this", "just"):
        return "token error", 403
    vlessFlag = request.args.get("type") == "vless"

    resp = get_nodes(token, 'clash', vless=vlessFlag)
    if resp is None:
        return "Failed to fetch nodes", 502

    data = yaml.safe_load(resp.get_data(as_text=True)) or {}
    proxies = [
        p for p in data.get("proxies", [])
        if "vultr" not in f"{p.get('name', '')} {p.get('server', '')}".lower()
    ]
    return Response(
        build_3xui_outbound_subscription(proxies),
        mimetype='text/plain'
    )

#测试使用函数
@app.route('/admin', methods=['POST','GET'])
def test1():
    token = request.args.get("token")
    if request.args.get("type")=="vless":
        vlessFlag = True
    else:
        vlessFlag = False
    ua = request.headers.get('User-Agent', '').lower()
    appClient = detect_client(ua)
    return  get_nodes(token,appClient,admin=True,vless=vlessFlag)

@app.route('/movie')
def movie_list():
    return '''
    <!DOCTYPE html>
<html>
<body>
<video width="400" height="300" controls="controls">
  <source src="static/movie/2.mp4" type="video/mp4" />
</video>
</body>
</html>
    '''

@app.route('/upload_base64', methods=['POST'])
def upload_base64_image():
    data = request.get_json()

    if not data or 'image' not in data:
        return jsonify({'status': 'error', 'message': 'No image data found'}), 400

    base64_image = data['image']

    try:
        # 如果前面带有 "data:image/png;base64," 则去除
        if ',' in base64_image:
            base64_image = base64_image.split(',')[1]

        # 解码
        image_data = base64.b64decode(base64_image)

        # 构建文件路径
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        save_path = os.path.join('static/uploaded_images', filename)
        os.makedirs('uploaded_images', exist_ok=True)

        # 保存图片
        with open(save_path, 'wb') as f:
            f.write(image_data)

        return jsonify({'status': 'success', 'filename': filename}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/img2img', methods=['POST'])
def img2img_handler():
    data = request.get_json()

    # 判断是否包含 execute 字段
    if not data or 'execute' not in data:
        return jsonify({'status': 'error', 'message': 'Missing "execute" field'}), 400

    if data['execute'] is True:

        processImgUrl = img2img(urlJoin('static/uploaded_images',data['uploadImageName']),
                                urlJoin('process_images'),
                                data['model'],
                                data['controlNetType'],
                                data['crossValue0'],
                                data['cfg'],
                                )
        
        # 这里只是一个示例动作：
        print("Executing image transformation...")
        # 示例返回
        return jsonify({'status': 'success', 'message': 'Image transformation executed','imgUrl':processImgUrl}), 200
    else:
        return jsonify({'status': 'skipped', 'message': 'Execution flag is false'}), 200

#强制更新远程规则并返回所有规则
@app.route('/rules', methods=['GET', 'POST'])
def rules():
    try:
        cfg = parse_acl4ssr_config(iniReturn())
        rulesets = order_rulesets_by_priority(cfg["rulesets"])
        all_rules = []
        for ruleset_rules in load_rulesets(rulesets, force=True):
            for r in ruleset_rules:
                r = filter_clash_rule(normalize_rule(r))
                if r:
                    all_rules.append(r)
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 502
    # 清除订阅缓存，使新规则立即生效
    with LOCK:
        CACHE_FILE.unlink(missing_ok=True)
    return jsonify({'status': 'success', 'count': len(all_rules), 'rules': all_rules})

@app.route('/shadowRocketConfig/', methods=['GET'])
def shadowRocketConfig():
    return get_shadowrocket_config()


def urlJoin(temUrl,fileName = None):
    if fileName is None:
        return os.path.join(current_dir,temUrl)
    else:
        return os.path.join(current_dir,temUrl,fileName)
    
def detect_client(ua):
    if any(x in ua for x in ('flclash','stash')):
        return 'clash'
    if 'shadowrocket' in ua:
        return 'clash'
    return 'unknown'

def make_cache_key(token, client):
    parts = []
    if token:
        parts.append(f"token:{token}")
    if client:
        parts.append(client)
    return "|".join(parts)

def is_expired(entry):
    return time.time() - entry["timestamp"] > entry["ttl"]

def load_cache():
    if not CACHE_FILE.exists():
        return {}
    return json.loads(CACHE_FILE.read_text(encoding="utf-8"))

def save_cache(cache):
    CACHE_FILE.parent.mkdir(exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(cache, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def get_nodes(token=None, client=None,admin=False,vless=False ):
    cache_key = make_cache_key(token, client)

    with LOCK:
        cache = load_cache()
        if admin is False:
            if cache_key in cache and not is_expired(cache[cache_key]):
                cached = cache[cache_key]
                return Response(
                    cached["body"],
                    headers=cached["headers"],
                    mimetype=cached.get("mimetype", "text/plain")
                )
            resp  = clashReturn(token, client,vless)
            if 'Error fetching content.' not in resp.get_data(as_text=True):
                cache[cache_key] = {
                    "timestamp": datetime.now().timestamp(),
                    "北京时间：": ts_to_beijing_str(datetime.now().timestamp()),
                    "ttl": 18 * 60,  # 18 分钟
                    "headers": dict(resp.headers),
                    "body": resp.get_data(as_text=True),
                    "mimetype": resp.mimetype
                }
                save_cache(cache)
                return resp
            else:
                return

        else:
        # 缓存失效 → 重新生成
            resp  = adminRetun(token, client,vless)
            if 'Error fetching content.' not in resp.get_data(as_text=True):
                if "body" in cache.get(cache_key, {}):
                    cache[cache_key]["timestamp"] = (datetime.now() - timedelta(minutes=18)).timestamp()
                    cache[cache_key]["北京时间："] = ts_to_beijing_str((datetime.now() - timedelta(minutes=18)).timestamp())
                    save_cache(cache)
              
                return resp
            else:
                return

def ts_to_beijing_str(ts):
    dt = datetime.fromtimestamp(
        ts,
        timezone(timedelta(hours=8))
    )

    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

def run_http():
    # 启动 HTTP 服务
    app.run(host='127.0.0.1', port=8000,debug=True)

def run_https():
    # 启动 HTTPS 服务
    app.run(host='127.0.0.1', port=9000, ssl_context=('www.andysun.cool.pem', 'www.andysun.cool.key'))


if __name__ == '__main__':
    #Thread(target=run_http).start()
    #Thread(target=run_https).start()
    run_http()
