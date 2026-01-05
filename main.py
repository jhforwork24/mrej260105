import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
URL = 'https://www.nars.go.kr/report/list.do?cmsCode=CM0043'
BASE_URL = 'https://www.nars.go.kr'
DB_FILE = 'last_post.txt'

def check_nars():
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    post = soup.select_one('table.board_list tbody tr')
    if not post: return

    title_elem = post.select_one('td.al a')
    title = title_elem.get_text(strip=True)
    link = BASE_URL + title_elem['href']
    post_id = post.select_one('td.num').get_text(strip=True)

    # 파일이 없으면 빈 문자열로 시작 (에러 방지)
    last_id = ""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            last_id = f.read().strip()

    # 새 글 발견 시 알림 발송 및 ID 저장
    if post_id != last_id:
        msg = f"🔔 [NARS 신규 보고서]\n\n제목: {title}\n링크: {link}"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.get(url, params={'chat_id': CHAT_ID, 'text': msg})
        
        with open(DB_FILE, 'w') as f:
            f.write(post_id)
        print(f"New post found: {post_id}")
    else:
        print("No new posts.")

if __name__ == "__main__":
    check_nars()
