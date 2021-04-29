import requests
from prettytable import PrettyTable
from termcolor import colored

from constants import NITFY_50_PAYLOAD

def get_stock_data_for_one_day(stock_name):
    duration = colored("1 Day", 'white')
    response = requests.get(f"https://api.tickertape.in/search?text={stock_name}&types=stock")
    json_data = response.json()

    try:
        total_stocks_found = json_data["data"]["total"]
    except:
        total_stocks_found = 0

    if total_stocks_found == 0:
        return None, None, None

    try:
        stock_data = json_data["data"]["stocks"][0]
        full_stock_name = stock_data["name"]
        sector = stock_data["sector"]
        stock_quote = stock_data["quote"]

        previous_close = round(stock_quote["close"], 2)
        price = round(stock_quote["price"], 2)
        sid = stock_quote["sid"]
        high = round(stock_quote["high"], 2)
        low = round(stock_quote["low"], 2)

        one_day_return = round((price - previous_close) / (previous_close) * 100, 2)

        if one_day_return < 0:
            one_day_return = colored(one_day_return, 'red', attrs=['blink'])
        else:
            one_day_return = colored(one_day_return, 'green')

        data = [
            duration,
            colored(price, 'magenta'),
            colored(previous_close, "yellow"),
            high,
            low,
            one_day_return
        ]

        return sid, full_stock_name, sector, data
    except:
        return None, None, None

def get_stock_data_by_duration(stock_sid, duration):
    response = requests.get(f"https://api.tickertape.in/stocks/charts/inter/{stock_sid}?duration={duration}")
    json_data = response.json()

    stock_data = json_data["data"][0]
    high = round(stock_data["h"], 2)
    low = round(stock_data["l"], 2)
    previous_close = round(stock_data["points"][0]["lp"], 2)
    price = round(stock_data["points"][-1]["lp"], 2)
    percentage_return = round(stock_data["r"], 2)

    if percentage_return < 0:
        percentage_return = colored(percentage_return, 'red', attrs=['blink'])
    else:
        percentage_return = colored(percentage_return, 'green')

    investment_duration = duration

    if duration == "1w":
        investment_duration = colored("1 Week", "white")
    elif duration == "1mo":
        investment_duration = colored("1 Month", "white")
    elif duration == "1y":
        investment_duration = colored("1 Year", "white")
    elif duration == "5y":
        investment_duration = colored("5 Years", "white")

    data = [
        investment_duration,
        colored(price, "magenta"),
        colored(previous_close, "yellow"),
        high,
        low,
        percentage_return
    ]

    return data


def get_nifty_50_data():
    headers = {'content-type': 'application/json;charset=UTF-8'}
    try:
        response = requests.post('https://api.tickertape.in/screener/query', headers = headers, data = NITFY_50_PAYLOAD)
        json_data = response.json()
        results = json_data["data"]["results"]
    except:
        print("Error in fetching Nifty data")
        return None

    if len(results) == 0:
        print("Error in fetching Nifty data")
        return None

    index_header = colored("Index", 'cyan')
    company_name_header = colored("Company Name", 'cyan')
    ticker_header = colored("Ticker", 'cyan')
    sector_header = colored("Sector", 'cyan')
    price_header = colored("Price (INR)", 'cyan')

    myTable = PrettyTable([index_header, company_name_header, ticker_header, sector_header, price_header])

    company_name_list = []
    ticker_list = []
    sector_list = []
    last_price_list = []

    for result in results:
        info = result["stock"]["info"]
        company_name = colored(info["name"], 'red')
        ticker = colored(info["ticker"], 'yellow')
        sector = info["sector"]
        last_price = colored(result["stock"]["advancedRatios"]["lastPrice"], 'blue')

        company_name_list.append(company_name)
        ticker_list.append(ticker)
        sector_list.append(sector)
        last_price_list.append(last_price)

    index = 1
    for company_name, ticker, sector, last_price in zip(company_name_list, ticker_list, sector_list, last_price_list):
        index_value = colored(index, 'white')
        myTable.add_row([index_value, company_name, ticker, sector, last_price])
        myTable.add_row(['', '', '', '', ''])
        index += 1

    return myTable
