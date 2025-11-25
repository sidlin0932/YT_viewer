import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import schedule


class AdvancedYoutubeViewer:
    def __init__(self):
        self.video_urls = []
        self.proxies = []
        self.use_proxy = False
        self.watch_duration = 60  # 預設觀看60秒
        self.headless = False  # 是否使用無頭模式
        
    def add_video(self, url):
        """新增影片URL"""
        if "youtube.com" in url or "youtu.be" in url:
            self.video_urls.append(url)
            print(f"✓ 已新增影片: {url}")
        else:
            print(f"✗ 無效的YouTube連結: {url}")
    
    def add_proxy(self, proxy):
        """新增代理伺服器
        
        格式範例:
        - HTTP: "http://123.456.789.0:8080"
        - HTTPS: "https://123.456.789.0:8080"
        - 帶認證: "http://username:password@123.456.789.0:8080"
        - SOCKS5: "socks5://123.456.789.0:1080"
        """
        self.proxies.append(proxy)
        print(f"✓ 已新增代理: {proxy}")
        self.use_proxy = True
    
    def load_proxies_from_file(self, filename):
        """從檔案載入代理列表（每行一個）"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                proxies = [line.strip() for line in f if line.strip()]
                self.proxies.extend(proxies)
                self.use_proxy = len(self.proxies) > 0
                print(f"✓ 從 {filename} 載入了 {len(proxies)} 個代理")
        except FileNotFoundError:
            print(f"✗ 找不到檔案: {filename}")
        except Exception as e:
            print(f"✗ 載入代理時發生錯誤: {e}")
    
    def get_random_proxy(self):
        """隨機選擇一個代理"""
        if self.proxies:
            return random.choice(self.proxies)
        return None
    
    def create_driver(self, proxy=None):
        """建立瀏覽器驅動"""
        chrome_options = Options()
        
        # 基本設定
        if self.headless:
            chrome_options.add_argument('--headless')  # 無頭模式
        
        # 反偵測設定
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 隨機User Agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        ]
        chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        # 設定代理
        if proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
            print(f"  🌐 使用代理: {proxy}")
        
        # 其他設定
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--mute-audio')  # 靜音
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 設定偏好（關閉通知等）
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            
            # 移除自動化標誌
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            return driver
        except Exception as e:
            print(f"✗ 建立瀏覽器驅動時發生錯誤: {e}")
            print("  請確認已安裝 ChromeDriver")
            return None
    
    def random_sleep(self, min_sec=1, max_sec=3):
        """隨機等待（模擬人類行為）"""
        time.sleep(random.uniform(min_sec, max_sec))
    
    def simulate_human_behavior(self, driver):
        """模擬人類行為"""
        try:
            # 隨機滾動
            if random.random() > 0.5:
                scroll_amount = random.randint(100, 500)
                driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                self.random_sleep(0.5, 1.5)
            
            # 隨機移動滑鼠（透過移動到隨機元素）
            if random.random() > 0.7:
                try:
                    elements = driver.find_elements(By.TAG_NAME, "button")
                    if elements:
                        random_element = random.choice(elements[:5])
                        driver.execute_script("arguments[0].scrollIntoView(true);", random_element)
                        self.random_sleep(0.3, 0.8)
                except:
                    pass
        except Exception as e:
            pass  # 忽略錯誤
    
    def watch_video(self, url, proxy=None):
        """觀看影片"""
        driver = None
        try:
            print(f"\n{'='*60}")
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 開始觀看影片")
            print(f"URL: {url}")
            
            # 建立瀏覽器
            driver = self.create_driver(proxy)
            if not driver:
                return False
            
            # 開啟影片頁面
            print("  📺 正在載入影片頁面...")
            driver.get(url)
            self.random_sleep(3, 5)
            
            # 等待並點擊播放按鈕（如果需要）
            try:
                print("  ▶️  嘗試播放影片...")
                
                # 方法1: 點擊影片播放器
                video_player = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "video.html5-main-video"))
                )
                
                # 檢查是否已在播放
                is_paused = driver.execute_script("return document.querySelector('video.html5-main-video').paused")
                
                if is_paused:
                    # 點擊播放
                    driver.execute_script("document.querySelector('video.html5-main-video').play()")
                    self.random_sleep(1, 2)
                
                print("  ✓ 影片正在播放")
                
                # 隨機調整音量（但保持靜音）
                volume = random.randint(0, 30) / 100
                driver.execute_script(f"document.querySelector('video.html5-main-video').volume = {volume}")
                
            except TimeoutException:
                print("  ⚠ 無法找到播放器，可能需要手動處理")
            except Exception as e:
                print(f"  ⚠ 播放時發生問題: {e}")
            
            # 觀看影片（模擬真實行為）
            watch_duration = self.watch_duration
            print(f"  ⏱️  觀看時長: {watch_duration}秒")
            
            # 分段觀看，期間進行互動
            segments = 5
            time_per_segment = watch_duration / segments
            
            for i in range(segments):
                print(f"  ⏳ 進度: {int((i+1)/segments*100)}%", end='\r')
                time.sleep(time_per_segment)
                
                # 隨機進行人類行為（每段有50%機率）
                if random.random() > 0.5:
                    self.simulate_human_behavior(driver)
            
            print(f"\n  ✓ 完成觀看 ({watch_duration}秒)")
            
            # 獲取影片資訊
            try:
                title = driver.title
                print(f"  📝 影片標題: {title}")
            except:
                pass
            
            print(f"{'='*60}\n")
            return True
            
        except Exception as e:
            print(f"  ✗ 發生錯誤: {e}")
            print(f"{'='*60}\n")
            return False
            
        finally:
            # 關閉瀏覽器
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    def view_all_videos(self):
        """瀏覽所有影片"""
        if not self.video_urls:
            print("⚠ 沒有設定任何影片URL")
            return
        
        print(f"\n{'#'*60}")
        print(f"開始執行批次瀏覽任務")
        print(f"影片數量: {len(self.video_urls)}")
        print(f"使用代理: {'是 (' + str(len(self.proxies)) + '個)' if self.use_proxy else '否'}")
        print(f"{'#'*60}")
        
        success_count = 0
        
        for i, url in enumerate(self.video_urls, 1):
            print(f"\n>>> 影片 [{i}/{len(self.video_urls)}]")
            
            # 選擇代理
            proxy = self.get_random_proxy() if self.use_proxy else None
            
            # 觀看影片
            if self.watch_video(url, proxy):
                success_count += 1
            
            # 如果不是最後一個影片，隨機等待
            if i < len(self.video_urls):
                wait_time = random.randint(5, 15)
                print(f"  💤 等待 {wait_time} 秒後繼續...")
                time.sleep(wait_time)
        
        print(f"\n{'#'*60}")
        print(f"✓ 批次任務完成")
        print(f"成功: {success_count}/{len(self.video_urls)}")
        print(f"{'#'*60}\n")
    
    def schedule_daily(self, time_str):
        """設定每日固定時間執行"""
        schedule.every().day.at(time_str).do(self.view_all_videos)
        print(f"✓ 已設定每日 {time_str} 執行")
    
    def schedule_interval(self, hours=0, minutes=0):
        """設定間隔時間執行"""
        if hours > 0:
            schedule.every(hours).hours.do(self.view_all_videos)
            print(f"✓ 已設定每 {hours} 小時執行一次")
        elif minutes > 0:
            schedule.every(minutes).minutes.do(self.view_all_videos)
            print(f"✓ 已設定每 {minutes} 分鐘執行一次")
    
    def run_loop(self, times=1, interval_minutes=0):
        """執行指定次數的循環
        
        參數:
            times: 執行次數（預設1次）
            interval_minutes: 每次執行之間的等待時間（分鐘，預設0）
        """
        print(f"\n{'='*60}")
        print("進階 YouTube 影片瀏覽器 - 循環模式")
        print(f"{'='*60}")
        print(f"目前時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"影片數量: {len(self.video_urls)}")
        print(f"代理數量: {len(self.proxies)}")
        print(f"執行次數: {times}")
        print(f"間隔時間: {interval_minutes} 分鐘")
        print(f"觀看時長: {self.watch_duration}秒")
        print(f"\n{'='*60}\n")
        
        try:
            for i in range(times):
                print(f"\n{'🔄'*30}")
                print(f"第 {i+1}/{times} 次執行")
                print(f"{'🔄'*30}\n")
                
                # 執行觀看
                self.view_all_videos()
                
                # 如果不是最後一次，等待指定時間
                if i < times - 1 and interval_minutes > 0:
                    wait_seconds = interval_minutes * 60
                    print(f"\n⏳ 等待 {interval_minutes} 分鐘後繼續...")
                    print(f"下次執行時間: {datetime.now().strftime('%H:%M:%S')}")
                    
                    # 顯示倒數計時
                    for remaining in range(wait_seconds, 0, -60):
                        mins = remaining // 60
                        print(f"  剩餘 {mins} 分鐘...", end='\r')
                        time.sleep(60)
                    print()  # 換行
            
            print(f"\n{'='*60}")
            print(f"✅ 所有循環已完成！")
            print(f"總共執行: {times} 次")
            print(f"{'='*60}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n⚠️ 程式已被中斷（已完成 {i} 次）")
    
    def run(self):
        """開始執行排程"""
        print(f"\n{'='*60}")
        print("進階 YouTube 影片瀏覽器已啟動")
        print(f"{'='*60}")
        print(f"目前時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"影片數量: {len(self.video_urls)}")
        print(f"代理數量: {len(self.proxies)}")
        print(f"排程任務: {len(schedule.jobs)}")
        print(f"觀看時長: {self.watch_duration}秒")
        print("\n按 Ctrl+C 可停止程式\n")
        
        # 顯示所有排程
        for job in schedule.jobs:
            print(f"⏰ {job}")
        
        print(f"\n{'='*60}\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n程式已停止")


def main():
    """主程式"""
    viewer = AdvancedYoutubeViewer()
    
    # ==================== 設定區域 ====================
    
    # 1. 基本設定
    viewer.watch_duration = 60  # 每次觀看秒數（建議30-120秒）
    viewer.headless = False     # False=顯示瀏覽器, True=背景執行
    
    # 2. 新增影片URL
    viewer.add_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    # viewer.add_video("https://www.youtube.com/watch?v=YOUR_VIDEO_ID_2")
    
    # 3. 設定代理（三選一）
    
    # 方式A: 手動新增代理
    # viewer.add_proxy("http://123.456.789.0:8080")
    # viewer.add_proxy("socks5://123.456.789.0:1080")
    
    # 方式B: 從檔案載入代理列表
    # viewer.load_proxies_from_file("proxies.txt")
    

