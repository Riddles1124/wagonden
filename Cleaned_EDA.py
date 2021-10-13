#!/usr/bin/env python

import datetime as dt
import sqlite3
import pandas as pd
import numpy as np

def html_list(startdate, enddate):
    tsdate = startdate
    outlist = []
    while tsdate <= enddate:
        outlist.append(tsdate)
        date = dt.datetime.strptime(str(tsdate), '%y%m%d')
        date += dt.timedelta(days=7)
        tsdate = int(date.strftime('%y%m%d'))
    return outlist

def dataframe_creator(scraping_list):
    db = dict()
    for ind, timeval in enumerate(scraping_list):
        db[ind] = pd.read_csv(f'http://web.mta.info/developers/data/nyct/turnstile/turnstile_{timeval}.txt')
    return db

def local_database_creator(startdate=180623, weeks=14):
    conn = sqlite3.connect('ts_database')
    c = conn.cursor()
    datetime = (dt.datetime.strptime(str(startdate), '%y%m%d') + dt.timedelta(weeks=weeks-1))
    enddate = int(datetime.strftime('%y%m%d'))
    startdate = int((dt.datetime.strptime(str(startdate), '%y%m%d') - dt.timedelta(weeks = 1)).strftime('%y%m%d'))
    scraping_list = html_list(startdate, enddate)
    for val in scraping_list:
        date = str(val)
        c.execute(f"CREATE TABLE IF NOT EXISTS TS{date} ([STATION] TEXT)")
    conn.commit()
    db = dataframe_creator(scraping_list)
    for ind, val in enumerate(scraping_list):
        db[ind].to_sql(f'TS{val}', conn, if_exists = 'replace', index = False)
    print("Database Created")
    return scraping_list


tslist = local_database_creator()
tsdata = dict()

for val in tslist:
    tsdata[val] = pd.read_sql(f'''SELECT  "STATION", "DATE", "TIME", "ENTRIES", "EXITS",
                                    CASE WHEN "TIME" = "04:00:00" THEN "BENCH 1"
                                    WHEN "TIME" = "16:00:00" THEN "BENCH 2"
                                    WHEN "TIME" = "08:00:00" THEN "COUNT 1"
                                    WHEN "TIME" = "12:00:00" THEN "COUNT 2"
                                    ELSE "COUNT 3" END AS "TYPE"
                                    FROM "TS{str(val)}"
                                    WHERE "TIME" = "08:00:00" OR "TIME" = "12:00:00" OR "TIME" = "20:00:00" OR "TIME" = "04:00:00" OR "TIME" ="16:00:00"
                                    GROUP BY "DATE", "STATION", "TIME";''', sqlite3.connect('ts_database.db'))



print(tslist[0])
print(tsdata.keys())
frame = tsdata[180606]
bench1 = (frame[(frame["DATE"] == date) & (frame["TYPE"] == "BENCH 1") & (frame["STATION"] == station)][["ENTRIES","EXITS"]].sum(axis=1).sort_index())


def daybreaker(tsdata):
    traffic = dict()
    for key in tsdata.keys():
        frame = tsdata[key]
        for date in sorted(set(frame["DATE"])):
            for station in frame["STATION"]:
                bench1 = (frame[(frame["DATE"] == date) & (frame["TYPE"] == "BENCH 1") & (frame["STATION"] == station)][["ENTRIES","EXITS"]].sum(axis=1).sort_index())
                count1 = (frame[(frame["DATE"] == date) & (frame["TYPE"] == "COUNT 1") & (frame["STATION"] == station)][["ENTRIES","EXITS"]].sum(axis=1).sort_index())
                count2 = (frame[(frame["DATE"] == date) & (frame["TYPE"] == "COUNT 2") & (frame["STATION"] == station)][["ENTRIES","EXITS"]].sum(axis=1).sort_index())
                bench2 = (frame[(frame["DATE"] == date) & (frame["TYPE"] == "BENCH 2") & (frame["STATION"] == station)][["ENTRIES","EXITS"]].sum(axis=1).sort_index())
                count3 = (frame[(frame["DATE"] == date) & (frame["TYPE"] == "COUNT 3") & (frame["STATION"] == station)][["ENTRIES","EXITS"]].sum(axis=1).sort_index())
                am = count1-bench1
                mor = count2-count1
                eve = count3-bench2
            traffic[date] = {station: [am, mor, eve]}
    return traffic

traffic = daybreaker(tsdata)

print(traffic[])



# CUMVALUE TRAFFIC ROUTE:
# SQL:
# f'''SELECT "STATION", "DATE", "TIME", SUM("ENTRIES" + "EXITS") AS CUMTRAFFIC
#                                   FROM "TS{str(val)}"
#                                   WHERE "TIME" = "08:00:00" OR "TIME" = "12:00:00" OR "TIME" = "20:00:00"
#                                   GROUP BY "STATION", "DATE"
#                                   ORDER BY "STATION", "DATE", "TIME";''', sqlite3.connect('ts_database.db'))
# # for val in range(len(tslist)):
#     tsdata[val]["TRAFFIC"] = tsdata[val].CUMTRAFFIC.diff(1)
#     if val >= 1:
#         tsdata[val].loc[0,"TRAFFIC"] = tsdata[val-1].iloc[-1,-1]

# station_pop = dict()
# mask = dict()


# for val in range(len(tsdata)):
#     mask[val] = tsdata[val].groupby(["DATE", "STATION"]).TRAFFIC.agg('max')
#     station_pop[val] = pd.DataFrame(mask[val]).reset_index()
#     # if val == 1:
#     #     station_pop[val].iloc[0,-1] = station_pop[val-1].iloc[-1,-1]

# popframe = dict()

# print(pd.DataFrame(station_pop[1].sort_values("TRAFFIC", ascending=False)))

# for val in range(1,len(tsdata)):
#     for date in set(station_pop[val]["DATE"]):
#         popframe[date] = station_pop[val][station_pop[val]["DATE"]==date].sort_values("TRAFFIC", ascending=False).head(5)


# stationlist=[]

# for date in sorted(popframe.keys()):
#     for station in popframe[date]["STATION"]:
#         stationlist.append(station)

# from collections import Counter

# test = dict(Counter(stationlist))
# bestest = []
# finaldict = dict()

# for ind, val in enumerate(test.keys()):
#     if ind < 10:
#         bestest.append(val)

# for val in test.keys():
#     if val in bestest:
#         finaldict[val] = test[val]

# print(finaldict)

# import matplotlib
# import matplotlib.pyplot as plt


# keys = [l if not i%2 else '\n'+l for i,l in enumerate(finaldict.keys())]
# values = finaldict.values()

# plt.bar(keys, values)
# plt.xlabel('Station Name')
# plt.ylabel('Number Of Instances in Top 5')

# plt.savefig('/Users/wragonface/Desktop/saved.png')






# for val in range(1,len)

# Dbtest = pd.read_sql('''SELECT "STATION", "DATE", "TIME", SUM("ENTRIES" + "EXITS") AS TRAFFIC
# FROM "TS180623"
# WHERE "TIME" = "08:00:00" OR "TIME" = "12:00:00" OR "TIME" = "20:00:00"
# GROUP BY "STATION", "DATE"
# ORDER BY "TRAFFIC" DESC, "DATE";''', sqlite3.connect('ts_database.db'))
