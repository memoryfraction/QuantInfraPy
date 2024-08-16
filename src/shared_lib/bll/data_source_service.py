import yfinance as yf


def get_data():
    # 创建股票代码对象
    apple = yf.Ticker("AAPL")

    # 获取历史数据
    data = apple.history(period="1d", interval="1m")

    return data
