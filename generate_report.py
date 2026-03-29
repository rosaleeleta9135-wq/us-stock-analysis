import argparse
import os
from datetime import datetime
from fetch_news import fetch_news
from fetch_market import fetch_market_data
from analyze_news import analyze_articles, calculate_market_sentiment
import config

def generate_pre_market_report(articles, market_data):
    """生成盘前分析报告"""
    analyzed = analyze_articles(articles)
    sentiment = calculate_market_sentiment(analyzed)
    
    bullish = [a for a in analyzed if a['sentiment']['label'] == '看涨']
    bearish = [a for a in analyzed if a['sentiment']['label'] == '看跌']
    
    report = f"""# 📈 美股盘前分析报告
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🔮 市场情绪评估

| 指标 | 数值 |
|-----|------|
| 市场情绪 | {sentiment['emoji']} **{sentiment['label']}** |
| 情感评分 | {sentiment['score']} |
| 看涨新闻 | {len(bullish)} 条 |
| 看跌新闻 | {len(bearish)} 条 |

## 📰 热点新闻 (Top 5)
"""
    
    for i, article in enumerate(analyzed[:5], 1):
        report += f"\n{i}. **{article['title']}**\n"
        report += f"   来源: {article['source']} | {article['sentiment']['emoji']} {article['sentiment']['label']}\n"
    
    report += f"""
## 📊 关键股指行情

| 代码 | 开盘 | 收盘 | 涨跌幅 |
|-----|------|------|--------|
"""
    
    for symbol, data in market_data.items():
        report += f"| {symbol} | ${data['open']} | ${data['close']} | {data['change_pct']:+.2f}% |\n"
    
    return report

def generate_post_market_report(articles, market_data):
    """生成盘后展望报告"""
    analyzed = analyze_articles(articles)
    sentiment = calculate_market_sentiment(analyzed)
    
    report = f"""# 📉 美股盘后展望报告
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📊 今日行情总结

| 代码 | 开盘 | 收盘 | 涨跌幅 |
|-----|------|------|--------|
"""
    
    for symbol, data in market_data.items():
        change_emoji = "📈" if data['change_pct'] > 0 else "📉"
        report += f"| {change_emoji} {symbol} | ${data['open']} | ${data['close']} | {data['change_pct']:+.2f}% |\n"
    
    report += f"""
## 🎯 市场情绪评估

| 指标 | 数值 |
|-----|------|
| 市场情绪 | {sentiment['emoji']} **{sentiment['label']}** |
| 情感评分 | {sentiment['score']} |

## 📰 今日热点新闻 (Top 5)
"""
    
    for i, article in enumerate(analyzed[:5], 1):
        report += f"\n{i}. **{article['title']}**\n"
        report += f"   来源: {article['source']} | {article['sentiment']['emoji']} {article['sentiment']['label']}\n"
    
    report += "\n---\n\n✅ 报告生成完成！\n"
    return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='pre', choices=['pre', 'post'])
    args = parser.parse_args()
    
    if not config.NEWS_API_KEY:
        print("❌ 错误: NEWS_API_KEY 未配置")
        return
    
    print("📥 正在获取数据...")
    articles = fetch_news(config.NEWS_API_KEY, config.MONITOR_SYMBOLS, mode=args.mode)
    market_data = fetch_market_data(config.MONITOR_SYMBOLS)
    
    if not articles or not market_data:
        print("❌ 无法获取数据")
        return
    
    print("✍️ 正在生成报告...")
    if args.mode == 'pre':
        report = generate_pre_market_report(articles, market_data)
    else:
        report = generate_post_market_report(articles, market_data)
    
    timestamp = datetime.now().strftime('%Y-%m-%d')
    period = 'AM' if args.mode == 'pre' else 'PM'
    filename = f"{config.REPORTS_DIR}/report_{timestamp}_{period}.md"
    
    os.makedirs(config.REPORTS_DIR, exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告已生成: {filename}")

if __name__ == '__main__':
    main()
