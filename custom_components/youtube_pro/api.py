import requests
import json
import re
from http.cookiejar import MozillaCookieJar
import logging

_LOGGER = logging.getLogger(__name__)

class YouTubeAPI:
    def __init__(self, cookie_file):
        self.cookie_file = cookie_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self._load_cookies()

    def _load_cookies(self):
        try:
            cj = MozillaCookieJar(self.cookie_file)
            cj.load(ignore_discard=True, ignore_expires=True)
            self.session.cookies.update(cj)
            _LOGGER.info("YouTube Pro: Cookies loaded successfully.")
        except Exception as e:
            _LOGGER.error(f"YouTube Pro: Failed to load cookies from {self.cookie_file}: {e}")

    def fetch_data(self):
        data = {
            "account_name": "Unknown",
            "notifications_count": 0,
            "watch_later_count": 0,
            "watching_now": None,
            "live_now_count": 0,
            "live_channels": []
        }
        
        try:
            r = self.session.get("https://www.youtube.com/")
            match = re.search(r'ytInitialData\s*=\s*({.*?});', r.text)
            if not match:
                return data
            
            yt_data = json.loads(match.group(1))
            
            # Account name
            try:
                topbar = yt_data['header']['ytdMasthead']['topbar']['ytdTopbarRenderer']['topbarButtons']
                for btn in topbar:
                    if 'topbarMenuButtonRenderer' in btn:
                        data['account_name'] = btn['topbarMenuButtonRenderer'].get('tooltip', 'Unknown Account')
                    # Notifications
                    if 'notificationTopbarButtonRenderer' in btn:
                        notif_count = btn['notificationTopbarButtonRenderer'].get('notificationCount', 0)
                        data['notifications_count'] = int(notif_count) if str(notif_count).isdigit() else 0
            except:
                pass
                
            # Parse feed for Watch Later / Live / Recent
            try:
                tabs = yt_data['contents']['twoColumnBrowseResultsRenderer']['tabs']
                rich_grid = tabs[0]['tabRenderer']['content']['richGridRenderer']['contents']
                for item in rich_grid:
                    if 'richItemRenderer' in item:
                        content = item['richItemRenderer']['content']
                        if 'videoRenderer' in content:
                            vid = content['videoRenderer']
                            # Check if Live
                            badges = vid.get('badges', [])
                            for badge in badges:
                                if badge.get('metadataBadgeRenderer', {}).get('label') == 'LIVE NOW':
                                    data['live_now_count'] += 1
                                    data['live_channels'].append(vid.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown'))
                            # First video is likely "watching now" or recent history if we scrape /feed/history instead
                            if not data['watching_now']:
                                data['watching_now'] = vid.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
            except:
                pass

        except Exception as e:
            _LOGGER.error(f"YouTube Pro: API Error - {e}")
            
        return data
