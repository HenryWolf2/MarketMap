import requests
import matplotlib.pyplot as plt
import squarify
from bs4 import BeautifulSoup

stocks_to_check = 'https://companiesmarketcap.com/new-zealand/largest-companies-in-new-zealand-by-market-cap/'
data = requests.get(url=stocks_to_check)
bs = BeautifulSoup(data.text, 'lxml')
table = bs.find('table', class_='default-table table marketcap-table dataTable')
rows = table.find_all('td')
def get_data():
    """
    This function will get all the graphing data needed for the graph_data function.
    """
    tickers = []
    square_sizes = []
    caps = []
    ticker_i = 2
    cap_i = 3
    num_of_companies = int((len(rows) - 1) / 8)
    for num in range(num_of_companies):
        try:
            cap = rows[cap_i].text
            caps.append(cap)
            if cap[-1] == "M":
                square_sizes.append(float(cap[1:-2]) * 1000000)
            elif cap[-1] == "B":
                square_sizes.append(float(cap[1:-2]) * 1000000000)
            elif cap[-1] == "T":
                square_sizes.append(float(cap[1:-2]) * 1000000000000)
            ticker = rows[ticker_i].find("div", {"class": "company-code"}).text
            tickers.append(ticker)
            cap_i += 8
            ticker_i += 8
        except AttributeError:
            pass
    return tickers, square_sizes, caps


def graph_data(tickers, square_sizes, caps):
    """
    This function will graph the market map using matplotlib.
    Input variables:
    Tickers = the stock symbols
    Square_size = Numerical sizes to plot the market map
    Caps = String labels of the market caps for the market map
    """
    colours_of_squares = []
    for i in range(len(tickers)):
        colours_of_squares.append(plt.cm.jet(i / len(tickers)))
    plot_labels = []
    for i in range(len(tickers)):
        plot_labels.append(tickers[i] + '-' + caps[i])
    squarify.plot(color=colours_of_squares, sizes=square_sizes, label=plot_labels)
    plt.show()


tickers, square_sizes, caps = get_data()
print(tickers, square_sizes, caps)
graph_data(tickers, square_sizes, caps)
