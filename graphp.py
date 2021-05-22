import pandas
import mplfinance as mpf
import matplotlib.pyplot as plt  # плохо
import datetime


# default
# dt_default = yf.Ticker('MSFT')
# dt_default = dt_default.history(period="1mo")  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
# print(dt_default)


def ts_to_datetime(ts, d=None):
    result = datetime.datetime.fromtimestamp(ts / 1000.0)
    if d is None:
        return result.strftime('%Y-%m-%d %H:%M')
    else:
        return result


def json_to_dt(lst_original, count=None, reverse=None):
    result = []
    temp = lst_original.copy()
    j = 0
    for i in temp:
        j += 1
        temp_dic = {}
        if count is None:
            x = ts_to_datetime(ts=i['t'], d=True)
            date = pandas.to_datetime(x)
            temp_dic.update(
                {"Date": date, "Open": i["o"], "High": i["h"], "Low": i["l"], "Close": i["c"], "Volume": i["v"]})
            result.append(temp_dic)
        else:
            if count >= j:
                x = ts_to_datetime(ts=i['t'], d=True)
                date = pandas.to_datetime(x)
                temp_dic.update(
                    {"Date": date, "Open": i["o"], "High": i["h"], "Low": i["l"], "Close": i["c"], "Volume": i["v"]})
                result.append(temp_dic)
    print("Число свеч: {}".format(len(result)))
    return result


def save_graph_to_png(dataframe):
    plt.figure(figsize=(26, 18))
    z = mpf.plot(dataframe, type='candle', returnfig=True)
    z.savefig('static/graph.png')
    print("Сохранено!")


def save_graph(data):
    lst = json_to_dt(data[1], count=14)
    dt = pandas.DataFrame(lst)
    dt = dt.set_index(['Date'])
    save_graph_to_png(dataframe=dt)
