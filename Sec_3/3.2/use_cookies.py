import requests

headers = {
    'Cookie': '_xsrf=b8P79pyjd9V2RCtbvK0z40HoHnirN8fp; _zap=3149f0e8-9da1-4e43-95be-57cbbbae108c; d_c0="AJBhxWKx9A-PTgUu8THmGvwW5rcTRyWuZMc=|1566899101"; __utmc=51854390; __utmv=51854390.100--|2=registration_date=20161214=1^3=entry_date=20161214=1; z_c0="2|1:0|10:1582607576|4:z_c0|92:Mi4xR1NiUEF3QUFBQUFBa0dIRllySDBEeVlBQUFCZ0FsVk4yUHBCWHdBVGJ0T1lGZWdPcFIzOGEzekNENTZoN1NRS3BB|86d2985e1c6e96f7711c897376a00a420cb99e3e1daeffd0087b8d07f5d52970"; _ga=GA1.2.2029524421.1576474159; __utma=51854390.2029524421.1576474159.1576474159.1583198892.2; __utmz=51854390.1583198892.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/question/19869956; tst=r; q_c1=5d1251c6e060429f961763b419105cb8|1587690052000|1566899286000; _gid=GA1.2.2133097782.1588060248; SESSIONID=oNOPRGhnoCAVsCYoRqXkcm5mHIIa3hyiqrJytG7iSDV; JOID=W14TA05Qtq-1PHFkbFk1-eYjcFZyMPjm4GI5DAQz-u7lSj4yA7NZBOI_fmJvfSldiIDB2s7gE8_6FkWVf4P6uNY=; osd=UVoRBUlasq2zO3tgbl8y8-IhdlF4NPrg52g9DgI08OrnTDk4B7FfA-g7fGRody1fjofL3szmFMX-FEOSdYf4vtE=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1588123258,1588127813,1588128996,1588129864; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1588129882; KLBRSID=d6f775bb0765885473b0cba3a5fa9c12|1588131967|1588127809',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'
}
r = requests.get('https://www.zhihu.com', headers=headers)
print(r.text)