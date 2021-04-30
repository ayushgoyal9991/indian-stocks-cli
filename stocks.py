import click
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

def get_stock_data_table_for_a_list_of_stocks(stock_names):
    for stock_name in stock_names:
        stock_data_table = get_stock_data_table(stock_name)
        if stock_data_table is not None:
            print(stock_data_table)

def get_stock_data_table(stock_name):
    row_list = []
    duration_header = colored("Duration", 'cyan')
    price_header = colored("Price (INR)", 'cyan')
    prev_close_header = colored("Previous Close (INR)", 'cyan')
    high_header = colored("High (INR)", 'cyan')
    low_header = colored("Low (INR)", 'cyan')
    percentage_return_header = colored("% Return", 'cyan')
    myTable = PrettyTable(
        [duration_header, price_header, prev_close_header, high_header, low_header, percentage_return_header])

    stock_id, full_stock_name, sector, row_data = get_stock_data_for_one_day(stock_name = stock_name)
    if stock_id is None:
        stock_ticker_name = colored(stock_name, 'red')
        print(f"No data found for stock ticker name '{stock_ticker_name}'")
        return

    row_list.append(row_data)

    row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = "1w")
    row_list.append(row_data)

    row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = "1mo")
    row_list.append(row_data)

    row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = "1y")
    row_list.append(row_data)

    row_data = get_stock_data_by_duration(stock_sid = stock_id, duration = "5y")
    row_list.append(row_data)

    full_stock_name = click.style(full_stock_name, fg = 'red', bold = True)
    stock_sector = click.style(f"Sector - {sector}", fg = 'yellow', bold = True)
    print()
    print(f"{full_stock_name}".center(90))
    print(f"{stock_sector}".center(90))
    for row in row_list:
        myTable.add_row(row)
        myTable.add_row(['', '', '', '', '', ''])

    return myTable

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

def get_annual_growth_stock_data(stock_name):
    stock_id, full_stock_name, sector, row_data = get_stock_data_for_one_day(stock_name = stock_name)
    response = requests.get(f"https://api.tickertape.in/stocks/financials/income/{stock_id}/annual/growth?count=10")
    json_data = response.json()
    last_four_year_annual_data = json_data["data"][-4:]
    eps_growth_data = [colored("EPS Growth (%)", "yellow")]
    net_income_growth_data = [colored("Net Income Growth (%)", "yellow")]
    financial_year_name = []

    for year_data in last_four_year_annual_data:
        eps = round(year_data["incEps"], 2)
        net_income = round(year_data["incNinc"], 2)
        financial_year_period = year_data["displayPeriod"].replace(" ", "").replace("FY'", "20")

        if eps < 0:
            eps = colored(eps, 'red')
        else:
            eps = colored(eps, 'green')

        if net_income < 0:
            net_income = colored(net_income, 'red')
        else:
            net_income = colored(net_income, 'green')

        eps_growth_data.append(eps)
        net_income_growth_data.append(net_income)
        financial_year_name.append(financial_year_period)

    debt_to_equity_ratio_data, current_ratio_data, long_term_debt_data, roe_data, roce_data = get_financial_ratios(stock_id)
    row_list = []
    financial_year_header = colored("Financial Year", 'cyan')
    fy_1 = colored(financial_year_name[0], 'cyan')
    fy_2 = colored(financial_year_name[1], 'cyan')
    fy_3 = colored(financial_year_name[2], 'cyan')
    fy_4 = colored(financial_year_name[3], 'cyan')
    myTable = PrettyTable(
        [financial_year_header, fy_1, fy_2, fy_3, fy_4])

    row_list.append(eps_growth_data)
    row_list.append(net_income_growth_data)
    row_list.append(debt_to_equity_ratio_data)
    row_list.append(current_ratio_data)
    row_list.append(long_term_debt_data)
    row_list.append(roe_data)
    row_list.append(roce_data)

    for row in row_list:
        myTable.add_row(row)
        myTable.add_row(['', '', '', '', ''])
    return myTable

def get_quarterly_growth_stock_data(stock_name):
    stock_id, full_stock_name, sector, row_data = get_stock_data_for_one_day(stock_name = stock_name)
    response = requests.get(f"https://api.tickertape.in/stocks/financials/income/{stock_id}/interim/growth?count=10")
    json_data = response.json()
    last_four_quarters_data = json_data["data"][-4:]
    eps_growth_data = [colored("EPS Growth (%)", "yellow")]
    net_income_growth_data = [colored("Net Income Growth (%)", "yellow")]
    quarter_name = []

    for quarter_data in last_four_quarters_data:
        eps = round(quarter_data["qIncEps"], 2)
        net_income = round(quarter_data["qIncNinc"], 2)
        quarter_period = quarter_data["displayPeriod"].replace(" ", "")

        if eps < 0:
            eps = colored(eps, 'red')
        else:
            eps = colored(eps, 'green')

        if net_income < 0:
            net_income = colored(net_income, 'red')
        else:
            net_income = colored(net_income, 'green')

        eps_growth_data.append(eps)
        net_income_growth_data.append(net_income)
        quarter_name.append(quarter_period)

    row_list = []
    quarter_header = colored("Quarter", 'cyan')
    q_name_1 = colored(quarter_name[0], 'cyan')
    q_name_2 = colored(quarter_name[1], 'cyan')
    q_name_3 = colored(quarter_name[2], 'cyan')
    q_name_4 = colored(quarter_name[3], 'cyan')
    myTable = PrettyTable(
        [quarter_header, q_name_1, q_name_2, q_name_3, q_name_4])

    row_list.append(eps_growth_data)
    row_list.append(net_income_growth_data)

    for row in row_list:
        myTable.add_row(row)
        myTable.add_row(['', '', '', '', ''])

    return myTable

def get_financial_ratios(stock_id):
    balance_sheet_response = requests.get(f"https://api.tickertape.in/stocks/financials/balancesheet/{stock_id}/annual/normal?count=10")
    json_data = balance_sheet_response.json()
    last_four_year_balance_sheet_data = json_data["data"][-4:]

    debt_to_equity_ratio_data = [colored("Debt/Equity Ratio", "yellow")]
    current_ratio_data = [colored("Current Ratio", "yellow")]
    roe_data = [colored("RoE (%)", "yellow")]
    roce_data = [colored("RoCE (%)", "yellow")]
    long_term_debt_data = [colored("Long Term Debt (in Cr)", "yellow")]

    annual_normal_response = requests.get(f"https://api.tickertape.in/stocks/financials/income/{stock_id}/annual/normal?count=10")
    annual_normal_json_data = annual_normal_response.json()
    last_four_year_annual_normal_data = annual_normal_json_data["data"][-4:]

    for yearly_bs_data, yearly_income_data in zip(last_four_year_balance_sheet_data, last_four_year_annual_normal_data):
        long_term_debt = round(yearly_bs_data["balTltd"], 2)
        roe = round((yearly_income_data["incNinc"]/yearly_bs_data["balTeq"])*100, 2)
        roce = round(yearly_income_data["incPbi"]/(yearly_bs_data["balTota"]-yearly_bs_data["balTcl"])*100, 2)
        debt_to_equity_ratio = round((yearly_bs_data["balAccp"] + yearly_bs_data["balTltd"])/yearly_bs_data["balTeq"], 2)

        if debt_to_equity_ratio > 2 or debt_to_equity_ratio < 0:
            debt_to_equity_ratio = colored(debt_to_equity_ratio, "red")
        else:
            debt_to_equity_ratio = colored(debt_to_equity_ratio, "green")


        current_ratio = round(yearly_bs_data["balTca"]/yearly_bs_data["balTcl"], 2) #  total_current_assets/total_current_liabilities
        debt_to_equity_ratio_data.append(debt_to_equity_ratio)
        current_ratio_data.append(current_ratio)
        roe_data.append(roe)
        roce_data.append(roce)
        long_term_debt_data.append(long_term_debt)

    return debt_to_equity_ratio_data, current_ratio_data, long_term_debt_data, roe_data, roce_data
