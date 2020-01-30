import traceback
import time
import pandas as pd
from datetime import datetime
import urllib.request
import json

def dataScrap(ticker):
    urlIncomeStatement = urllib.request.urlopen('https://financialmodelingprep.com/api/v3/financials/income-statement/' + ticker)
    urlBalanceSheet = urllib.request.urlopen('https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/' + ticker)
    urlProfile = urllib.request.urlopen('https://financialmodelingprep.com/api/v3/company/profile/' + ticker)

    incomeStatementData = json.loads(urlIncomeStatement.read().decode())
    balanceSheetData = json.loads(urlBalanceSheet.read().decode())
    profileData = json.loads(urlProfile.read().decode())


    EBIT = float(incomeStatementData['financials'][0]['EBIT'])
    EV = float(profileData['profile']['mktCap']) - float(balanceSheetData['financials'][0]['Total debt']) - float(balanceSheetData['financials'][0]['Cash and cash equivalents'])
    print('Earnings Yeild')
    earningsYield = EBIT / EV
    print('Return on Cap')
    returnOnCap = EBIT / (float(balanceSheetData['financials'][0]['Total non-current assets']) + (float(balanceSheetData['financials'][0]['Total assets']) - float(balanceSheetData['financials'][0]['Total liabilities'])))

    return earningsYield, returnOnCap, datetime.strptime(incomeStatementData['financials'][0]['date'], "%Y-%m-%d"), datetime.strptime(balanceSheetData['financials'][0]['date'], "%Y-%m-%d")

def run(args):
    dataScrap('AAPL')
    abcSpace = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    abc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    cutOffDate = datetime.strptime(args['dataDate'][0], "%Y-%m-%d")
    header = True
    tickersChecked = 0
    tickersAdded = 0
    for i in abc:
        for j in abcSpace:
            for x in abcSpace:
                for y in abcSpace:
                    ticker = i + j + x + y
                    now = datetime.now()
                    tickersChecked += 1
                    print('\n***********************************\n*******\tTesting Ticker ' + ticker + '\t*******\n*******\t' + now.strftime("%d/%m/%Y %H:%M:%S") + '\t*******\n*******\tCheck #' + str(tickersChecked) + '\t\t*******\n***********************************\n')
                    try:
                        earningsYield, returnOnCap, incomeStatementDate, balanceSheetDate = dataScrap(ticker)
                        magPercent = (100 * (earningsYield + returnOnCap))
                        print('\tCollected: ' + ticker)
                        print('\tearningsYield: ' + str(earningsYield))
                        print('\treturnOnCap: ' + str(returnOnCap))
                        print('\tMagic Num: ' + str(magPercent))
                        print()
                        if magPercent > args['minMagicPercent'][0] and incomeStatementDate > cutOffDate and balanceSheetDate > cutOffDate:
                            tickersAdded += 1
                            print("\t****Added To File****")
                            print('\tTicker Added #' + str(tickersAdded))
                            tempRowDF = pd.DataFrame([{'Ticker': ticker,
                                                       'earningsYield': earningsYield,
                                                       'returnOnCap': returnOnCap,
                                                       'Magic Percent': magPercent,
                                                       'IncomeDate': incomeStatementDate.strftime("%m/%d/%Y"),
                                                       'BalanceDate': balanceSheetDate.strftime("%m/%d/%Y")}])
                            tempRowDF.to_csv(args['fileLocation'][0], mode='a', header=header)
                            header = False
                            print('***********************************')
                            time.sleep(0.001)
                    except Exception as e:
                        print('Error: ' + ticker)
                        print(str(e))
                        print(traceback.format_exc())

if __name__ == '__main__':
    rerun = 'Y'
    while rerun == 'y' or rerun == 'Y':
        args = pd.DataFrame([{'minMarketCap':(1000000*float(input('Min Market Cap (in Millions): '))),
                              'minMagicPercent': (float(input('Min Magic Percent (in Percent): '))/100),
                              'fileLocation':str(input('Location and name of CSV file to save data EX:(D:\\\\FinTech\\\\UnderValuedStockSearcher\\\\Data12.csv): ')),
                              'dataDate':str(input('Date where data is deemed inaccurate format EX:(YYYY-MM-DD): '))}])
        run(args)
        print('Search Market Run Complete')
        rerun = input('Would you like to rerun? (Y/N)')
    print('**** End Program ****')