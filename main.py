import requests,os,platform,re
from fastapi import FastAPI

app = FastAPI()
@app.post("/apishare")
async def modeshare(cookie:str, idpost:str, message):
    hd = {
        'authority': 'mbasic.facebook.com',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'cookie': cookie,
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    url = requests.get('https://mbasic.facebook.com/'+idpost, headers=hd).url
    ac = requests.get(url, headers=hd).text
    node_share = re.findall('\/composer\/mbasic\/\?c_src=share.*?"', ac)
    if node_share == []:
        data1 = {'status':'fail','message':'Post Die Hoặc Không Có Nút Share'}
        return data1
    truycapshare = ac.split('/composer/mbasic/?c_src=share')[1].split('"')[0].replace('amp;', '')
    ac = requests.get('https://mbasic.facebook.com/composer/mbasic/?c_src=share'+truycapshare, headers=hd).text
    fb = ac.split('name="fb_dtsg" value="')[1].split('"')[0]
    jaz = ac.split('name="jazoest" value="')[1].split('"')[0]
    target = ac.split('name="target" value="')[1].split('"')[0]
    csid = ac.split('name="csid" value="')[1].split('"')[0]
    privacyx = ac.split('name="privacyx" value="')[1].split('"')[0]
    sid = ac.split('name="sid" value="')[1].split('"')[0]

    data = {
        "fb_dtsg": fb,
        "jazoest": jaz,
        "at": "",
        "target": target,
        "csid": csid,
        "c_src": "share",
        "referrer": "feed",
        "ctype": "advanced",
        "cver": "amber_share",
        "users_with": "",
        "album_id": "",
        "waterfall_source": "advanced_composer_timeline",
        "privacyx": privacyx,
        "appid": "0",
        "sid": sid,
        "linkUrl": "",
        "m": "self",
        "xc_message": message,
        "view_post": "Chia sẻ",
        "shared_from_post_id": sid,
    }
    share = ac.split('/composer/mbasic/?csid=')[2].split('"')[0].replace('amp;', '')
    hoan_thanh = requests.post('https://mbasic.facebook.com/composer/mbasic/?csid='+share, headers=hd, data=data).text
    if "Cảnh báo" in hoan_thanh or "Giờ bạn chưa dùng được tính năng này" in hoan_thanh:
        data2 = {'status':'fail','message':'Account Bị Block Tính Năng'}
        return data2
    data3 = {'status':'success','message':'Share Post Thành Công'}
    return data3
