import aiohttp
import asyncio
from bs4 import BeautifulSoup
from telegram import Bot
import time
from fake_useragent import FakeUserAgent

# Konfigurasi bot Telegram
BOT_TOKEN = "8002094527:AAEVgIUGGEjAXop0Neib78oVwqkQnabI8jw"
CHAT_ID = "5171922156"  # ID user Anda
bot = Bot(token=BOT_TOKEN)

# URL yang akan dipantau
URL = "https://app.layer3.xyz/communities/the-sandbox?slug=the-sandbox"

# Menggunakan FakeUserAgent untuk mendapatkan User-Agent yang acak
user_agent = FakeUserAgent().random

# Header lengkap untuk menghindari error 403
headers = {
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://app.layer3.xyz",
    "Referer": "https://app.layer3.xyz/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": user_agent
}

# Fungsi untuk mendapatkan daftar quest dari halaman menggunakan aiohttp
async def fetch_quests():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch data from {URL}. Status code: {response.status}")
            
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            # Menggunakan kelas spesifik
            quests = soup.find_all('div', class_='flex w-full min-w-0 grow flex-col justify-between gap-[28px] rounded-inherit mobile:gap-md')
            return [quest.text.strip() for quest in quests]

# Simpan daftar quest terakhir
last_quests = []

async def main():
    global last_quests
    while True:
        try:
            current_quests = await fetch_quests()
            if not last_quests:
                last_quests = current_quests

            # Cari quest baru
            new_quests = [quest for quest in current_quests if quest not in last_quests]
            if new_quests:
                for quest in new_quests:
                    await bot.send_message(chat_id=CHAT_ID, text=f"Quest baru ditemukan: {quest}")
                last_quests = current_quests

        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

        # Tunggu 1 menit sebelum memeriksa lagi
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
