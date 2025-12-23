<div align="center">

# TikTok Downloader CLI

**Terminal‑first TikTok downloader powered by ClipX**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Requests](https://img.shields.io/badge/Requests-HTTP-000000?style=for-the-badge)](https://requests.readthedocs.io/)
[![ClipX](https://img.shields.io/badge/ClipX-API-111827?style=for-the-badge)](https://clipx.zamdev.dev)

**[🌐 ClipX](https://clipx.zamdev.dev)** • **[📬 Telegram](https://zamdevio.t.me)** • **[🤖 Bot](https://t.me/TikTok_DownloaderiBot)**

</div>

---

## ✨ Features

- Download videos (standard/HD), audio (MP3), thumbnails
- Image posts with bulk/zip options
- Styled terminal UI with clean sections and menus
- Rate‑limit visibility + unlimited token support
- Works in Termux and desktop environments

---

## 🚀 Quick Start

### Requirements
- Python 3.8+
- `requests`

```bash
pip install requests
```

### Run
```bash
python3 TikTokDownloader.py
```

Optional: set a custom download folder
```bash
python3 TikTokDownloader.py /path/to/downloads
```

---

## 📂 Download Structure

```
<download_dir>/
  video/
    standard/
    hd/
  audio/
  thumbnail/
```

---

## 🔑 Unlimited Token

Create a `.unlimited` file in the same folder as the script:
```
<your_token_here>
```

Tokens are issued by ClipX. Request one via email: `clipx@zamdev.dev`.

---

## 📊 Rate Limits

The tool can display your per‑minute and daily limits and reset times using the API.

---

## 🔗 Links

- ClipX: https://clipx.zamdev.dev
- Telegram: https://zamdevio.t.me
- Telegram Bot: https://t.me/TikTok_DownloaderiBot
- GitHub: https://github.com/zamdevio
