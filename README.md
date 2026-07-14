# YouTube Pro (Innertube API) 📺🚀

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

The ultimate Home Assistant custom component for YouTube. Instead of relying on slow scrapers, this integration uses a `cookies.txt` file to natively query YouTube's internal Innertube API (`pbj=1`).

## 🌟 Features Extractable
- **Currently Watching:** Real-time extraction of what you are viewing.
- **Unread Notifications:** Scrapes the bell icon for new channel uploads.
- **Live Streams:** Detects which of your subscribed channels are currently live.
- **Watch Later:** Tracks the count and details of your saved videos.

## 🛠️ Installation
1. Add this repository to HACS as a `Custom Repository` (Integration).
2. Download and Restart Home Assistant.
3. Export your YouTube cookies using the `Get cookies.txt LOCALLY` Chrome extension.
4. Place the `cookies.txt` file in your Home Assistant `/config` folder.

## ⚙️ Configuration
In your `configuration.yaml`, add:
```yaml
youtube_pro:
  cookie_path: "/config/cookies.txt"
```

## 📄 License
MIT License
