# AI Kupon Posteri Üretimi + Instagram/TikTok/X Otomasyonu (Windows)

Bu proje, [`ornek.jpeg`](ornek.jpeg) benzeri “günün kuponu” tarzı görselleri üretip sosyal medyada otomatik dağıtmak için tasarlandı.

## Hedef

- [`ornek.jpeg`](ornek.jpeg) stilinde 1080x1920 kupon görseli üretimi
- Ücretsiz/low-cost model seçenekleri ile AI görsel üretimi
- Instagram + TikTok + X dağıtım hattı
- Windows'ta tek tık veya zamanlanmış otomatik çalışma

## Ana Bileşenler

- [`otomatik_kupon_windows.py`](otomatik_kupon_windows.py): Kupon posteri üretimi + dağıtım
- [`kupon_sablon.json`](kupon_sablon.json): İçerik şablonu (maçlar, oranlar, metinler)
- [`n8n_social_media_workflow.json`](n8n_social_media_workflow.json): n8n otomasyon akışı
- [`run_otomatik_kupon.bat`](run_otomatik_kupon.bat): Windows tek tık çalıştırma
- [`setup_windows_task.ps1`](setup_windows_task.ps1): Windows Görev Zamanlayıcı kurulumu

## Hızlı Kurulum (Windows)

```bat
pip install -r requirements.txt
copy .env.example .env
```

Sonra [` .env.example `](.env.example) içindeki değişkenleri [` .env `](.env) dosyasına doldurun.

## Kullanım

### 1) Sadece görsel üret

```bat
python otomatik_kupon_windows.py --config kupon_sablon.json --only-generate
```

Çıktı: [`output/gunun_kuponu.png`](output/gunun_kuponu.png)

### 2) Tam otomasyon (Instagram + TikTok webhook)

```bat
python otomatik_kupon_windows.py --config kupon_sablon.json
```

### 3) Tek tık `.bat`

```bat
run_otomatik_kupon.bat
```

## Ücretsiz GitHub Kaynakları

Detaylı repo listesi: [`FREE_GITHUB_REPOS.md`](FREE_GITHUB_REPOS.md)

## Önemli Notlar

- [` .env `](.env) dosyasını GitHub'a yüklemeyin.
- TikTok için bu projede webhook köprüsü yaklaşımı kullanılır (`TIKTOK_WEBHOOK_URL`).
- Instagram paylaşımı [`instagrapi`](requirements.txt) ile yapılır.
