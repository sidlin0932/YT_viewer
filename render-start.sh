#!/usr/bin/env bash
# Render.com 啟動腳本

set -o errexit

echo "======================================"
echo "啟動YouTube Viewer..."
echo "======================================"

# 啟動虛擬顯示
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99

# 等待Xvfb啟動
sleep 2

echo "虛擬顯示已啟動 (DISPLAY=$DISPLAY)"
echo "======================================"

# 運行主程式
python3 youtube_viewer_advanced.py
