import requests
from datetime import datetime, timedelta

def fetch_news(api_key, symbols, mode='pre'):
    """获取美股新闻"""
    all_articles = []
    
    for symbol in symbols:
        query = f"({symbol} stock) OR (USA market)"
        
        if mode == 'pre':
            from_date = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d')
        else:
            from_date = datetime.now().strftime('%Y-%m-%d')
        
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': query,
            'sortBy': 'publishedAt',
            'language': 'en',
            'from': from_date,
            'apiKey': api_key,
            'pageSize': 50,
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                all_articles.extend(articles)
                print(f"✓ 获取 {symbol} 的 {len(articles)} 条新闻")
            else:
                print(f"✗ NewsAPI 失败: {response.status_code}")
        except Exception as e:
            print(f"✗ 异常: {str(e)}")
    
    return all_articles
