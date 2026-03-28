"""美股分析系统配置文件"""
import os
from datetime import datetime
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
MONITOR_SYMBOLS = ['SPY', 'QQQ']
TIMEZONE = 'US/Eastern'
REPORTS_DIR = 'reports'
os.makedirs(REPORTS_DIR, exist_ok=True)
TIMESTAMP = datetime.now().strftime('%Y-%m-%d')