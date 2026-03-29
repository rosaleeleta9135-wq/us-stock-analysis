import os
from datetime import datetime

# API 配置
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

# 监控股票列表
MONITOR_SYMBOLS = ['SPY', 'QQQ']

# 报告保存目录
REPORTS_DIR = 'reports'

# 创建目录
os.makedirs(REPORTS_DIR, exist_ok=True)
