# Görsel Üret → X + TikTok Paylaş (N8N Workflow)

```
[Metin] → [Hugging Face] → [Görsel] → X (Twitter) paylaşım
                                ↓
                          [FFmpeg 9:16 Video] → TikTok paylaşım
```

---

## Gerekli 3 API

### 1. Hugging Face (Görsel üretimi)
- **Link:** https://huggingface.co/settings/tokens
- **Key:** `.env` içine `HF_API_KEY=...` olarak ekle
- **Limit:** Ayda ~30.000 istek, ücretsiz

### 2. X (Twitter) API
- **Başvuru:** https://developer.twitter.com/en/portal/petition/essential/basic-info
- **App oluştur:** https://developer.twitter.com/en/portal/projects-and-apps
- **Yapılacaklar:**
  1. Linke git, developer hesabı aç (Free plan)
  2. "Create Project" → ad: `ai-art-bot`
  3. "Keys and Tokens" sekmesinden şunları kaydet:
     - API Key
     - API Secret
     - Client ID
     - Client Secret
  4. "User authentication settings" → OAuth 2.0 aç:
     - Callback URL: `http://localhost:5678/rest/oauth2-credential/callback`
- **Limit:** Ayda 1.500 tweet, ücretsiz

### 3. TikTok API
- **Başvuru:** https://developers.tiktok.com/
- **Yapılacaklar:**
  1. Linke git, "Manage apps" → "Create app" (Sandbox modunda başla)
  2. App adı: `ai-art-publisher`
  3. "Add products" → "Content Posting API" ekle
  4. Scope: `video.publish` izni ekle
  5. "Keys" sekmesinden **Client Key** ve **Client Secret** kaydet
  6. Redirect URI: `http://localhost:5678/rest/oauth2-credential/callback`
- **Limit:** Sandbox: günde 5 video; Onaylanınca sınırsız, ücretsiz

---

## Kurulum (5 Dakika)

### 1. Python bağımlılıkları
```bash
pip install flask pillow requests
```

### 2. FFmpeg kur
- **Windows:** https://www.gyan.dev/ffmpeg/builds/ → "essentials" zip indir → `C:\ffmpeg` çıkar → PATH'e `C:\ffmpeg\bin` ekle
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

### 3. N8N kur
```bash
npm install n8n -g
n8n start
# http://localhost:5678 açılır
```

---

## N8N'de Credential Ekleme

### Hugging Face
1. N8N → Settings → Credentials → Add Credential
2. Tip: **Header Auth**
3. Name: `Hugging Face API`
4. Header Name: `Authorization`
5. Header Value: `Bearer <HF_API_KEY>`

### X (Twitter)
1. Credentials → Add → **Twitter OAuth2 API**
2. Client ID ve Client Secret gir
3. "Connect" tıkla, hesabını bağla

### TikTok
1. Credentials → Add → **Header Auth**
2. Name: `TikTok API`
3. Header Name: `Authorization`
4. Header Value: `Bearer TIKTOK_ACCESS_TOKENIN`

(Access token almak için TikTok OAuth akışını çalıştırman gerekir - N8N'deki OAuth2 credential ile otomatik olur)

---

## Çalıştırma

```bash
# Terminal 1: Video sunucusu
python video_server.py

# Terminal 2: Test et
python test_pipeline.py

# Terminal 3: N8N
n8n start
```

1. http://localhost:5678 aç
2. Import → `n8n_social_media_workflow.json` seç
3. Her node'a tıkla, credential'ı bağla
4. "Execute Workflow" bas

---

## Hata Durumları

| Hata | Çözüm |
|------|-------|
| "Model is loading" | 30-60 sn bekle, tekrar dene |
| "Rate limit exceeded" | 15 dk bekle |
| "FFmpeg not found" | PATH'e ekle, CMD'de `ffmpeg -version` kontrol |
| Video sunucusu bağlanmıyor | `python video_server.py` çalıştır |
| Twitter 403 | Developer portal'dan izinleri kontrol et |
| TikTok sandbox limit | Günde max 5 video, ertesi gün sıfırlanır |

---

## Windows Tek Tık + Otomatik Çalışma

### Tek tık çalıştırma

```bat
run_otomatik_kupon.bat
```

Bu komut sırasıyla:
- bağımlılıkları kurar,
- [`kupon_sablon.json`](kupon_sablon.json) ile görseli üretir,
- Instagram ve TikTok dağıtım adımlarını tetikler.

### Günlük otomatik görev oluşturma

PowerShell'i proje klasöründe açıp:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup_windows_task.ps1 -TaskName AIKuponOtomasyon -RunAt 10:00
```

Bu işlem Windows Task Scheduler'a günlük bir görev ekler ve [`run_otomatik_kupon.bat`](run_otomatik_kupon.bat) dosyasını çalıştırır.
