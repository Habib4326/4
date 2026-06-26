import json
import requests
import re
from urllib.parse import urljoin

# =====================================================================
# SCRIP 1: LIVETV EXTRACTOR (IP: 198.195.239.50)
# =====================================================================
def extract_m3u_from_livetv():
    base_url = "http://198.195.239.50/"
    print("\n" + "="*70)
    print("  📺 [1/2] LiveTV M3U Extractor v2.0")
    print("="*70)
    
    try:
        print("  ⏳ Fetching LiveTV main page...")
        response = requests.get(base_url, timeout=15)
        response.raise_for_status()
        html_content = response.text
        
        json_urls = []
        json_patterns = [
            r'fetch\s*\(\s*["\']([^"\']+\.json)["\']\s*\)',
            r'src\s*=\s*["\']([^"\']+\.json)["\']',
            r'href\s*=\s*["\']([^"\']+\.json)["\']',
            r'"([^"]+\.json)"',
        ]
        for pattern in json_patterns:
            matches = re.findall(pattern, html_content)
            for match in matches:
                if match not in json_urls:
                    json_urls.append(match)
        
        tv_json = None
        for j in json_urls:
            if 'channel' in j.lower() or 'tv' in j.lower():
                tv_json = j
                break
        
        if tv_json:
            json_url = urljoin(base_url, tv_json)
            try:
                json_response = requests.get(json_url, timeout=10)
                json_response.raise_for_status()
                data = json_response.json()
                channels = data.get("channels", [])
                
                m3u_lines = ["#EXTM3U\n# Generated from LiveTV"]
                for ch in channels:
                    if ch.get("status") == "hidden": continue
                    name = ch.get("name", "Unknown")
                    url = ch.get("url", "")
                    logo = ch.get("logo", "")
                    category = ch.get("category", "Other")
                    if not url: continue
                    if not url.startswith('http'): url = urljoin(base_url, url)
                    
                    m3u_lines.append(f'#EXTINF:-1 group-title="{category}" logo="{logo}",{name}\n{url}')
                
                with open("livetv_channels.m3u", 'w', encoding='utf-8') as f:
                    f.write("\n".join(m3u_lines))
                print("  ✅ M3U saved to: livetv_channels.m3u")
            except Exception as e:
                print(f"  ❌ LiveTV JSON Error: {e}")
        else:
            print("  ⚠️ No channels.json found on LiveTV!")
    except Exception as e:
        print(f"  ❌ LiveTV Connection error: {e}")

# =====================================================================
# SCRIPT 2: TEXAS TV EXTRACTOR (IP: 10.99.99.99)
# =====================================================================
def extract_texas_stream_url(player_url):
    try:
        response = requests.get(player_url, timeout=10)
        html = response.text
        patterns = [
            r'file\s*:\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
            r'src\s*=\s*["\']([^"\']+\.m3u8[^"\']*)["\']',
            r'["\']([^"\']+\.m3u8[^"\']*)["\']',
        ]
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                url = matches[0]
                if not url.startswith('http'): url = urljoin('http://10.99.99.99/', url)
                return url
        return None
    except:
        return None

def extract_all_texas_channels():
    base_url = "http://10.99.99.99/"
    print("\n" + "="*70)
    print("  📺 [2/2] TEXAS TV - Real Stream URL Extractor")
    print("="*70)
    
    try:
        print("  ⏳ Fetching Texas TV main page...")
        response = requests.get(base_url, timeout=10)
        html = response.text
        
        li_pattern = r'<li class="([^"]+)">\s*<a[^>]*onclick="view\.location\.href=\'([^\']+)\'"[^>]*>\s*<img src="([^"]+)" alt="([^"]+)"'
        matches = re.findall(li_pattern, html)
        print(f"  📊 Found {len(matches)} channels on Texas TV.")
        
        m3u_lines = ["#EXTM3U\n# Generated from Texas TV"]
        
        for match in matches:
            classes, stream_url, img_src, name = match[0].split(), match[1], match[2], match[3]
            category = "Other"
            for cls in classes:
                if cls not in ['All', 'channel']:
                    category = cls
                    break
            
            player_full_url = urljoin(base_url, stream_url)
            real_url = extract_texas_stream_url(player_full_url)
            
            if real_url:
                m3u_lines.append(f'#EXTINF:-1 group-title="{category}" logo="{urljoin(base_url, img_src)}",{name}\n{real_url}')
                print(f"    ✅ Found: {name}")
            else:
                print(f"    ❌ No stream for: {name}")
                
        with open("texas_tv_real.m3u", 'w', encoding='utf-8') as f:
            f.write("\n".join(m3u_lines))
        print("  ✅ M3U saved to: texas_tv_real.m3u")
    except Exception as e:
        print(f"  ❌ Texas TV Connection error: {e}")

# =====================================================================
# MAIN RUNNER
# =====================================================================
if __name__ == "__main__":
    # ১ নম্বর স্ক্রিপ্ট রান হবে
    extract_m3u_from_livetv()
    
    # ২ নম্বর স্ক্রিপ্ট রান হবে
    extract_all_texas_channels()
