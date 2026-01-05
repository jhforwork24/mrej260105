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
    
    # 공지사항을 제외한 첫 번째 일반 게시글 찾기
    post = soup.select_one('table.board_list tbody tr')
    if not post: return

    title_elem = post.select_one('td.al a')
    title = title_elem.get_text(strip=True)
    link = BASE_URL + title_elem['href']
    post_id = post.select_one('td.num').get_text(strip=True)

    # 이전 기록 확인
    last_id = ""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            last_id = f.read().strip()

    # 새 글일 경우 텔레그램 전송
    if post_id != last_id:
        msg = f"🔔 [NARS 신규 보고서]\n\n제목: {title}\n링크: {link}"
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.get(url, params={'chat_id': CHAT_ID, 'text': msg})
        
        # 최신 ID 저장
        with open(DB_FILE, 'w') as f:
            f.write(post_id)

if __name__ == "__main__":
    check_nars()
