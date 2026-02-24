"""
Website Entegrasyonu - Flask API
==================================
Website'den gelen kupon ve tercih paylaşımlarını X ve Telegram'a iletir.

Kurulum:
    pip install flask flask-cors

Çalıştırma:
    python web_server.py

Endpointler:
    POST /api/kupon          → kupon paylaşımı (gorsel + metin)
    POST /api/tercih         → tercih paylaşımı (metin + opsiyonel gorsel)
    POST /api/paylas         → tur bazlı paylaşım (admin panel dropdown)
    GET  /health             → durum kontrolü

Örnek İstekler:
    # Günün kuponunu paylaş
    curl -X POST http://localhost:5000/api/paylas \
         -H "Content-Type: application/json" \
         -d '{"tur": "gunun-kuponu"}'

    # Kupon paylaş (gorsel/ klasöründeki son görsel ile)
    curl -X POST http://localhost:5000/api/kupon \
         -H "Content-Type: application/json" \
         -d '{"metin": "Bugünün kuponu!"}'

    # WEB_API_KEY varsa header ekle
    curl -X POST http://localhost:5000/api/paylas \
         -H "X-API-Key: gizli_anahtar" \
         -H "Content-Type: application/json" \
         -d '{"tur": "gunun-tercihleri"}'
"""

from __future__ import annotations

import os
import sys
import tempfile
import urllib.request

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from otomatik_kupon_windows import (
    build_caption,
    gorsel_sec,
    post_telegram_metin,
    post_to_telegram,
    post_to_x,
    post_x_metin,
)

load_dotenv()

app = Flask(__name__)
CORS(app)  # Admin panel'den gelen cross-origin isteklere izin ver

# .env dosyasında WEB_API_KEY tanımlıysa istekler bu anahtarla doğrulanır.
# Boş bırakılırsa doğrulama devre dışı kalır.
API_KEY = os.getenv("WEB_API_KEY", "")

# Her paylaşım türü için varsayılan metin
PAYLAS_METINLER = {
    "gunun-kuponu":      "Oddsy'de Günün Banko Kuponu yayında!\n\noddsw.com.tr",
    "gunun-tercihleri":  "Oddsy'de Günün Tercihleri yayında!\n\noddsw.com.tr",
    "kupon-kazandi":     "Oddsy Günün Kuponu KAZANDI!\n\noddsw.com.tr",
    "editor-tercihleri": "Oddsy'de Editör Tercihleri yayında!\n\noddsw.com.tr",
    "editor-kazandi":    "Oddsy Editörün Tercihi KAZANDI!\n\noddsw.com.tr",
}


def _yetkili() -> bool:
    if not API_KEY:
        return True
    return request.headers.get("X-API-Key") == API_KEY


def _indir_gorsel(url: str) -> str | None:
    """URL'den görseli geçici dosyaya indir, dosya yolunu döndür."""
    try:
        suffix = ".jpg"
        clean = url.split("?")[0].split("/")[-1]
        if "." in clean:
            suffix = "." + clean.rsplit(".", 1)[-1]
        tmp_fd, tmp_path = tempfile.mkstemp(suffix=suffix)
        os.close(tmp_fd)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            with open(tmp_path, "wb") as f:
                f.write(resp.read())
        return tmp_path
    except Exception as exc:
        print(f"[indir_gorsel] Hata: {exc}")
        return None


# ── Endpointler ──────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/paylas", methods=["POST"])
def paylas():
    """
    Admin panel dropdown'dan tetiklenen paylaşım endpoint'i.

    Body (JSON):
        tur        : "gunun-kuponu" | "gunun-tercihleri" | "kupon-kazandi"
                     | "editor-tercihleri" | "editor-kazandi"  — zorunlu
        metin      : özel metin — opsiyonel, belirtilmezse türe göre varsayılan kullanılır
        image_url  : görsel URL — opsiyonel, belirtilmezse gorsel/ klasöründeki son görsel
    """
    if not _yetkili():
        return jsonify({"hata": "Yetkisiz istek."}), 401

    data = request.get_json(silent=True) or {}
    tur = data.get("tur", "").strip()

    if tur not in PAYLAS_METINLER:
        return jsonify({
            "hata": f"Geçersiz tür. Kabul edilen değerler: {list(PAYLAS_METINLER.keys())}"
        }), 400

    metin = data.get("metin") or PAYLAS_METINLER[tur]
    tmp_path = None

    try:
        image_url = data.get("image_url")
        if image_url:
            tmp_path = _indir_gorsel(image_url)

        gorsel = tmp_path or gorsel_sec(None)

        if gorsel is None:
            return jsonify({"hata": "Görsel bulunamadı. gorsel/ klasörüne bir görsel ekleyin."}), 400

        sonuc = {
            "tur": tur,
            "gorsel": str(gorsel),
            "x": post_to_x(str(gorsel), metin),
            "telegram": post_to_telegram(str(gorsel), metin),
        }
        return jsonify(sonuc)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception:
                pass


@app.route("/api/kupon", methods=["POST"])
def kupon_paylas():
    """
    Kupon paylaşımını tetikle.

    Body (JSON):
        gorsel  : dosya adı (gorsel/ klasöründe) — opsiyonel, belirtilmezse son görsel alınır
        metin   : paylaşım metni — opsiyonel, belirtilmezse kupon_sablon.json'dan alınır
    """
    if not _yetkili():
        return jsonify({"hata": "Yetkisiz istek."}), 401

    data = request.get_json(silent=True) or {}

    gorsel_adi = data.get("gorsel")
    gorsel = gorsel_sec(f"gorsel/{gorsel_adi}" if gorsel_adi else None)

    if gorsel is None:
        return jsonify({"hata": "gorsel/ klasöründe görsel bulunamadı."}), 400

    metin = data.get("metin") or build_caption() or "Günün kuponu!"

    return jsonify({
        "gorsel": str(gorsel),
        "x": post_to_x(str(gorsel), metin),
        "telegram": post_to_telegram(str(gorsel), metin),
    })


@app.route("/api/tercih", methods=["POST"])
def tercih_paylas():
    """
    Tercih paylaşımını tetikle.

    Body (JSON):
        metin   : paylaşım metni — zorunlu
        gorsel  : dosya adı (gorsel/ klasöründe) — opsiyonel
    """
    if not _yetkili():
        return jsonify({"hata": "Yetkisiz istek."}), 401

    data = request.get_json(silent=True) or {}
    metin = data.get("metin", "").strip()

    if not metin:
        return jsonify({"hata": "metin alanı zorunlu."}), 400

    gorsel_adi = data.get("gorsel")
    gorsel = gorsel_sec(f"gorsel/{gorsel_adi}" if gorsel_adi else None)

    if gorsel:
        x_sonuc = post_to_x(str(gorsel), metin)
        tg_sonuc = post_to_telegram(str(gorsel), metin)
    else:
        x_sonuc = post_x_metin(metin)
        tg_sonuc = post_telegram_metin(metin)

    return jsonify({
        "metin": metin,
        "gorsel": str(gorsel) if gorsel else None,
        "x": x_sonuc,
        "telegram": tg_sonuc,
    })


# ── Başlat ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    print(f"Web server başlatılıyor: http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
