import requests
import json
import re
from http.cookiejar import MozillaCookieJar
import logging

_LOGGER = logging.getLogger(__name__)

class YouTubeAPI:
    def __init__(self, cookie_path):
        self.cookie_path = cookie_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self._load_cookies()

    def _load_cookies(self):
        try:
            cj = MozillaCookieJar(self.cookie_path)
            cj.load(ignore_discard=True, ignore_expires=True)
            self.session.cookies.update(cj)
            _LOGGER.info("YouTube Pro: Cookies loaded successfully.")
        except Exception as e:
            _LOGGER.error(f"YouTube Pro: Failed to load cookies: {e}")

    def _get_yt_data(self, url):
        try:
            r = self.session.get(url, timeout=10)
            match = re.search(r'ytInitialData\s*=\s*({.*?});', r.text)
            if match:
                return json.loads(match.group(1))
        except Exception as e:
            _LOGGER.error(f"YouTube Pro: Failed fetching {url} - {e}")
        return None

    def fetch_data(self):
        data = {
            "account_name": "Unknown",
            "account_email": "Unknown",
            "notifications_count": 0,
            "watch_later_count": 0,
            "subscriptions_count": 0,
            "watching_now": None,
            "live_now_count": 0,
            "live_channels": [],
            "recent_history": []
        }
        
        # 1. Home Page (Account, Notifications, Live, Watching Now)
        yt_home = self._get_yt_data("https://www.youtube.com/")
        if yt_home:
            try:
                topbar = yt_home['header']['ytdMasthead']['topbar']['ytdTopbarRenderer']['topbarButtons']
                for btn in topbar:
                    # Account
                    if 'topbarMenuButtonRenderer' in btn:
                        data['account_name'] = btn['topbarMenuButtonRenderer'].get('tooltip', 'Unknown Account')
                    # Notifications
                    if 'notificationTopbarButtonRenderer' in btn:
                        notif = btn['notificationTopbarButtonRenderer'].get('notificationCount', 0)
                        data['notifications_count'] = int(notif) if str(notif).isdigit() else 0
            except: pass

            try:
                tabs = yt_home['contents']['twoColumnBrowseResultsRenderer']['tabs']
                rich_grid = tabs[0]['tabRenderer']['content']['richGridRenderer']['contents']
                for item in rich_grid:
                    if 'richItemRenderer' in item:
                        vid = item['richItemRenderer']['content'].get('videoRenderer', {})
                        if not vid: continue
                        
                        badges = vid.get('badges', [])
                        for badge in badges:
                            if badge.get('metadataBadgeRenderer', {}).get('label') == 'LIVE NOW':
                                data['live_now_count'] += 1
                                data['live_channels'].append(vid.get('ownerText', {}).get('runs', [{}])[0].get('text', 'Unknown'))
                        
                        if not data['watching_now']:
                            data['watching_now'] = vid.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
            except: pass

        # 2. Watch Later
        yt_wl = self._get_yt_data("https://www.youtube.com/playlist?list=WL")
        if yt_wl:
            try:
                stats = yt_wl['header']['playlistHeaderRenderer']['stats']
                for stat in stats:
                    if 'videos' in stat.get('runs', [{}])[0].get('text', ''):
                        count_str = stat['runs'][0]['text'].replace(',', '').replace('videos', '').strip()
                        data['watch_later_count'] = int(count_str) if count_str.isdigit() else 0
            except: pass

        # 3. Subscriptions
        yt_subs = self._get_yt_data("https://www.youtube.com/feed/channels")
        if yt_subs:
            try:
                contents = yt_subs['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']
                count = 0
                for c in contents:
                    if 'itemSectionRenderer' in c:
                        grid = c['itemSectionRenderer']['contents'][0].get('gridRenderer', {}).get('items', [])
                        count += len(grid)
                data['subscriptions_count'] = count
            except: pass

        # 4. History
        yt_hist = self._get_yt_data("https://www.youtube.com/feed/history")
        if yt_hist:
            try:
                contents = yt_hist['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']
                hist_items = contents[0]['itemSectionRenderer']['contents']
                for item in hist_items:
                    if 'videoRenderer' in item:
                        title = item['videoRenderer'].get('title', {}).get('runs', [{}])[0].get('text', 'Unknown')
                        channel = item['videoRenderer'].get('longBylineText', {}).get('runs', [{}])[0].get('text', 'Unknown')
                        data['recent_history'].append(f"{title} ({channel})")
                        if len(data['recent_history']) >= 5: break
            except: pass

        return data