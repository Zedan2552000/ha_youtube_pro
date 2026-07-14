# YouTube Pro (Innertube API) 📺🚀

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

The ultimate Home Assistant custom component for YouTube. Instead of relying on slow scrapers, this integration uses a `cookies.txt` file to natively query YouTube's internal Innertube API (`pbj=1`).

## 🌟 Features Extractable
- **Account Info:** Your YouTube Account Name.
- **Currently Watching:** Real-time extraction of what you are viewing.
- **Unread Notifications:** Scrapes the bell icon for new channel uploads.
- **Live Streams:** Detects which of your subscribed channels are currently live.
- **Watch Later:** Tracks the count of your saved videos.
- **Subscriptions:** Total number of channels you are subscribed to.
- **Recent History:** Your last 5 watched videos.

## 🍪 How to Get Your Cookies (CRITICAL TRICK)
To prevent your YouTube cookies from expiring quickly, you **MUST** extract them using an Incognito/Private window. If you extract them from your normal browser session, they will expire as soon as you log out or clear data.

1. Install the [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) extension.
2. Open a **New Incognito / Private Window** in your browser.
3. Go to [YouTube](https://www.youtube.com/) and Log in to your account.
4. Click the extension icon and export your cookies.
5. Save the file as `youtube_cookies.txt` and place it in your Home Assistant `/config` folder.
6. You can now close the incognito window, and the cookies will remain valid for a very long time!

## 🛠️ Installation
1. Add this repository to HACS as a `Custom Repository` (Integration).
2. Download and Restart Home Assistant.
3. Go to **Settings > Devices & Services > Add Integration**.
4. Search for `YouTube Pro`.
5. Enter the path to your cookies file (e.g., `/config/youtube_cookies.txt`).

## 📄 License
MIT License