import click
from termcolor import colored

from stocks import get_nifty_50_data


@click.group()
def main():
    pass

@main.command()
@click.argument("stock_name", nargs = 1)
def ticker(stock_name):
    """
    Usage: python main.py ticker <ticker_name_without_spaces>
    Example: python main.py ticker State-Bank-Of-India
    """
    print(stock_name)
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