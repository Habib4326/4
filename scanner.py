import json
import requests
import re
from urllib.parse import urljoin

def extract_m3u_from_livetv():
    """
    http://198.195.239.50/ থেকে M3U লিংক এক্সট্রাক্ট করুন
    """
    base_url = "http://198.195.239.50/"
    
    print("\n" + "="*70)
    print("  📺 LiveTV M3U Extractor v2.0")
    print("="*70)
    print(f"\n  🌐 Target URL: {base_url}")
    
    try:
        # 1. প্রধান পেজ ডাউনলোড করুন
        print("\n  ⏳ Fetching main page...")
        response = requests.get(base_url, timeout=15)
        response.raise_for_status()
        html_content = response.text
        
        print(f"  ✅ Page loaded ({len(html_content)} bytes)")
        
        # 2. JSON ফাইল খুঁজুন
        print("\n  🔍 Looking for JSON files...")
        json_urls = []
        
        json_patterns = [
            r'fetch\s*\(\s*["\']([^"\']+\.json)["\']\s*\)',
            r'src\s*=\s*["\']([^"\']+\.json)["\']',
            r'href\s*=\s*["\']([^"\']+\.json)["\']',
            r'url\s*:\s*["\']([^"\']+\.json)["\']',
            r'"([^"]+\.json)"',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, html_content)
            for match in matches:
                if match not in json_urls:
                    json_urls.append(match)
        
        print(f"\n  📄 Found JSON files: {json_urls}")
        
        # 3. tv_channels.json চেক করুন
        tv_json = None
        for j in json_urls:
            if 'channel' in j.lower() or 'tv' in j.lower():
                tv_json = j
                break
        
        if tv_json:
            json_url = urljoin(base_url, tv_json)
            print(f"\n  📥 Found channels JSON: {json_url}")
            
            try:
                json_response = requests.get(json_url, timeout=10)
                json_response.raise_for_status()
                data = json_response.json()
                
                channels = data.get("channels", [])
                print(f"\n  📊 Found {len(channels)} channels")
                
                m3u_lines = ["#EXTM3U"]
                m3u_lines.append(f"# Playlist generated from {base_url}")
                m3u_lines.append(f"# Total channels: {len(channels)}")
                m3u_lines.append("")
                
                for ch in channels:
                    if ch.get("status") == "hidden":
                        continue
                    
                    name = ch.get("name", "Unknown")
                    url = ch.get("url", "")
                    logo = ch.get("logo", "")
                    category = ch.get("category", "Other")
                    
                    if not url:
                        continue
                    
                    if not url.startswith('http'):
                        url = urljoin(base_url, url)
                    
                    extinf = f'#EXTINF:-1 group-title="{category}" logo="{logo}",{name}'
                    m3u_lines.append(extinf)
                    m3u_lines.append(url)
                
                m3u_content = "\n".join(m3u_lines)
                
                filename = "livetv_channels.m3u"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(m3u_content)
                
                print(f"\n  ✅ M3U saved to: {filename}")
                return m3u_content
                
            except json.JSONDecodeError:
                print("  ❌ Invalid JSON format!")
            except requests.exceptions.RequestException as e:
                print(f"  ❌ JSON download error: {e}")
        else:
            print("\n  ⚠️ No channels.json found!")
            print("  🔍 Searching for channel data in HTML...")
            
            channel_pattern = r'\{[^}]*"name"[^}]*"url"[^}]*\}'
            channel_data = re.findall(channel_pattern, html_content)
            
            if channel_data:
                print(f"  📊 Found {len(channel_data)} channel entries")
                
                m3u_lines = ["#EXTM3U"]
                for ch_json in channel_data:
                    try:
                        ch = json.loads(ch_json)
                        name = ch.get("name", "Unknown")
                        url = ch.get("url", "")
                        logo = ch.get("logo", "")
                        category = ch.get("category", "Other")
                        
                        if url:
                            extinf = f'#EXTINF:-1 group-title="{category}" logo="{logo}",{name}'
                            m3u_lines.append(extinf)
                            m3u_lines.append(url)
                    except:
                        continue
                
                m3u_content = "\n".join(m3u_lines)
                filename = "livetv_channels.m3u"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(m3u_content)
                
                print(f"\n  ✅ M3U saved to: {filename}")
                return m3u_content
            
    except requests.exceptions.RequestException as e:
        print(f"\n  ❌ Connection error: {e}")
    
    return None

def main():
    # গিটহাব অ্যাকশনের জন্য সরাসরি মেইন এক্সট্রাক্টর রান হবে
    extract_m3u_from_livetv()

if __name__ == "__main__":
    main()