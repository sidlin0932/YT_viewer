# Advanced YouTube Viewer

這是一個進階的 YouTube 影片瀏覽工具，支援自動化瀏覽、代理伺服器切換、排程執行以及模擬人類行為。

## 功能特點

- **自動化瀏覽**: 自動開啟瀏覽器觀看指定影片。
- **代理支援**: 支援 HTTP, HTTPS, SOCKS5 代理，並可隨機切換。
- **行為模擬**: 模擬人類滑鼠移動、滾動頁面、隨機暫停等行為，降低被偵測風險。
- **排程執行**: 支援每日定時執行或間隔執行。
- **無頭模式**: 支援背景執行，不干擾日常作業。

## 安裝說明

1.  **環境需求**:
    - Python 3.8 或以上版本
    - Google Chrome 瀏覽器

2.  **安裝依賴套件**:
    ```bash
    pip install -r requirements.txt
    ```
    *注意: 程式會自動使用 Selenium Manager 下載對應的 ChromeDriver，無需手動下載。*

## 使用方法

### 1. 設定代理 (Proxies)

在專案目錄下建立 `proxies.txt` 檔案，每行填入一個代理伺服器位址。

**格式範例**:
```text
http://123.456.789.0:8080
socks5://123.456.789.0:1080
http://username:password@123.456.789.0:8080
```

> **注意**: `proxies.txt` 包含敏感資訊，請勿上傳至公開版本控制系統 (已加入 .gitignore)。

### 2. 執行程式

直接執行 Python 腳本：

```bash
python youtube_viewer_advanced.py
```

### 3. 程式設定

您可以直接修改 `youtube_viewer_advanced.py` 中的 `main()` 函式來調整設定：

```python
def main():
    viewer = AdvancedYoutubeViewer()
    
    # 設定觀看時間 (秒)
    viewer.watch_duration = 60
    
    # 設定是否背景執行
    viewer.headless = False
    
    # 新增影片
    viewer.add_video("https://www.youtube.com/watch?v=YOUR_VIDEO_ID")
    
    # 載入代理
    viewer.load_proxies_from_file("proxies.txt")
    
    # 執行模式 (三選一)
    # 1. 單次執行
    viewer.view_all_videos()
    
    # 2. 循環執行 (例如執行 10 次，每次間隔 30 分鐘)
    # viewer.run_loop(times=10, interval_minutes=30)
    
    # 3. 排程執行
    # viewer.schedule_daily("09:00")
    # viewer.run()
```

## 檔案說明

- `youtube_viewer_advanced.py`: 主要程式邏輯。
- `get_proxies.py`: (選用) 用於從網路抓取免費代理的工具。
- `proxies.txt`: 代理伺服器列表 (需自行建立)。
- `requirements.txt`: Python 套件依賴列表。

## 免責聲明

本工具僅供教育與研究用途，請勿用於惡意刷取點閱率或違反 YouTube 服務條款之行為。使用者需自行承擔使用本工具之風險。
