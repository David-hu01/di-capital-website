import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
from jinja2 import Template
import math
import warnings

# 忽略所有警告
warnings.filterwarnings('ignore')

# 设置股票代码和今日/一年前的日期
tickers = ["TSLA"]  # 美股代码
today = datetime.today()
last_year = today - timedelta(days=365)

# 获取历史价格数据
def get_price(ticker, date):
    try:
        # 获取美股历史数据
        df = ak.stock_us_daily(symbol=ticker)
        # 将日期转换为datetime
        df['date'] = pd.to_datetime(df['date'])
        # 找到最接近指定日期的数据
        target_date = pd.to_datetime(date)
        closest_date = df['date'].iloc[(df['date'] - target_date).abs().argsort()[0]]
        price = df[df['date'] == closest_date]['close'].iloc[0]
        return float(price) if not math.isnan(price) else None
    except Exception as e:
        print(f"获取 {ticker} 价格数据时出错: {e}")
        return None

# 获取初始和当前价格
initial_value = 0
current_value = 0
for ticker in tickers:
    price_then = get_price(ticker, last_year)
    price_now = get_price(ticker, today)
    if price_then is not None and price_now is not None and not (math.isnan(price_then) or math.isnan(price_now)):
        initial_value += 1  # 假设每个资产当初都投入1单位
        current_value += price_now / price_then  # 单独收益乘上原始单位

# 计算滚动年收益率
if initial_value > 0:
    return_rate = (current_value / initial_value - 1) * 100
    # 计算当前净值（初始净值12.11）
    nav = 12.11 * (1 + return_rate/100)
else:
    return_rate = 0
    nav = 12.11

# 加载 HTML 模板并渲染
with open("templates/index_template.html", "r", encoding="utf-8") as f:
    template = Template(f.read())

output_html = template.render(
    return_rate=f"{return_rate:.2f}%",
    date=today.strftime("%Y-%m-%d"),
    tickers=", ".join(tickers),
    nav=f"{nav:.2f}"  # 净值保留4位小数
)

# 修改输出路径
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write(output_html)

print("✅ 页面生成完成：docs/index.html")