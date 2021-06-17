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
        if len(splitter) < 4:
            continue
        # KJSR - Performance note: Don't create this date object until after you know this line has PRICES
        date_time_obj1 = datetime.datetime.strptime(splitter[TIME_COL][0:12], '%H:%M:%S.%f')
        if splitter[PRICE_COL].startswith("PRICES") == False:
            continue
        strike = splitter[PRICE_COL][12:16]

        #KJSR 
        # You're searching the dictionary one item at a time. This is like searching a real dictionary 
        #starting at the first word. That is O(n) performance. 
        #Use the language's much faster lookup which is likely O(log(n))
        # In this case it's 
        # if Dict.has_key(strike):
        #    dict_strike_data = Dict[strike]
        
        for key in Dict:
            if strike == key:
                seperate = Dict[key].split('|')
                date_time_obj2 = datetime.datetime.strptime(seperate[TIME_COL][0:12], '%H:%M:%S.%f')
                if date_time_obj1 == date_time_obj2:
                    answer = comp(line, Dict[key])
                    if answer != "No errors":
                        return answer
                    else:
                        continue #KJSR - At this point you already found the strike but there are no errors. You want to break or continue? 
                else:
                    Dict[key] = line
                    break
        if len(Dict) == 0:
            Dict[strike] = line        
        elif Dict[strike] == line:  #KJSR - this clause is unnecessary. It does the same thing as the else clause below it right?
            continue
        else:
            Dict[strike] = line
    return answer

def comp(line1, line2):
    #KJSR - You need to rewrite this function.
    # You can't assume each number will always use the same number of digits.
    #What if the number was 13.26342593 instead of 3.26342593?
    #You CAN assume the format of the line is constant, but not the number of digits
    #So, you can assume buyPrice1 is between "B:" and the first "/". 
    #you can assume buyPrice2 is between the first and 2nd "/" characters
    #etc
    # Note: It's always nice to put sample data as a comment in your code (when feasible) to give you somthing to refer to easily
    #815818496|IN|PRICES NG1NC2750 B:0.5170/3.26342593/Y A:0.5220/3.27332736/Y
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