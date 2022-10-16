import requests,os,platform,re
from fastapi import FastAPI

app = FastAPI()
@app.post("/apishare")
async def modeshare(cookie:str, idpost:str, message):
    url = requests.get(f'https://mbasic.facebook.com/{idpost}',headers={'cookie': cookie}).url
    share = requests.get(url,headers={'cookie': cookie},timeout=100).text
    print(share)
    _find = re.findall('composer/mbasic/.*?"',share)
    print(_find)

    if _find == []:
        data = {'status':'fail','message':'Post Die Hoặc Không Có Nút Share'}
        return data
    else:
        data = str(_find[0]).replace('amp;','').replace('"','')
        done1 = requests.get(f'https://mbasic.facebook.com/{data}',headers={'cookie': cookie}).text
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
        _share = requests.post(f'https://mbasic.facebook.com/composer/mbasic/?csid={share3}',headers={'cookie': cookie},data=data).text
        if "Cảnh báo" in _share or "Giờ bạn chưa dùng được tính năng này" in _share:
            data = {'status':'fail','message':'Account Bị Block Tính Năng'}
            return data
        else:
            data = {'status':'success','message':'Share Post Thành Công'}
            return data
