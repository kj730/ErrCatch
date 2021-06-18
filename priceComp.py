#!/usr/bin/python
import sys
import datetime
TIME_COL = 0
PRICE_COL = 3
BUY_COL = 2
SELL_COL = 3

def priceMatch(filename):
    Dict ={}
    answer = []
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
        if len(splitter) < 4:
            continue
        if splitter[PRICE_COL].startswith("PRICES") == False:
            continue
        date_time_obj = datetime.datetime.strptime(splitter[TIME_COL][0:12], '%H:%M:%S.%f')
        strike = splitter[PRICE_COL][12:16]
        if strike in Dict.keys():
            Dict_split = Dict[strike].split('|')
            Dict_time_obj = datetime.datetime.strptime(Dict_split[TIME_COL][0:12], '%H:%M:%S.%f')
            if date_time_obj == Dict_time_obj:
                compAnswer = comp(line, Dict[strike])
                if compAnswer != "No errors":
                    answer.append(Dict[strike])
                    answer.append(line)                    
        Dict[strike] = line
    return answer

def comp(line1, line2):
    #815818496|IN|PRICES NG1NC2750 B:0.5170/3.26342593/Y A:0.5220/3.27332736/Y
    answer = "No errors"
    cutter = line1.split('|')
    splice = line2.split('|')
    price1_data = cutter[PRICE_COL]
    price2_data = splice[PRICE_COL]
    B_pos1 = price1_data.find('B:')
    B_pos2 = price2_data.find('B:')
    buy_line1_slash1 = price1_data.find('/')
    buy_line1_slash2 = price1_data.find('/', buy_line1_slash1 + 1)
    buy_line2_slash1 = price2_data.find('/')
    buy_line2_slash2 = price2_data.find('/', buy_line2_slash1 + 1)
    A_pos1 = price1_data.find('A:')
    A_pos2 = price2_data.find('A:')
    sell_line1_slash1 = price1_data.find('/', A_pos1)
    sell_line1_slash2 = price1_data.find('/', sell_line1_slash1 + 1)
    sell_line2_slash1 = price2_data.find('/', A_pos2)
    sell_line2_slash2 = price2_data.find('/', sell_line2_slash1 + 1)
    buyPrice1 = price1_data[B_pos1 + 2:buy_line1_slash1]
    buyPrice2 = price2_data[B_pos2 + 2:buy_line2_slash1]
    buyStockPrice1 = price1_data[buy_line1_slash1 + 1:buy_line1_slash2]
    buyStockPrice2 = price2_data[buy_line2_slash1 + 1:buy_line2_slash2]
    sellPrice1 = price1_data[A_pos1 + 2:sell_line1_slash1]
    sellPrice2 = price2_data[A_pos2 + 2:sell_line2_slash1]
    sellStockPrice1 = price1_data[sell_line1_slash1 + 1:sell_line1_slash2]
    sellStockPrice2 = price2_data[sell_line2_slash1 + 1:sell_line2_slash2]
    if(buyPrice1 == buyPrice2):
        if(buyStockPrice1 != buyStockPrice2):
            answer = line1, "\n", line2
    if(sellPrice1 == sellPrice2):
        if(sellStockPrice1 != sellStockPrice2):
           answer = line1, "\n", line2
    return answer

def main():
    if len(sys.argv) < 2:
        print("Usage: ", sys.argv[0], "Filename")
        exit(-1)
    filename = sys.argv[1]
    answer_list = priceMatch(filename)
    if len(answer_list) < 2:
        print("No errors")
    else:
        print(answer_list)
if __name__ == "__main__":
    main()