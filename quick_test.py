"""
快速測試腳本 - 用於測試進階版功能
這會立即執行一次，不需要等待排程
"""

import sys
import os

# 導入主程式
from youtube_viewer_advanced import AdvancedYoutubeViewer


def main():
    print("="*60)
    print("YouTube 影片瀏覽器 - 快速測試")
    print("="*60)
    print()
    
    # 創建瀏覽器實例
    viewer = AdvancedYoutubeViewer()
    
    # ==================== 快速設定 ====================
    
    # 基本設定
    viewer.watch_duration = 30  # 測試用，只觀看30秒
    viewer.headless = False     # 顯示瀏覽器，方便觀察
    
    # 詢問用戶輸入影片URL
    print("請輸入要測試的YouTube影片URL：")
    print("範例：https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print()
    
    url = input("URL: ").strip()
    
    if not url:
        print("\n使用預設測試影片...")
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    viewer.add_video(url)
    
    # 詢問是否使用代理
    print("\n" + "="*60)
    print("是否使用代理？")
    print("1. 不使用（使用本機IP）")
    print("2. 使用 proxies.txt 中的代理")
    print("3. 手動輸入代理")
    print("="*60)
    
    choice = input("請選擇 (1/2/3) [預設:1]: ").strip() or "1"
    
    if choice == "2":
        if os.path.exists("proxies.txt"):
            viewer.load_proxies_from_file("proxies.txt")
        else:
            print("\n⚠ 找不到 proxies.txt，將不使用代理")
    elif choice == "3":
        proxy = input("\n請輸入代理 (例如: http://123.456.789.0:8080): ").strip()
        if proxy:
            viewer.add_proxy(proxy)
    
    # 詢問觀看時長
    print("\n" + "="*60)
    duration = input("觀看時長（秒）[預設:30]: ").strip()
    if duration and duration.isdigit():
        viewer.watch_duration = int(duration)
    print("="*60)
    
    # 確認設定
    print("\n" + "="*60)
    print("測試設定：")
    print(f"  影片: {url}")
    print(f"  觀看時長: {viewer.watch_duration}秒")
    print(f"  使用代理: {'是 (' + str(len(viewer.proxies)) + '個)' if viewer.proxies else '否'}")
    print(f"  顯示瀏覽器: {'是' if not viewer.headless else '否'}")
    print("="*60)
    print()
    
    input("按 Enter 開始測試...")
    
    # 立即執行測試
    print("\n開始測試...\n")
    viewer.view_all_videos()
    
    print("\n" + "="*60)
    print("測試完成！")
    print("="*60)
    print()
    print("如果測試成功，您可以：")
    print("1. 編輯 youtube_viewer_advanced.py 設定排程")
    print("2. 執行正式版本自動執行")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n測試已取消")
    except Exception as e:
        print(f"\n\n錯誤: {e}")
        print("\n請確認：")
        print("1. 已安裝所有套件 (pip install -r requirements.txt)")
        print("2. 已下載ChromeDriver並放到正確位置")
        print("3. 網路連線正常")
