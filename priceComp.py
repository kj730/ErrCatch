#!/usr/bin/python
import sys
import datetime
TIME_COL = 0
PRICE_COL = 3
BUY_COL = 2
SELL_COL = 3

def priceMatch(filename):
    Dict ={}
    answer = "No errors"
    try:
        general = open(filename, "r")
    except OSError as err:
        print("Unable to open General File. OS error: {0}".format(err))
        return -1
    except:
        print("Unable to open General File")
        return -1
    for line in general:
        splitter = line.split('|')
        date_time_obj1 = datetime.datetime.strptime(splitter[TIME_COL], '%H:%M:%S.%f')
        if splitter[PRICE_COL].startswith("PRICES") == False:
            continue
        for key in Dict:
            if splitter[PRICE_COL][12:16] == key:
                seperate = Dict[key].split('|')
                date_time_obj2 = datetime.datetime.strptime(seperate[TIME_COL], '%H:%M:%S.%f')
                if date_time_obj1 == date_time_obj2:
                    answer = comp(line, Dict[key])
                else:
                    Dict[key] = line
                    break
        if Dict[splitter[PRICE_COL][12:16]] == line:
            continue
        else:
            Dict[splitter[PRICE_COL][12:16]] = line
    return answer

def comp(line1, line2):
    answer = "No errors"
    cutter = line1.split('|')
    splice = line2.split('|')
    duplicate = cutter[PRICE_COL].split(' ')
    multiply = splice[PRICE_COL].split(' ')
    buyPrice1 = duplicate[BUY_COL][2:8]
    buyPrice2 = multiply[BUY_COL][2:8]
    sellPrice1 = duplicate[SELL_COL][2:8]
    sellPrice2 = multiply[SELL_COL][2:8]
    buyStockPrice1 = duplicate[BUY_COL][9:19]
    buyStockPrice2 = multiply[BUY_COL][9:19]
    sellStockPrice1 = duplicate[SELL_COL][9:19]
    sellStockPrice2 = multiply[SELL_COL][9:19]
    if(buyPrice1 == buyPrice2):
        if(buyStockPrice1 == buyStockPrice2):
            answer = line1, "\n", line2
    elif(sellPrice1 == sellPrice2):
        if(sellStockPrice1 == sellStockPrice2):
            answer = line1, "\n", line2
    return answer

def main():
    if len(sys.argv) < 2:
        print("Usage: ", sys.argv[0], "Filename")
        exit(-1)
    filename = sys.argv[1]
    answer = priceMatch(filename)
    print(answer)
if __name__ == "__main__":
    main()