from textblob import TextBlob

def analyze_sentiment(text):
    """分析情感倾向"""
    try:
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.1:
            return {'score': round(polarity, 3), 'label': '看涨', 'emoji': '📈'}
        elif polarity < -0.1:
            return {'score': round(polarity, 3), 'label': '看跌', 'emoji': '📉'}
        else:
            return {'score': round(polarity, 3), 'label': '中立', 'emoji': '➡️'}
    except:
        return {'score': 0, 'label': '未知', 'emoji': '❓'}

def analyze_articles(articles):
    """分析一批文章"""
    analyzed = []
    
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        text = f"{title}. {description if description else ''}"
        
        sentiment = analyze_sentiment(text)
        analyzed.append({
            'title': title,
            'source': article.get('source', {}).get('name', 'Unknown'),
            'url': article.get('url', ''),
            'sentiment': sentiment,
        })
    
    return analyzed

def calculate_market_sentiment(analyzed_articles):
    """计算市场情感评分"""
    if not analyzed_articles:
        return {'label': '无数据', 'score': 0, 'emoji': '❓'}
    
    total_score = sum(article['sentiment']['score'] for article in analyzed_articles)
    avg_score = total_score / len(analyzed_articles)
    
    if avg_score > 0.1:
        label, emoji = '看涨', '📈'
    elif avg_score < -0.1:
        label, emoji = '看跌', '📉'
    else:
        label, emoji = '中立', '➡️'
    
    return {
        'label': label,
        'emoji': emoji,
        'score': round(avg_score, 3),
        'total_articles': len(analyzed_articles),
    }
