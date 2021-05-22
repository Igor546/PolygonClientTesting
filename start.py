from time import sleep
from polygon import RESTClient
from flask import Flask, render_template, request
import datetime
from graphp import Graph
from threading import Thread
import multiprocessing


# Вариант 1 (не работает)
# save_graph(data=data, count=14)
# Вариант 2 (не работает)
# Thread(target=save_graph, args=(data, 14)).start()
# Вариант 3 (работает)
# multiprocessing.Process(None, save_graph, args=(data, 14)).start()

def ts_to_datetime(ts, d=None):
    result = datetime.datetime.fromtimestamp(ts / 1000.0)
    if d is None:
        return result.strftime('%Y-%m-%d %H:%M')
    else:
        return result


def get_bars(t, p, date_from, date_to):
    key = "P4KJxw1ZvsZ9JDxWPGS2VXvBnxCpDi8H"
    with RESTClient(key) as client:
        title = [f'Данные для данные для', f'{t}', f'с {date_from} по {date_to}', f'(Период: {period} min)']
        resp = client.stocks_equities_aggregates(t, p, "minute", date_from, date_to, unadjusted=False)
        print("{} [get_bars] Принято свеч: {}".format(datetime.datetime.now(), len(resp.results)))
        return {"Main": resp, "Candles": resp.results, "Title": title}


def get_table(resp):
    sleep(1)
    result_text = []
    for result in resp.results:
        dt = ts_to_datetime(result["t"])
        temp = [f"{dt}", f"O: {result['o']}", f"H: {result['h']}", f"L: {result['l']}", f"C: {result['c']}"]
        result_text.append(temp)
        # print(f"{dt}\n\tO: {result['o']}\n\tH: {result['h']}\n\tL: {result['l']}\n\tC: {result['c']} ")
    return result_text


# Умная пауза
def wait(thread, delay=5):
    count = 0
    for i in range(delay * 1000):
        count += 1
        sleep(0.001)
        if not thread.is_alive():
            print("{} [wait] Пауза закончилась. (Iterations={})".format(datetime.datetime.now(), count))
            return True
    print("{} [wait] Пауза закончилась. (Iterations=MAX)".format(datetime.datetime.now()))
    return False


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    global position
    global ticker
    global period
    global data
    global table
    global count

    if request.method == 'GET':  # Запрос на чтение (к примеру при обновлении страницы Flask)
        th = multiprocessing.Process(None, graph.save_graph, args=(data["Candles"], position[0], position[1]))
        th.start()
        wait(th)
        progress = [position[1] + count + 1, len(data["Candles"])]
        json = {"ticker": ticker, "period": period, "table": table, "progress": progress}
        return render_template('index.html', TITLE=data["Title"], JSON=json)
    if request.method == 'POST':
        if request.form['submit'] == "Отправить":

            count = 6
            position = [count + 1, 0]  # count, shift

            ticker = request.form['ticket']
            period = request.form['period']
            data = get_bars(t=ticker, p=period, date_from="2021-04-18", date_to="2021-05-18")
            th = multiprocessing.Process(None, graph.save_graph, args=(data["Candles"], position[0], position[1]))
            th.start()
            wait(th)
            table = get_table(data["Main"])
            progress = [position[1] + count + 1, len(data["Candles"])]
            json = {"ticker": ticker, "period": period, "table": table, "progress": progress}
            return render_template('index.html', TITLE=data["Title"], JSON=json)
        elif request.form['submit'] == "Вперед":
            print(len(data["Candles"]))
            if position[1] + count + 1 < len(data["Candles"]):
                position[1] += count

            progress = [position[1] + count + 1, len(data["Candles"])]
            th = multiprocessing.Process(None, graph.save_graph, args=(data["Candles"], position[0], position[1]))
            th.start()
            wait(th)
            json = {"ticker": ticker, "period": period, "table": table, "progress": progress}
            return render_template('index.html', TITLE=data["Title"], JSON=json)
        elif request.form['submit'] == "Назад":
            if position[1] - count > 0:
                position[1] -= count
            progress = [position[1] + count + 1, len(data["Candles"])]
            th = multiprocessing.Process(None, graph.save_graph, args=(data["Candles"], position[0], position[1]))
            th.start()
            wait(th)
            json = {"ticker": ticker, "period": period, "table": table, "progress": progress}
            return render_template('index.html', TITLE=data["Title"], JSON=json)


if __name__ == '__main__':

    graph = Graph()

    ticker = "MSFT"
    period = 15
    data = get_bars(t=ticker, p=period, date_from="2021-04-18", date_to="2021-05-18")
    table = get_table(data["Main"])

    count = 6
    position = [count + 1, 0]  # count, shift

    app.run()
