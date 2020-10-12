import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
    'Cookie': 'Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1602483736; _ga=GA1.2.839897484.1602483737; _gid=GA1.2.721085612.1602483737; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1602485893'
}

session = requests.Session()
response = session.get('https://www.itjuzi.com/investevent', headers=headers)
print(response.status_code)
print(response.text)