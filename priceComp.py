#!/usr/bin/python
import sys
import datetime
TIME_COL = 0
PRICE_COL = 3
BUY_COL = 2
SELL_COL = 3
#checks to see if two lines in a file have the same time and strike
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
        #skips any line that is not in the right parameters
        if len(splitter) < 4:
            continue
        if splitter[PRICE_COL].startswith("PRICES") == False:
            continue
        #make a time object to compare the times
        date_time_obj = datetime.datetime.strptime(splitter[TIME_COL][0:12], '%H:%M:%S.%f')
        strike = splitter[PRICE_COL][12:16]
        #for the correct lines, make a dictionary and add the line to it, using strike as the key
        if len(Dict) == 0:
            Dict[strike] = line
        #compare the current strike and time object with those in the file
        elif strike in Dict.keys():
            Dict_split = Dict[strike].split('|')
            Dict_time_obj = datetime.datetime.strptime(Dict_split[TIME_COL][0:12], '%H:%M:%S.%f')
            if date_time_obj == Dict_time_obj:
                #call the comp method to compare the buy/sell prices and future prices
                answer = comp(line, Dict[strike])
                if answer != "No errors":
                    return answer
        Dict[strike] = line
    return answer
#checks to see if there are two lines with the same but/sell prices, but different future prices
def comp(line1, line2):
    #815818496|IN|PRICES NG1NC2750 B:0.5170/3.26342593/Y A:0.5220/3.27332736/Y
    answer = "No errors"
    #sererates the two file lines to get each of their values
    cutter = line1.split('|')
    splice = line2.split('|')
    B_pos1 = cutter[PRICE_COL].find('B:')
    B_pos2 = splice[PRICE_COL].find('B:')
    buy_line1_slash1 = cutter[PRICE_COL].find('/')
    buy_line1_slash2 = cutter[PRICE_COL].find('/', buy_line1_slash1 + 1)
    buy_line2_slash1 = splice[PRICE_COL].find('/')
    buy_line2_slash2 = splice[PRICE_COL].find('/', buy_line2_slash1 + 1)
    A_pos1 = cutter[PRICE_COL].find('A:')
    A_pos2 = splice[PRICE_COL].find('A:')
    sell_line1_slash1 = cutter[PRICE_COL].find('/', A_pos1)
    sell_line1_slash2 = cutter[PRICE_COL].find('/', sell_line1_slash1 + 1)
    sell_line2_slash1 = splice[PRICE_COL].find('/', A_pos2)
    sell_line2_slash2 = splice[PRICE_COL].find('/', sell_line2_slash1 + 1)
    buyPrice1 = cutter[PRICE_COL][B_pos1 + 2:buy_line1_slash1]
    buyPrice2 = splice[PRICE_COL][B_pos2 + 2:buy_line2_slash1]
    buyStockPrice1 = cutter[PRICE_COL][buy_line1_slash1 + 1:buy_line1_slash2]
    buyStockPrice2 = splice[PRICE_COL][buy_line2_slash1 + 1:buy_line2_slash2]
    sellPrice1 = cutter[PRICE_COL][A_pos1 + 2:sell_line1_slash1]
    sellPrice2 = splice[PRICE_COL][A_pos2 + 2:sell_line2_slash1]
    sellStockPrice1 = cutter[PRICE_COL][sell_line1_slash1 + 1:sell_line1_slash2]
    sellStockPrice2 = splice[PRICE_COL][sell_line2_slash1 + 1:sell_line2_slash2]
    #compares the prices
    if(buyPrice1 == buyPrice2):
        if(buyStockPrice1 != buyStockPrice2):
            answer = line1, "\n", line2
    elif(sellPrice1 == sellPrice2):
        if(sellStockPrice1 != sellStockPrice2):
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