import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time

# Konfigurasi bot Telegram
BOT_TOKEN = "8002094527:AAEVgIUGGEjAXop0Neib78oVwqkQnabI8jw"
CHAT_ID = "5171922156"  # ID user Anda
bot = Bot(token=BOT_TOKEN)

# URL yang akan dipantau
URL = "https://app.layer3.xyz/communities/the-sandbox?slug=the-sandbox"

# Fungsi untuk mendapatkan daftar quest dari halaman
def fetch_quests():
    response = requests.get(URL)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {URL}. Status code: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    # Menggunakan kelas spesifik
    quests = soup.find_all('div', class_='flex w-full min-w-0 grow flex-col justify-between gap-[28px] rounded-inherit mobile:gap-md')
    return [quest.text.strip() for quest in quests]

# Simpan daftar quest terakhir
last_quests = []

def main():
    global last_quests
    while True:
        try:
            current_quests = fetch_quests()
            if not last_quests:
                last_quests = current_quests

            # Cari quest baru
            new_quests = [quest for quest in current_quests if quest not in last_quests]
            if new_quests:
                for quest in new_quests:
                    bot.send_message(chat_id=CHAT_ID, text=f"Quest baru ditemukan: {quest}")
                last_quests = current_quests

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

        # Tunggu 5 menit sebelum memeriksa lagi
        time.sleep(300)

if __name__ == "__main__":
    main()
