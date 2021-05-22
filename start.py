from time import sleep
from polygon import RESTClient
from flask import Flask, render_template, request
import datetime
from graphp import save_graph
from threading import Thread
import multiprocessing


def ts_to_datetime(ts, d=None):
    result = datetime.datetime.fromtimestamp(ts / 1000.0)
    if d is None:
        return result.strftime('%Y-%m-%d %H:%M')
    else:
        return result


def get_bars(ticker, period, date_from, date_to):
    key = "P4KJxw1ZvsZ9JDxWPGS2VXvBnxCpDi8H"
    with RESTClient(key) as client:
        title = f'Данные для данные для "{ticker}" с {date_from} по {date_to} (Период: {period} минут)'
        resp = client.stocks_equities_aggregates(ticker, period, "minute", date_from, date_to, unadjusted=False)
        # sleep(1)
        print("Получено свеч:", len(resp.results))
        return [resp, resp.results, title]


def print_table(resp):
    sleep(1)
    result_text = []
    for result in resp.results:
        dt = ts_to_datetime(result["t"])
        temp = [f"{dt}", f"O: {result['o']}", f"H: {result['h']}", f"L: {result['l']}", f"C: {result['c']}"]
        result_text.append(temp)
        # print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
    return result_text


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':  # Запрос на чтение (к примеру при обновлении страницы Flask)
        ticker = "MSFT"
        period = 15

        data = get_bars(ticker=ticker, period=period, date_from="2021-04-18", date_to="2021-05-18")

        # Вариант 1 (не работает)
        # save_graph(data=data)
        # Вариант 2 (не работает)
        # Thread(target=save_graph, args=(data, )).start()
        # Вариант 3 (работает)
        multiprocessing.Process(None, save_graph, args=(data,)).start()

        json = print_table(data[0])
        return render_template('index.html', TITLE=data[2], JSON=json, YEAR=None)
    if request.method == 'POST':
        ticker = request.form['ticket']
        period = request.form['period']

        data = get_bars(ticker=ticker, period=period, date_from="2021-04-18", date_to="2021-05-18")

        # Вариант 1 (не работает)
        # save_graph(data=data)
        # Вариант 2 (не работает)
        # Thread(target=save_graph, args=(data, )).start()
        # Вариант 3 (работает)
        multiprocessing.Process(None, save_graph, args=(data,)).start()

        json = print_table(data[0])
        return render_template('index.html', TITLE=data[2], JSON=json, YEAR=None)


if __name__ == '__main__':
    app.run()
