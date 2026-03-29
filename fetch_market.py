import yfinance as yf

def fetch_market_data(symbols):
    """获取股票行情数据"""
    market_data = {}
    
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='2d')
            
            if len(hist) > 0:
                latest = hist.iloc[-1]
                market_data[symbol] = {
                    'symbol': symbol,
                    'date': str(hist.index[-1].date()),
                    'open': round(float(latest['Open']), 2),
                    'close': round(float(latest['Close']), 2),
                    'high': round(float(latest['High']), 2),
                    'low': round(float(latest['Low']), 2),
                    'volume': int(latest['Volume']),
                    'change_pct': round((latest['Close'] - latest['Open']) / latest['Open'] * 100, 2),
                }
                print(f"✓ 获取 {symbol} 行情数据成功")
        except Exception as e:
            print(f"✗ 获取 {symbol} 失败: {str(e)}")
    
    return market_data
