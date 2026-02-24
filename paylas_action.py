"""
GitHub Actions Paylaşım Script
================================
workflow_dispatch tetiklendiğinde çalışır.
Ortam değişkenlerinden tur/metin/image_url okur, X ve Telegram'a paylaşır.
"""

from __future__ import annotations

import os
import sys
import tempfile
import urllib.request
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otomatik_kupon_windows import (
    post_telegram_metin,
    post_to_telegram,
    post_to_x,
    post_x_metin,
)

PAYLAS_METINLER = {
    "gunun-kuponu":      "Oddsy'de Günün Banko Kuponu yayında!\n\noddsw.com.tr",
    "gunun-tercihleri":  "Oddsy'de Günün Tercihleri yayında!\n\noddsw.com.tr",
    "kupon-kazandi":     "Oddsy Günün Kuponu KAZANDI!\n\noddsw.com.tr",
    "editor-tercihleri": "Oddsy'de Editör Tercihleri yayında!\n\noddsw.com.tr",
    "editor-kazandi":    "Oddsy Editörün Tercihi KAZANDI!\n\noddsw.com.tr",
}

tur       = os.environ.get("PAYLAS_TUR", "").strip()
metin     = os.environ.get("PAYLAS_METIN", "").strip() or PAYLAS_METINLER.get(tur, "")
image_url = os.environ.get("PAYLAS_IMAGE_URL", "").strip()

if not tur or tur not in PAYLAS_METINLER:
    print(f"HATA: Geçersiz tür '{tur}'. Kabul edilenler: {list(PAYLAS_METINLER.keys())}")
    sys.exit(1)

if not metin:
    print("HATA: Metin bulunamadı.")
    sys.exit(1)

print(f"Tür   : {tur}")
print(f"Metin : {metin}")
print(f"Görsel: {image_url or '(yok)'}")

tmp_path = None
try:
    gorsel = None

    if image_url:
        print("Görsel indiriliyor...")
        try:
            suffix = ".jpg"
            clean = image_url.split("?")[0].split("/")[-1]
            if "." in clean:
                suffix = "." + clean.rsplit(".", 1)[-1]
            tmp_fd, tmp_path = tempfile.mkstemp(suffix=suffix)
            os.close(tmp_fd)
            req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                with open(tmp_path, "wb") as f:
                    f.write(resp.read())
            gorsel = tmp_path
            print(f"Görsel indirildi: {tmp_path}")
        except Exception as exc:
            print(f"Görsel indirilemedi: {exc} — görselsiz devam ediliyor.")
            gorsel = None

    if gorsel is None:
        # URL yoksa gorsel/ klasöründeki görseli kullan
        g = gorsel_sec(None)
        if g:
            gorsel = str(g)
            print(f"Görsel klasöründen alındı: {gorsel}")
        else:
            print("gorsel/ klasöründe görsel bulunamadı — görselsiz devam.")

    if gorsel:
        print("X'e görsel ile paylaşılıyor...")
        x_sonuc = post_to_x(str(gorsel), metin)
        print(f"Telegram'a görsel ile paylaşılıyor...")
        tg_sonuc = post_to_telegram(str(gorsel), metin)
    else:
        print("X'e metin olarak paylaşılıyor...")
        x_sonuc = post_x_metin(metin)
        print("Telegram'a metin olarak paylaşılıyor...")
        tg_sonuc = post_telegram_metin(metin)

    print(f"\n--- SONUÇ ---")
    print(f"X       : {x_sonuc}")
    print(f"Telegram: {tg_sonuc}")

finally:
    if tmp_path and os.path.exists(tmp_path):
        os.unlink(tmp_path)
