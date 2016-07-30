from pyiso import client_factory
import pandas as pd
from datetime import datetime, timedelta
import math

## uses Watt Time pyiso library
caiso = client_factory('CAISO')

## user defines start and end dates
print("enter your start date. format example 2015-01-01 00:00")
start = str(input())

print("enter your end date. format example 2015-03-31 00:00")
end = str(input())

days = 30
start_time = datetime.strptime(start, '%Y-%m-%d %H:%M')
end_time = datetime.strptime(end, '%Y-%m-%d %H:%M')
time_range =  (start_time - end_time).days * -1
periods = math.ceil(time_range / 30)

## create lists of start and end dates
def queryDates(Start):
    timeDateQueryStart = datetime.strptime(Start, '%Y-%m-%d %H:%M')
    end = []
    beginning = []
    for i in range(periods):
        timeDateNewStart = timeDateQueryStart + timedelta(days = days) * range(periods)[i]
        beginning.append(timeDateNewStart)
        timeDateQueryEnd = timeDateNewStart + timedelta(days = days)
        end.append(timeDateQueryEnd)
    return beginning, end

date_ranges = CAISOquery(start)
query_begin = list(date_ranges[0])
query_end = list(date_ranges[1])
## reduce last time period to the right number of days
query_end[-1] = query_end[-1] - (query_end[-1] - end_time)

## passes dates through pyiso get_load function
def queryCAISO(begin, end):
    months = []
    for i in range(periods):
        month = caiso.get_load(start_at = begin[i], end_at = end[i])
        months.append(month)
    return months

## warning: the queryCAISO function takes several minutes to execute.
query_results = queryCAISO(query_begin, query_end)

## builds pandas dataframe
def buildDF(results):
    CAISO2015 = []
    for i in range(periods):
        frame = pd.DataFrame(results[i])
        CAISO2015.append(frame)
    return CAISO2015

def formatDF(rawDF):
    CAISO_fullResults = buildDF(rawDF)
    CAISO_fullTable = pd.concat(CAISO_fullResults)
    CAISO_indexed = CAISO_fullTable.set_index(['timestamp']).tz_convert('US/Pacific')
    CAISO_final = CAISO_indexed.sort_index()
    return CAISO_final

CAISO_finalTable = formatDF(query_results)
