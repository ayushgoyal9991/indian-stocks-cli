# CLI Tool for Indian Stocks

A command line tool that gives you real time information about Indian Stocks.

## Demo

To get Nifty-50 data:
```bash
  python3 main.py nifty-50
```
![nifty-50]

To get the stock data of a single company:
```bash
  python3 main.py ticker <comapny_name_without_spaces>
```
Example:
```bash
  python3 main.py ticker Reliance
```
![single-stock-data]

To get the stock data of multiple companies:
```bash
  python3 main.py tickers <comapny_name1_without_spaces> <company_name2_without_spaces>
```
Example:
```bash
  python3 main.py tickers Biocon Cipla
```
![multiple-stock-data]

To get the stock data of a company including the annual analysis:
```bash
  python3 main.py ticker <comapny_name_without_spaces> -aa
```
Example:
```bash
  python3 main.py ticker Avanti-Feeds -aa
```
![annual-analysis]

To get the stock data of a company including the quarterly analysis:
```bash
  python3 main.py ticker <comapny_name_without_spaces> -qa
```
Example:
```bash
  python3 main.py ticker Titan -aa
```
![quarterly-analysis]

To get the stock data of a company including both the analysis:
```bash
  python3 main.py ticker <comapny_name_without_spaces> -aa -qa
```
Example:
```bash
  python3 main.py ticker Adani-Green -aa -qa
```
![both-analysis]

[nifty-50]: demo/nifty-50.gif
[single-stock-data]: demo/get-stock-data.gif
[multiple-stock-data]: demo/get-data-of-multiple-stocks.gif
[annual-analysis]: demo/annual-analysis.gif
[quarterly-analysis]: demo/quarterly-analysis.gif
[both-analysis]: demo/both-analysis.gif