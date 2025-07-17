import requests
import time
import schedule
from telegram import Bot
from datetime import datetime

TOKEN = "7585978334:AAHHR39pQnxyfLzSfxL_k2BPG1QOO-68RZE"
CHAT_ID = "7583851647"

bot = Bot(token=TOKEN)

def get_price():
    try:
        url = (
            "https://api.coingecko.com/api/v3/simple/price"
            "?ids=bitcoin,solana,zebec-protocol"
            "&vs_currencies=usd,idr"
            "&include_24hr_change=true"
        )
        response = requests.get(url)
        data = response.json()

        # Ambil data harga dan perubahan
        btc = data["bitcoin"]
        sol = data["solana"]
        zebec = data["zebec-protocol"]

        now = datetime.now().strftime("%d %B %Y, %H:%M WIB")

        message = f"📊 *Update Harga Crypto*\n🗓️ {now}\n\n"
        message += f"₿ *Bitcoin (BTC)*\n"
        message += f"   💵 USD: ${btc['usd']:,} ({btc['usd_24h_change']:+.2f}%)\n"
        message += f"   🇮🇩 IDR: Rp{btc['idr']:,}\n\n"

        message += f"🌞 *Solana (SOL)*\n"
        message += f"   💵 USD: ${sol['usd']:,} ({sol['usd_24h_change']:+.2f}%)\n"
        message += f"   🇮🇩 IDR: Rp{sol['idr']:,}\n\n"

        message += f"💧 *Zebec (ZBC)*\n"
        message += f"   💵 USD: ${zebec['usd']:.4f} ({zebec['usd_24h_change']:+.2f}%)\n"
        message += f"   🇮🇩 IDR: Rp{zebec['idr']:,}\n"

        bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id=CHAT_ID, text=f"❗ Terjadi error: {e}")

# Jalankan tiap hari jam 8 pagi
schedule.every().day.at("08:00").do(get_price)

# Looping terus-menerus
while True:
    schedule.run_pending()
    time.sleep(1)
