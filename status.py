# !/usr/bin/python
import sys
import datetime
TIME_COL = 0
TOOL_COL = 3
ON_OFF_COL = 4
SYMBOL_COL = 6
YEAR_COL = 7
MONTH_COL = 8


def control_status(filename, time, tool):
    is_on = True
    statement = ""
    time_param = datetime.datetime.strptime(time, '%H:%M:%S')
    tool_arr = []
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
        if len(splitter) < MONTH_COL + 1:
            continue
        if splitter[TOOL_COL].find(tool) > -1:
            tool_arr.append(line)
    tool_arr.reverse()
    for x in tool_arr:
        cutter = x.split('|')
        date_time_obj = datetime.datetime.strptime(cutter[TIME_COL][0:8], '%H:%M:%S')
        if date_time_obj > time_param:
            continue
        else:
            if cutter[ON_OFF_COL].find("ON") > -1:
                is_on = True
            else:
                is_on = False
            if cutter[SYMBOL_COL].find("*") > -1:
                if is_on:
                    statement = ("Tool " + tool + " is on at time: " + str(date_time_obj))
                    return statement
                else:
                    statement = ("Tool " + tool + " is off at time: " + str(date_time_obj))
                    return statement
            elif cutter[YEAR_COL].find("-1") > -1:
                if is_on:
                    statement = ("Symbol " + cutter[SYMBOL_COL] + " is on at time: " + str(date_time_obj))
                    return statement
                else:
                    statement = ("Symbol " + cutter[SYMBOL_COL] + " is off at time: " + str(date_time_obj))
                    return statement
            else:
                if is_on:
                    statement = ("Symbol " + cutter[SYMBOL_COL] + " at year " + cutter[YEAR_COL] + " and month " + cutter[MONTH_COL] + " is on at time: " + str(date_time_obj))
                    return statement
                else:
                    statement = ("Symbol " + cutter[SYMBOL_COL] + " at year " + cutter[YEAR_COL] + " and month " + cutter[MONTH_COL] + " is off at time: " + str(date_time_obj))
                    return statement


def main():
    if len(sys.argv) < 4:
        print("Usage: ", sys.argv[0], "Filename Time Tool")
        exit(-1)
    filename = sys.argv[1]
    time = sys.argv[2]
    tool = sys.argv[3]
    answer = control_status(filename, time, tool)
    print(answer)


if __name__ == "__main__":
    main()