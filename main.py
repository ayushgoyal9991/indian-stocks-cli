import click
from termcolor import colored


@click.group()
def main():
    pass

@main.command()
@click.option("--nifty50")
def nifty_50(nifty50):
    """
        Usage: python main.py nifty-50
    """
    print()
    print(f"{colored('Nifty 50', 'red')}".center(110))
    return

if __name__ == "__main__":
    main()