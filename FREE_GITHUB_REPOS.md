# Ucretsiz GitHub Repo Arastirmasi (Gorsel Uretim + Sosyal Medya)

Bu listedeki projeler, Windows'ta yerel kurulum veya API tabanli entegrasyon icin uygundur.

## 1) Gorsel Uretimi

### 1. [`AUTOMATIC1111/stable-diffusion-webui`](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- En populer Stable Diffusion arayuzu.
- Yerel GPU ile calisir, API eklentileriyle otomasyona uygundur.
- Ucretsiz (donanim maliyeti haric).

### 2. [`comfyanonymous/ComfyUI`](https://github.com/comfyanonymous/ComfyUI)
- Dugum tabanli gelismis uretim pipeline'i.
- Stil kontrolu, batching, otomasyon senaryolari icin cok uygun.
- Ucretsiz ve topluluk destegi guclu.

### 3. [`invoke-ai/InvokeAI`](https://github.com/invoke-ai/InvokeAI)
- Kolay kurulum, modern UI, profesyonel workflow'lar.
- Inpainting/outpainting destegi ile tasarim kalitesini arttirir.

### 4. [`Stability-AI/stablediffusion`](https://github.com/Stability-AI/stablediffusion)
- Stable Diffusion cekirdek kaynak kodu.
- Dogrudan model tabanli gelistirme yapmak isteyenler icin.

### 5. [`huggingface/diffusers`](https://github.com/huggingface/diffusers)
- Python tarafinda model calistirma/ince ayar icin standart kutuphane.
- Bu projedeki scriptler ile kolay entegre olur.

### 6. [`black-forest-labs/flux`](https://github.com/black-forest-labs/flux)
- FLUX model ailesi altyapisi (ekosistem dokumantasyonu/model kartlari).
- Kaliteli poster/ilustrasyon uretiminde populer.

## 2) Sosyal Medya Otomasyonu

### 1. [`n8n-io/n8n`](https://github.com/n8n-io/n8n)
- Acik kaynak otomasyon platformu.
- Webhook + schedule + sosyal medya workflow'lari icin ideal.

### 2. [`subzeroid/instagrapi`](https://github.com/subzeroid/instagrapi)
- Python ile Instagram medya yukleme.
- Bu projede dogrudan kullaniliyor.

### 3. [`tweepy/tweepy`](https://github.com/tweepy/tweepy)
- X/Twitter API icin Python kutuphanesi.
- Projedeki mevcut X paylasim scriptleri bununla uyumlu.

### 4. [`TikTok/tiktok-opensdk`](https://github.com/TikTok/tiktok-opensdk)
- TikTok resmi gelistirici ekosistemi baglantilari.
- Icerik paylasim API surecine referans dokumantasyon sunar.

## Bu Projede Onerilen Strateji

1. Hizli baslangic: Hugging Face inference (ucretsiz kota) + [`otomatik_kupon_windows.py`](otomatik_kupon_windows.py)
2. Daha yuksek kalite/ozellestirme: ComfyUI veya A1111 lokal kuruluma gecis
3. Dagitim: Instagram icin instagrapi, TikTok icin webhook (n8n/Make/custom API), X icin Tweepy

