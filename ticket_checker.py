import time
import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = "https://discord.com/api/webhooks/1524383227018608850/zXnnGCtpDSKA7EM3fqpKvb-gpHXtolY2cO5jqOJqr2xiM2ZZ27HZ1QedkTmAoKS7E917"

# ★ URLごとに名前を付ける（Shiho専用）
TARGETS = [
    {
        "name": "なにわ北海道（2625501）",
        "url": "https://ticket.pia.jp/sp/ticketInformation.do?eventCd=2625501&rlsCd=001"
    },
    {
        "name": "なにわ福岡（2625504）",
        "url": "https://ticket.pia.jp/sp/ticketInformation.do?eventCd=2625504&rlsCd=001"
    },
    {
        "name": "トニセン大宮（2621541）",
        "url": "https://ticket.pia.jp/sp/ticketInformation.do?eventCd=2621541&rlsCd=001"
    },
    {
        "name": "バンザイ（2622348）",
        "url": "https://ticket.pia.jp/sp/ticketInformation.do?eventCd=2622348&rlsCd=001"
    }
]

# ★ Shiho専用：販売開始と判定するキーワード
KEYWORDS = ["販売中", "本日販売初日"]

def send_discord_message(text):
    data = {"content": text}
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code in (200, 204):
        print("Discord通知成功")
    else:
        print(f"通知失敗: {response.status_code}")

def check_ticket(target):
    url = target["url"]
    name = target["name"]

    try:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        page_text = soup.text

        # ★ キーワード判定
        for kw in KEYWORDS:
            if kw in page_text:
                send_discord_message(
                    f"🎉販売開始を検知しました！\n"
                    f"公演名: {name}\n"
                    f"URL: {url}\n"
                    f"判定キーワード: {kw}"
                )
                print(f"販売開始: {name}（キーワード: {kw}）")
                return True

        print(f"まだ販売開始していません: {name}")
        return False

    except Exception as e:
        print(f"エラー ({name}): {e}")
        return False

if __name__ == "__main__":
    while True:
        for target in TARGETS:
            if check_ticket(target):
                exit()  # どれか1つでも販売開始したら終了
        time.sleep(30)
