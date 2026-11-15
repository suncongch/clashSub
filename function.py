from datetime import datetime,timedelta,timezone
import requests
from flask import Response
from sub import build_from_config, yamlToStr
from urlConfig import token_config, ini_config, nodeMod, nodeMod_ios_anndroid, httpProxies, githubConfig, netflixConfig,CACHE_FILE
import threading
import time,json

LOCK = threading.Lock()
CACHE_TTL = 18 * 60   # 18 分钟

def iniReturn():
    urlHead = 'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Mini_NoAuto.ini'
    f = open(githubConfig,'r',encoding='utf-8')
    returnText = f.read()
    f.close()

    return returnText + nodeMod

def iniReturn_mobile():
    urlHead = 'https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Mini_NoAuto.ini'
    f = open(githubConfig,'r',encoding='utf-8')
    returnText = f.read()
    f.close()

    return returnText + nodeMod_ios_anndroid
    
def netflixIniReturn():
    f = open(netflixConfig,'r',encoding='utf-8')
    returnText = f.read()
    f.close()
    return returnText + nodeMod

def clashReturn(token,device):
    if device in ini_config:
        iniUrl = ini_config[device]
    else:
        iniUrl = ini_config["unknown"]
    
    temSubscribeUrl = None

    if token in token_config:
        temSubscribeUrl, msg = token_config[token]
        print(msg)

        yamlFile = build_from_config(iniUrl,temSubscribeUrl,auto_group=True)
        #save_yaml(yamlFile,"./test.yaml")
        return yaml_response(yamlFile,'Andysun_'+token,None)
    else:
        return Response("Invalid token", status=400)

#不走本地缓存
def netflixReturn(token,device):
    if device in ("Shadowrocket","Android"):
        iniUrl = ini_config[device]
    else:
        iniUrl = ini_config["netflix"]

    if token in token_config:
        temSubscribeUrl , msg= token_config[token]
        infoUrl = temSubscribeUrl[0]
    
        user_info = getUserInfo(infoUrl)
        print(user_info)
        yamlFile = build_from_config(iniUrl,temSubscribeUrl,auto_group=True)
        #save_yaml(yamlFile,"./test.yaml")
        return yaml_response(yamlFile,'Admin_'+token,user_info)
    else:
        return Response("Invalid token", status=400)
    
def adminRetun(token,device):
    if device in ("Shadowrocket","Android"):
        iniUrl = ini_config[device]
    else:
        iniUrl = ini_config["unknown"]

    if token in token_config:
        temSubscribeUrl , msg = token_config[token]
        infoUrl = temSubscribeUrl[0]
    
        print(temSubscribeUrl)
        user_info = getUserInfo(infoUrl)
        
        print(user_info)
        yamlFile = build_from_config(iniUrl,temSubscribeUrl,auto_group=True)
        #save_yaml(yamlFile,"./test.yaml")
        return yaml_response(yamlFile,'Admin_'+token,user_info)
    else:
        return "Invalid token"

def getUserInfo(temUrl):
    # 设置自定义 headers
    headers = {
        'User-Agent': 'ClashforWindows/0.20.39'
    }

    response = requests.get(temUrl, proxies=httpProxies, headers=headers)
    # 获取请求的 headers
    headers = response.headers
    return headers.get('subscription-userinfo',"none")

def yaml_response(temYaml, filename: str, userinfo: str | None = None):
    yaml_text = yamlToStr(temYaml)
    def stream():
        chunk_size = 8192  # 较小分块
        data = yaml_text.encode("utf-8")  # ✅ 一次性转 bytes
        total = len(data)
        for i in range(0, total, chunk_size):
            yield data[i:i+chunk_size]

    # 如果是文本且确定 UTF-8，可改 mimetype 为 text/plain;charset=utf-8
    resp = Response(stream(), mimetype='text/plain;charset=utf-8')
    resp.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{filename}"
    if userinfo:
        resp.headers['subscription-userinfo'] = userinfo
    else:
        resp.headers['subscription-userinfo'] = 'update=' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return resp

def get_nodes(token=None, client=None,admin=False ):
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
            resp  = clashReturn(token, client)
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
            resp  = adminRetun(token, client)
            if 'Error fetching content.' not in resp.get_data(as_text=True):
                if "body" in cache.get(cache_key, {}):
                    cache[cache_key]["timestamp"] = (datetime.now() - timedelta(minutes=18)).timestamp()
                    cache[cache_key]["北京时间："] = ts_to_beijing_str((datetime.now() - timedelta(minutes=18)).timestamp())
                    save_cache(cache)
              
                return resp
            else:
                return


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

def ts_to_beijing_str(ts):
    dt = datetime.fromtimestamp(
        ts,
        timezone(timedelta(hours=8))
    )

    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")
