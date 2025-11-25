#!/usr/bin/env bash
# Render.com 構建腳本

set -o errexit

echo "======================================"
echo "安裝系統依賴..."
echo "======================================"

# 更新包列表
apt-get update

# 安裝必要工具
apt-get install -y wget gnupg unzip

# 安裝Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# 安裝ChromeDriver
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+' | head -1)
CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d'.' -f1)
echo "Chrome版本: $CHROME_VERSION"

wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROME_MAJOR_VERSION}.0.6099.109/linux64/chromedriver-linux64.zip -P ~/
unzip -o ~/chromedriver-linux64.zip -d ~/
mv -f ~/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
rm -rf ~/chromedriver-linux64.zip ~/chromedriver-linux64

# 安裝字體
apt-get install -y fonts-liberation fonts-noto-cjk

# 安裝Xvfb（虛擬顯示）
apt-get install -y xvfb

echo "======================================"
echo "安裝Python依賴..."
echo "======================================"

pip install --upgrade pip
pip install -r requirements.txt

echo "======================================"
echo "構建完成！"
echo "======================================"
