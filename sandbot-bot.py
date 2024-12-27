import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Token bot Telegram Anda
TOKEN = '8002094527:AAEVgIUGGEjAXop0Neib78oVwqkQnabI8jw'  # Ganti dengan token bot yang diberikan oleh @BotFather
# Chat ID Anda (dapatkan dari @userinfobot)
CHAT_ID = '5171922156'  # Ganti dengan chat ID yang Anda dapatkan

# URL halaman yang ingin di-scrape
url = "https://dune.com/4brigade/layer3-quest-aggregator"  # Ganti dengan URL yang relevan

# Fungsi untuk mengirim pesan ke Telegram
def send_to_telegram(message):
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Fungsi untuk melakukan web scraping dan mencari link dengan kata "The Sandbox"
def scrape_and_notify():
    # Menambahkan header User-Agent untuk mensimulasikan permintaan dari browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Mengirim permintaan GET dengan header User-Agent
    response = requests.get(url, headers=headers)

    # Jika permintaan berhasil (status code 200), proses HTML
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Menyaring link dengan kata "the-sandbox" di href atau teks
        sandbox_links = soup.find_all("a", href=lambda href: href and "the-sandbox" in href.lower())
        
        # Jika Anda ingin mencari "The Sandbox" dalam teks link, gunakan ini:
        # sandbox_links = soup.find_all("a", string=lambda text: text and "the sandbox" in text.lower())

        # Jika ada link yang ditemukan
        if sandbox_links:
            message = "Link Quest The Sandbox:\n"
            for link in sandbox_links:
                message += f"{link['href']} - {link.text.strip()}\n"
            # Mengirimkan pesan ke Telegram
            send_to_telegram(message)
        else:
            print("Tidak ada link dengan kata 'The Sandbox' ditemukan.")
    else:
        print(f"Gagal mengambil halaman: {response.status_code}")

# Menjalankan fungsi untuk pertama kali
scrape_and_notify()
