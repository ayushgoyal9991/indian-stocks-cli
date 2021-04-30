import click
from termcolor import colored

from stocks import get_nifty_50_data, get_stock_data_table, get_stock_data_table_for_a_list_of_stocks


@click.group()
def main():
    pass

#  get stock data of a single company
@main.command()
@click.argument("stock_name", nargs = 1)
def ticker(stock_name):
    """
    Usage: python main.py ticker <ticker_name_without_spaces>
    Example: python main.py ticker State-Bank-Of-India
    """
    print(f"Getting stock data of {stock_name}!")
    stock_data_table = get_stock_data_table(stock_name)
    if stock_data_table is not None:
        print(stock_data_table)
    return

#  get stock data of multiple companies
@main.command()
@click.argument("stock_names", nargs = -1)
def tickers(stock_names):
    """
        Usage: python main.py tickers <ticker_name_1_without_spaces> <ticker_name_2_without_spaces> ......
        Example: python main.py tickers Reliance Wipro TCS
    """
    stock_names = list(stock_names)
    print(f"Getting stock data of {stock_names}!")
    get_stock_data_table_for_a_list_of_stocks(stock_names)
    return

#  get nifty-50 data
@main.command()
@click.option("--nifty50")
def nifty_50(nifty50):
    """
        Usage: python main.py nifty-50
    """
    print()
    print(f"{colored('Nifty 50', 'red')}".center(110))
    nifty_50_table = get_nifty_50_data()
    if nifty_50_table is not None:
        print(nifty_50_table)
    return

if __name__ == "__main__":
    main()