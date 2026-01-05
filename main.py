import os
import pandas as pd
import requests
from datetime import datetime
import sys

# --- CONFIGURAZIONE ---
# Questi dati verranno letti dai "Segreti" di GitHub o dal tuo PC
# NON scrivere qui il token se condividi il codice con altri
FB_PAGE_ID = os.environ.get("FB_PAGE_ID") 
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")

# Impostazioni Repository GitHub (Modifica con il tuo nome utente e nome repo)
# Esempio: se il tuo user è "antonio-giancani" e la repo "social-bot"
GITHUB_USER = os.environ.get("GITHUB_REPOSITORY_OWNER") # Lo prende in automatico su GitHub
REPO_NAME = os.environ.get("GITHUB_REPOSITORY")         # Lo prende in automatico su GitHub
BRANCH = "main"                                         # Di solito è main o master

def get_image_url_from_github(filename):
    """Costruisce il link pubblico dell'immagine caricata su GitHub"""
    # Esempio: https://raw.githubusercontent.com/antoniogiancani/social-bot/main/images/Giorno_1.png
    base_url = f"https://raw.githubusercontent.com/{REPO_NAME}/{BRANCH}/images/{filename}"
    return base_url

def post_to_facebook(message, image_url):
    """Invia la foto e il testo alla Pagina Facebook"""
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    
    payload = {
        'url': image_url,       # Link dell'immagine
        'message': message,     # Testo del post (con hashtag)
        'access_token': FB_ACCESS_TOKEN
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # Solleva errore se qualcosa va storto
        print("✅ POST PUBBLICATO CON SUCCESSO SU FACEBOOK!")
        print(f"🆔 ID Post: {response.json().get('id')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ ERRORE FACEBOOK: {e}")
        if response is not None:
            print(f"Dettagli errore: {response.text}")
        sys.exit(1) # Ferma tutto con errore

def main():
    print("--- AVVIO BOT IMMOBILIARE GIANCANI ---")
    
    # 1. Carica il file CSV
    # Assicurati che il file si chiami esattamente posts.csv
    try:
        df = pd.read_csv("posts.csv")
    except Exception as e:
        print(f"❌ Errore lettura CSV: {e}")
        sys.exit(1)

    # 2. Che giorno è oggi?
    today = datetime.now().strftime("%d/%m/%Y") # Formato gg/mm/aaaa (es. 05/01/2026)
    print(f"📅 Data di oggi: {today}")

    # 3. Cerca la riga corrispondente a oggi
    # Filtra il file CSV cercando la colonna 'Data' uguale a 'today'
    todays_post = df[df['Data'] == today]

    if todays_post.empty:
        print("📭 Nessun post programmato per oggi nel CSV.")
        sys.exit(0) # Esce senza errori, semplicemente non c'è nulla da fare

    # 4. Estrae i dati dalla riga trovata
    row = todays_post.iloc[0]
    messaggio_post = row['Testo']
    nome_file_immagine = row['File'] # Es: Giorno_1.png
    
    print(f"📝 Testo trovato: {messaggio_post[:30]}...") # Stampa solo l'inizio
    print(f"🖼️ File immagine: {nome_file_immagine}")

    # 5. Ottieni il link dell'immagine
    image_url = get_image_url_from_github(nome_file_immagine)
    
    # 6. Pubblica su Facebook
    post_to_facebook(messaggio_post, image_url)

if __name__ == "__main__":
    main()
