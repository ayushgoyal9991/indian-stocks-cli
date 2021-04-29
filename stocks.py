import requests
from prettytable import PrettyTable
from termcolor import colored

from constants import NITFY_50_PAYLOAD

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
