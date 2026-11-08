import os
import pandas as pd
import requests
from datetime import datetime
import sys

# ==============================================================================
# ⛔ BLOCCO META ATTIVO: Tutte le comunicazioni verso Meta sono bloccate.
# ✈️ CONVOGLIAMENTO SU TELEGRAM: Ogni interazione/post è instradato su Telegram.
# ==============================================================================

# Credenziali Telegram per convogliare le interazioni
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN") or "8643190035:AAHaUOT12j8l9f6GU9WW4W9HFOLfV-5r5-U"
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") or "1723292483"

# Configurazione Facebook conservata per ripristino futuro (ma DISATTIVATA)
FB_PAGE_ID_BACKUP = os.environ.get("FB_PAGE_ID") or "108297671444008"
FB_ACCESS_TOKEN_BACKUP = os.environ.get("FB_ACCESS_TOKEN")

# Impostazioni Repository GitHub
GITHUB_USER = os.environ.get("GITHUB_REPOSITORY_OWNER")
REPO_NAME = os.environ.get("GITHUB_REPOSITORY")
BRANCH = "main"

def get_image_url_from_github(filename):
    """Costruisce il link pubblico dell'immagine caricata su GitHub"""
    base_url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/images/{filename}"
    return base_url

def post_to_facebook(message, image_url):
    """
    ⛔ BLOCCO META: Graph API disattivata.
    ✈️ CONVOGLIAMENTO: Invia il post e la foto direttamente a Telegram (Chat ID 1723292483).
    """
    print("⛔ [BLOCCO META] Chiamata a graph.facebook.com bloccata con successo.")
    print("✈️ [CONVOGLIAMENTO TELEGRAM] Invio del post programmato ad Antonio su Telegram...")
    
    caption = f"📢 *[POST SOCIAL PROGRAMMATO — CONVOGLIATO SU TELEGRAM]*
_(Meta/Facebook bloccato)_

{message}"
    if len(caption) > 1024:
        caption = caption[:1020] + "..."
        
    url_tg_photo = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload_photo = {
        'chat_id': TELEGRAM_CHAT_ID,
        'photo': image_url,
        'caption': caption,
        'parse_mode': 'Markdown'
    }
    
    try:
        res = requests.post(url_tg_photo, data=payload_photo, timeout=25)
        if res.status_code == 200:
            print("✅ Post inviato con successo su Telegram!")
            return
        else:
            print(f"⚠️ Errore invio foto Telegram ({res.status_code}), tento solo testo...")
            url_tg_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload_msg = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': f"{caption}

🖼️ *Link Immagine:* {image_url}",
                'parse_mode': 'Markdown'
            }
            res_msg = requests.post(url_tg_msg, data=payload_msg, timeout=25)
            if res_msg.status_code == 200:
                print("✅ Post (testo) inviato con successo su Telegram!")
            else:
                print(f"❌ Errore fallback Telegram: {res_msg.text}")
    except Exception as e:
        print(f"❌ Errore Telegram: {e}")

def main():
    print("--- AVVIO BOT IMMOBILIARE GIANCANI (META BLOCCATO -> CONVOGLIATO SU TELEGRAM) ---")
    
    try:
        df = pd.read_csv("posts.csv")
    except Exception as e:
        print(f"❌ Errore lettura CSV: {e}")
        sys.exit(1)

    today = datetime.now().strftime("%d/%m/%Y")
    print(f"📅 Data di oggi: {today}")

    todays_post = df[df['Data'] == today]

    if todays_post.empty:
        print("📭 Nessun post programmato per oggi nel CSV.")
        sys.exit(0)

    row = todays_post.iloc[0]
    messaggio_post = row['Testo']
    nome_file_immagine = row['File']
    
    print(f"📝 Testo trovato: {messaggio_post[:30]}...")
    print(f"🖼️ File immagine: {nome_file_immagine}")

    image_url = get_image_url_from_github(nome_file_immagine)
    
    # Convoglia su Telegram
    post_to_facebook(messaggio_post, image_url)

if __name__ == "__main__":
    main()
