"""
免費代理獲取工具
從免費代理網站獲取代理列表並測試可用性

警告：免費代理品質通常很差，建議使用付費代理
"""

import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_free_proxy_list():
    """從free-proxy-list.net獲取代理"""
    proxies = []
    try:
        print("正在從 free-proxy-list.net 獲取代理...")
        url = "https://free-proxy-list.net/"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        table = soup.find('table', {'class': 'table table-striped table-bordered'})
        if table:
            rows = table.find_all('tr')[1:]  # 跳過表頭
            for row in rows[:50]:  # 只取前50個
                cols = row.find_all('td')
                if len(cols) >= 7:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    https = cols[6].text.strip()
                    
                    protocol = 'https' if https == 'yes' else 'http'
                    proxy = f"{protocol}://{ip}:{port}"
                    proxies.append(proxy)
        
        print(f"✓ 獲取了 {len(proxies)} 個代理")
    except Exception as e:
        print(f"✗ 獲取代理失敗: {e}")
    
    return proxies


def test_proxy(proxy, timeout=5):
    """測試代理是否可用"""
    try:
        proxies_dict = {
            "http": proxy,
            "https": proxy
        }
        response = requests.get(
            "http://httpbin.org/ip",
            proxies=proxies_dict,
            timeout=timeout
        )
        if response.status_code == 200:
            return proxy, True, response.json().get('origin', 'Unknown')
        return proxy, False, None
    except:
        return proxy, False, None


def test_proxies(proxy_list, max_workers=10):
    """並行測試多個代理"""
    print(f"\n開始測試 {len(proxy_list)} 個代理...")
    print("這可能需要一些時間，請稍候...\n")
    
    working_proxies = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxy_list}
        
        completed = 0
        total = len(proxy_list)
        
        for future in as_completed(future_to_proxy):
            completed += 1
            proxy, is_working, ip = future.result()
            
            if is_working:
                working_proxies.append(proxy)
                print(f"[{completed}/{total}] ✓ {proxy} (IP: {ip})")
            else:
                print(f"[{completed}/{total}] ✗ {proxy}", end='\r')
    
    print(f"\n\n測試完成！")
    print(f"可用代理: {len(working_proxies)}/{len(proxy_list)}")
    
    return working_proxies


def save_proxies(proxies, filename="proxies_working.txt"):
    """保存代理到檔案"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for proxy in proxies:
                f.write(proxy + '\n')
        print(f"\n✓ 代理已保存到 {filename}")
        return True
    except Exception as e:
        print(f"\n✗ 保存失敗: {e}")
        return False


def main():
    print("="*60)
    print("免費代理獲取與測試工具")
    print("="*60)
    print("\n⚠️  警告：免費代理通常不穩定，建議使用付費代理")
    print()
    
    # 獲取代理
    proxies = get_free_proxy_list()
    
    if not proxies:
        print("\n✗ 沒有獲取到任何代理")
        return
    
    # 測試代理
    working_proxies = test_proxies(proxies)
    
    if working_proxies:
        # 保存可用代理
        save_proxies(working_proxies)
        
        print("\n" + "="*60)
        print("可用的代理：")
        print("="*60)
        for i, proxy in enumerate(working_proxies, 1):
            print(f"{i}. {proxy}")
    else:
        print("\n✗ 沒有找到可用的代理")
        print("建議：")
        print("1. 稍後再試")
        print("2. 使用付費代理服務")
        print("3. 使用VPN")


if __name__ == "__main__":
    main()
