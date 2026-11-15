from pathlib import Path

"""本地的ini配置文件路径，用于存储 普通分流 配置和 Netflix 分流配置"""

githubConfig = "data/githubConfig.txt"
netflixConfig = "data/netflixConfig.txt"

includeCondition = (
    r'日本(?!\s*3\b).*|'
    r'日本\s*1\s*\[\s*IPv6\s*\]|'
    r'日本\s*2\s*\[\s*IPv6\s*\]|'
    r'香港|'
    r'andy|'
    r'新加坡(?!\s*3\b).*|'
    r'新加坡\s*1\s*\[\s*IPv6\s*\]|'
    r'新加坡\s*2\s*\[\s*IPv6\s*\]|'
    r'新加坡.*推荐|'
    r'美国(?!.*海外).*|'
    r'台湾(?!.*海外).*'
)
CACHE_FILE = Path("data/node_cache.json")

justSubUrl = [
             "https://mytoken-1.huyun.nl/api/hutoken/8d09b3b4a30bf2ddcab454e15763413a",
             "https://vultr.andysun.cool:2096/clash/andysun",
            ]
#this
thisSubUrl = [
             "https://xhtoken.huyun.nl/api/xiongtoken/3f7abd09da5057b371fa9cc091cb34a4",
             "https://vultr.andysun.cool:2096/clash/andysun",
             "https://mytoken-1.huyun.nl/api/hutoken/8d09b3b4a30bf2ddcab454e15763413a",
             ]
#tem
testScribeUrl = [
                "https://mytoken-1.huyun.nl/api/v1/client/subscribe?token=929aed590be33b7f90c182e83a62a40a",
                ]
#jan
janSubUrl = [
            "https://xhtoken.huyun.nl/api/xiongtoken/3f7abd09da5057b371fa9cc091cb34a4",
            "https://vultr.andysun.cool:2096/clash/andysun",
            ]
#netflix
netflixSubUrl = [
                "https://mytoken-1.huyun.nl/api/hutoken/8d09b3b4a30bf2ddcab454e15763413a",
                "https://tg.govlist.top/api/v1/client/subscribe?token=f527ba7e39666421955cb1301798b214"
                ]

token_config = {
    "just": (justSubUrl, "justPost"),
    "jan": (janSubUrl[:2], "janPost"),
    "this": (thisSubUrl[:2], "thisPost"),
}

ini_config = {
    "Shadowrocket": "http://cloud.andysun.cool:9001/iniMobile",
    "Android": "http://cloud.andysun.cool:9001/iniMobile",
    "unknown": "http://cloud.andysun.cool:9001/iniMobile",
    "netflix": "http://cloud.andysun.cool:9001/netflixIni"
}

httpProxies = {
        "http": "http://we4fnl6n:jdygxy766r2q@185.220.197.184:41747",
        "https": "http://we4fnl6n:jdygxy766r2q@185.220.197.184:41747"
}

nodeMod = r'''
add_emoji=true
remove_old_emoji=true
emoji=(香港|HK|Hong Kong),🇭🇰
emoji=(日本|川日|东京|大阪|泉日|埼玉|JP|Japan),🇯🇵
emoji=(美国|波特兰|达拉斯|俄勒冈|凤凰城|费利蒙|硅谷|拉斯维加斯|洛杉矶|圣何塞|圣克拉拉|西雅图|芝加哥|US|United States),🇺🇸
emoji=(台湾|新北|彰化|TW|Taiwan),🇹🇼
emoji=(新加坡|坡|狮城|狮城|SG|Singapore),🇸🇬
emoji=(KR|Korea|KOR|首尔|韩国|韩|韓),🇰🇷
emoji=(DE|Germany|DEU|德|德国),🇩🇪
emoji=(IN|India|IND|印度),🇮🇳
emoji=(CA|Canada|CAN|加拿大),🇨🇦
emoji=(LU|LUX|卢森堡|盧森堡),🇱🇺
emoji=(RU|RUS|俄罗斯|俄),🇷🇺
emoji=(TR|TUR|土耳其),🇹🇷
emoji=(GB|GBR|UK|英国|英),🇬🇧
emoji=(AR|ARG|阿根廷),🇦🇷
emoji=(BR|BRA|巴西),🇧🇷
emoji=(AU|AUS|澳大利亚|澳),🇦🇺
emoji=(AE|UAE|阿联酋|阿拉伯联合酋长国),🇦🇪
emoji=(PL|POL|波兰),🇵🇱
emoji=(FR|FRA|法国),🇫🇷
rename_node=新加坡@狮城
rename_node=2\ 倍扣费节点@备用
rename_node=  \[ h4 \]@
rename_node=  \ \[ 推荐 \]@
rename_node=  \ \[\ 高速\ \]@
rename_node=  (\d+)@$1
rename_node=  狮城\ (\d)\ $@狮城 $1   wifi 推荐
rename_node=  日本\ (\d)\ $@日本 $1   wifi 推荐
rename_node=  狮城\ (\d)\ \[(.*)Inter2\ \]$@狮城 $1   wifi 推荐
rename_node=  日本\ (\d)\ \[(.*)Inter2\ \]$@日本 $1   wifi 推荐
rename_node=  韩国.*?/(SK|KT)区域(\d+)节点$@韩国区域$2-$1节点
rename_node= -解锁Netflix@🍿

rename_node=hysteria2-vultr.andysun.cool-42426@🇸🇬 vultr
rename_node=andy@🇸🇬 vultr

rename_node=\ h12@
rename_node=  \[ IPv6 \]@  📶 流量  \[IPv6\]
rename_node=  \ \[ 0.5x \]@
'''
nodeMod_ios_anndroid = r'''
add_emoji=true
remove_old_emoji=true
emoji=(香港|HK|Hong Kong),🇭🇰
emoji=(日本|川日|东京|大阪|泉日|埼玉|JP|Japan),🇯🇵
emoji=(美国|波特兰|达拉斯|俄勒冈|凤凰城|费利蒙|硅谷|拉斯维加斯|洛杉矶|圣何塞|圣克拉拉|西雅图|芝加哥|US|United States),🇺🇸
emoji=(台湾|新北|彰化|TW|Taiwan),🇹🇼
emoji=(新加坡|坡|狮城|狮城|SG|Singapore),🇸🇬
emoji=(KR|Korea|KOR|首尔|韩国|韩|韓),🇰🇷
emoji=(DE|Germany|DEU|德|德国),🇩🇪
emoji=(IN|India|IND|印度),🇮🇳
emoji=(CA|Canada|CAN|加拿大),🇨🇦
emoji=(LU|LUX|卢森堡|盧森堡),🇱🇺
emoji=(RU|RUS|俄罗斯|俄),🇷🇺
emoji=(TR|TUR|土耳其),🇹🇷
emoji=(GB|GBR|UK|英国|英),🇬🇧
emoji=(AR|ARG|阿根廷),🇦🇷
emoji=(BR|BRA|巴西),🇧🇷
emoji=(AU|AUS|澳大利亚|澳),🇦🇺
emoji=(AE|UAE|阿联酋|阿拉伯联合酋长国),🇦🇪
emoji=(PL|POL|波兰),🇵🇱
emoji=(FR|FRA|法国),🇫🇷
rename_node=新加坡@狮城
rename_node=  \[ h4 \]@
rename_node=  \ \[ 推荐 \]@
rename_node=  \ \[ 高速 \]@
rename_node=  (\d+)@$1
rename_node=  狮城\s(\d)\ $@狮城 $1   🛜 推荐
rename_node=  日本\ (\d)\ $@日本 $1   🛜 推荐

rename_node=  狮城\ (\d)\ \[(.*)Inter2\ \]$@狮城 $1   wifi 推荐
rename_node=  日本\ (\d)\ \[(.*)Inter2\ \]$@日本 $1   wifi 推荐
rename_node=  韩国.*?/(SK|KT)区域(\d+)节点$@韩国区域$2-$1节点
rename_node= -解锁Netflix@🍿

rename_node=  \[ IPv6 \]@  📶 流量  \[IPv6\]
rename_node=  \ \[ 0.5x \]@
'''

testHtml = """<html>
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

tokenList = ["this", "jan", "just"]