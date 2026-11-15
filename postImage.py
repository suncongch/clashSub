from datetime import datetime
import json
import yaml
from flask_cors import CORS

from flask import Flask, jsonify, request
from urlConfig import token_config,testHtml
from function import *
from ini import parse_acl4ssr_config, load_rulesets, normalize_rule, filter_clash_rule
from shadowrocket_cache import get_shadowrocket_config
from sub import order_rulesets_by_priority

app = Flask(__name__)
CORS(app, supports_credentials=True)

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

#netflix订阅文件
@app.route('/netflix', methods=['POST','GET'])
def netflix():
    token = request.args.get("token")
    ua = request.headers.get('User-Agent', '').lower()
    if  token in token_config:
        return netflixReturn(token,'clash')
    else:
        return "token error"

#普通分流配置
@app.route('/ini', methods=['POST','GET'])
def ini():
    return iniReturn()

#普通分流配置
@app.route('/iniMobile', methods=['POST','GET'])
def iniMobile():
    return iniReturn_mobile()

#Netflix 分流配置
@app.route('/netflixIni', methods=['POST','GET'])
def netflixIni():
    return netflixIniReturn()

#网络连接测试页
@app.route('/net')
def net():
    return testHtml 

#normal分流订阅函数1
@app.route('/sub')
def sub():
    token = request.args.get("token")
    ua = request.headers.get('User-Agent', '').lower()
    if  token in token_config:
        #appClient = detect_client(ua)
        #print(ua,appClient)
        return get_nodes(token,'clash')
    else:
        return "token error"

#admin分流订阅接口
@app.route('/admin', methods=['POST','GET'])
def admin():
    token = request.args.get("token")
    ua = request.headers.get('User-Agent', '').lower()
    appClient = detect_client(ua)
    return  get_nodes(token,appClient,admin=True)

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


def run_http():
    # 启动 HTTP 服务
    app.run(host='127.0.0.1', port=8000,debug=True)

def run_https():
    # 启动 HTTPS 服务
    app.run(host='127.0.0.1', port=9000, ssl_context=('www.andysun.cool.pem', 'www.andysun.cool.key'))


if __name__ == '__main__':
    run_http()
