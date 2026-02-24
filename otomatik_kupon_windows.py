"""
X ve Telegram Paylaşım
=======================
gorsel/ klasöründeki görselleri X ve Telegram'a paylaşır.

Kullanım:
    python otomatik_kupon_windows.py                            # gorsel/'deki son görseli paylaş
    python otomatik_kupon_windows.py --gorsel gorsel/kupon.png  # belirli görseli paylaş
    python otomatik_kupon_windows.py --metin "özel metin"       # özel metin ile paylaş
    python otomatik_kupon_windows.py --config kupon_sablon.json # JSON config'den metin al
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

import requests
import tweepy
from dotenv import load_dotenv

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
TWITTER_BEARER = os.getenv("TWITTER_BEARER")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

GORSEL_KLASORU = Path("gorsel")


# ── X (Twitter) ─────────────────────────────────────────────────────────────

def post_to_x(image_path: str, text: str) -> str:
    """X'e görsel ile paylaşım yap."""
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET,
                TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET, TWITTER_BEARER]):
        return "X atlandi: API bilgileri eksik."
    try:
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY, TWITTER_API_SECRET,
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET,
        )
        api_v1 = tweepy.API(auth)
        media = api_v1.media_upload(filename=image_path)

        client = tweepy.Client(
            bearer_token=TWITTER_BEARER,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET,
        )
        resp = client.create_tweet(text=text, media_ids=[media.media_id_string])
        tweet_id = resp.data["id"]
        return f"X paylaşımı başarılı: https://x.com/i/status/{tweet_id}"
    except Exception as exc:
        return f"X hatası: {exc}"


def post_x_metin(text: str) -> str:
    """X'e yalnızca metin paylaş."""
    if not all([TWITTER_API_KEY, TWITTER_API_SECRET,
                TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET, TWITTER_BEARER]):
        return "X atlandi: API bilgileri eksik."
    try:
        client = tweepy.Client(
            bearer_token=TWITTER_BEARER,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_SECRET,
        )
        resp = client.create_tweet(text=text)
        tweet_id = resp.data["id"]
        return f"X paylaşımı başarılı: https://x.com/i/status/{tweet_id}"
    except Exception as exc:
        return f"X hatası: {exc}"


# ── Telegram ─────────────────────────────────────────────────────────────────

def post_to_telegram(image_path: str, text: str) -> str:
    """Telegram'a görsel ile paylaşım yap."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return "Telegram atlandi: TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID eksik."
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        with open(image_path, "rb") as photo:
            resp = requests.post(
                url,
                data={"chat_id": TELEGRAM_CHAT_ID, "caption": text},
                files={"photo": photo},
                timeout=30,
            )
        if resp.status_code == 200:
            return "Telegram paylaşımı başarılı."
        return f"Telegram hatası: HTTP {resp.status_code} — {resp.text}"
    except Exception as exc:
        return f"Telegram hatası: {exc}"


def post_telegram_metin(text: str) -> str:
    """Telegram'a yalnızca metin gönder."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return "Telegram atlandi: TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID eksik."
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        resp = requests.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=30,
        )
        if resp.status_code == 200:
            return "Telegram mesajı başarılı."
        return f"Telegram hatası: HTTP {resp.status_code} — {resp.text}"
    except Exception as exc:
        return f"Telegram hatası: {exc}"


# ── Yardımcı Fonksiyonlar ────────────────────────────────────────────────────

def gorsel_sec(gorsel_yolu: Optional[str] = None) -> Optional[Path]:
    """gorsel/ klasöründen görsel seç. Belirtilmezse en son eklenen alınır."""
    if gorsel_yolu:
        p = Path(gorsel_yolu)
        return p if p.exists() else None

    GORSEL_KLASORU.mkdir(exist_ok=True)
    uzantilar = {".png", ".jpg", ".jpeg"}
    gorseller = sorted(
        [f for f in GORSEL_KLASORU.iterdir() if f.suffix.lower() in uzantilar],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    return gorseller[0] if gorseller else None


def build_caption(config_path: str = "kupon_sablon.json") -> str:
    """JSON config dosyasından paylaşım metnini oluştur."""
    try:
        with open(config_path, "r", encoding="utf-8") as fp:
            config = json.load(fp)
        social = config.get("social", {})
        caption = social.get("caption", "")
        hashtags = " ".join(social.get("hashtags", []))
        return f"{caption}\n\n{hashtags}".strip()
    except Exception:
        return ""


def paylas(image_path: str, text: str) -> dict:
    """X ve Telegram'a görsel ile paylaşım yap."""
    return {
        "x": post_to_x(image_path, text),
        "telegram": post_to_telegram(image_path, text),
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="X ve Telegram'a görsel paylaşım")
    parser.add_argument(
        "--gorsel",
        help="Paylaşılacak görsel yolu (belirtilmezse gorsel/ klasöründen son alınır)",
    )
    parser.add_argument("--metin", default="", help="Paylaşım metni")
    parser.add_argument(
        "--config",
        default="kupon_sablon.json",
        help="JSON config dosyası (metin için)",
    )
    args = parser.parse_args()

    gorsel = gorsel_sec(args.gorsel)
    if gorsel is None:
        print("HATA: Görsel bulunamadı. gorsel/ klasörüne görsel ekleyin.")
        sys.exit(1)

    metin = args.metin or build_caption(args.config) or "Günün paylaşımı!"

    print(f"Görsel : {gorsel}")
    print(f"Metin  : {metin[:80]}...")
    print()

    print("[1/2] X'e paylaşılıyor...")
    print(f"      {post_to_x(str(gorsel), metin)}")

    print("[2/2] Telegram'a paylaşılıyor...")
    print(f"      {post_to_telegram(str(gorsel), metin)}")


if __name__ == "__main__":
    main()
