import pandas
import mplfinance as mpf
import matplotlib.pyplot as plt
import datetime


# default
# dt_default = yf.Ticker('MSFT')
# dt_default = dt_default.history(period="1mo")  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
# print(dt_default)

# Класс "Графика"
class Graph:

    # Преобразование "timestamp" в "datetime" или "string"
    @staticmethod
    def ts_to_datetime(ts, d=None):
        result = datetime.datetime.fromtimestamp(ts / 1000.0)
        if d is None:
            return result.strftime('%Y-%m-%d %H:%M')
        else:
            return result

    # Преобразоввывает "lst_original" полученый от Polygon в более удобный (count - количество свеч, shift - сдвиг)
    def transformation_list(self, lst_original, count=None, shift=0):
        result = []
        temp = lst_original.copy()
        j = 0
        for i in temp:
            j += 1
            temp_dic = {}
            if count is None:
                x = self.ts_to_datetime(ts=i['t'], d=True)
                date = pandas.to_datetime(x)
                y = {"Date": date, "Open": i["o"], "High": i["h"], "Low": i["l"], "Close": i["c"], "Volume": i["v"]}
                temp_dic.update(y)
                result.append(temp_dic)
            else:
                if (count + shift) >= j > shift:
                    x = self.ts_to_datetime(ts=i['t'], d=True)
                    date = pandas.to_datetime(x)
                    y = {"Date": date, "Open": i["o"], "High": i["h"], "Low": i["l"], "Close": i["c"], "Volume": i["v"]}
                    temp_dic.update(y)
                    result.append(temp_dic)
        print("{} [transformation_list] Выбрано свеч: {} Сдвиг: {}".format(datetime.datetime.now(), len(result), shift))
        return result

    # Сохранить картинку графика на основе "data"
    def save_graph(self, data, count, shift=0):

        def save_to_png(dataframe, filename="graph.png"):
            plt.figure(figsize=(26, 18))
            z = mpf.plot(dataframe, type='candle', returnfig=True)
            z.savefig('static/{}'.format(filename))
            print("{} [save_graph_to_png] Изображение сохранено!".format(datetime.datetime.now()))

        lst = self.transformation_list(data, count=count, shift=shift)
        dt = pandas.DataFrame(lst)
        dt = dt.set_index(['Date'])
        save_to_png(dataframe=dt)
