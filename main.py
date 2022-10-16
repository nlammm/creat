import requests,os,platform,re
from fastapi import FastAPI

app = FastAPI()
@app.post("/")
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
    url = requests.get(f'https://mbasic.facebook.com/{idpost}',headers=hd).url
    share = requests.get(url,headers=hd).text
    _find = re.findall('composer/mbasic/.*?"',share)
    if _find == []:
        data = {'status':'fail','message':'Post Die Hoặc Không Có Nút Share'}
        return data
    else:
        data = str(_find[0]).replace('amp;','').replace('"','')
        done1 = requests.get(f'https://mbasic.facebook.com/{data}',headers=hd).text
        fb_dtsg = done1.split('name="fb_dtsg" value="')[1].split('"')[0]
        jazoest = done1.split('name="jazoest" value="')[1].split('"')[0]
        target = done1.split('name="target" value="')[1].split('"')[0]
        csid = done1.split('name="csid" value="')[1].split('"')[0]
        privacyx = done1.split('name="privacyx" value="')[1].split('"')[0]
        sid = done1.split('name="sid" value="')[1].split('"')[0]
        data = {
            "fb_dtsg": fb_dtsg,
            "jazoest": jazoest,
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
        share2 = done1.split('action="/composer/mbasic/?csid=')[1].split('"')[0]
        share3 = share2.replace('amp;','')
        _share = requests.post(f'https://mbasic.facebook.com/composer/mbasic/?csid={share3}',headers=hd,data=data).text
        if "Cảnh báo" in _share or "Giờ bạn chưa dùng được tính năng này" in _share:
            data = {'status':'fail','message':'Account Bị Block Tính Năng'}
            return data
        else:
            data = {'status':'success','message':'Share Post Thành Công'}
            return data
