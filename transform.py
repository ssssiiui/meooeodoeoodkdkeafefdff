

UNCOMMENT ME

import csv
import re
import os

def path_fix(row):
    badpath = row['Path']
    match_ = re.search('^.*BestBuy >> ([^>]*) >>.*',badpath)
    site = match_.group(1)
    row['Path'] = site
    return row

def active_datefix(row):
    # Fix Dates
    baddate = row['Incident Time']
    match_ = re.search('([0-9]{1,2})/([0-9]{1,2})/([0-9]{4})',baddate)
    year = match_.group(3)
    month = match_.group(1)
    day =  match_.group(2)
    if (len(day) != 2):
        day = "0" + day
    if (len(month) != 2):
        month = "0" + month        
    match_ = re.search('([0-9]{1,2}):([0-9]{1,2})',baddate)
    hour = match_.group(1)
    minute = match_.group(2)

    if (len(hour) != 2):
        hour = "0" + hour
    if (len(minute) != 2):
        minute = "0" + minute                
    date = "{}-{}-{} {}:{}".format(year,month,day,hour,minute)
    row['Incident Time'] = date
    for key in row:
        row[key] = row[key].replace('\n', ' ').replace('\r', '')
    return row



 
def history_datefix(row):
    # Fix Dates
    baddate = row['Incident Time']
    match_ = re.search('([0-9]{2})/([0-9]{2})/([0-9]{4}) ([0-9]{2}):([0-9]{2})....(AM|PM)',baddate)
    year = match_.group(3)
    month = match_.group(1)
    day =  match_.group(2)
    hour = match_.group(4)
    minute = match_.group(5)
    meridian = match_.group(6)
    if (meridian == "PM"):
        hour = str(int(hour) + 12)
    if (len(day) != 2):
        day = "0" + day
    if (len(month) != 2):
        month = "0" + month
    if (len(hour) != 2):
        hour = "0" + hour
    if (len(minute) != 2):
        minute = "0" + minute                            
    date = "{}-{}-{} {}:{}".format(year,month,day,hour,minute)
    row['Incident Time'] = date

    baddate = row['Cleared Time']
    match_ = re.search('([0-9]{2})/([0-9]{2})/([0-9]{4}) ([0-9]{2}):([0-9]{2})....(AM|PM)',baddate)
    year = match_.group(3)
    month = match_.group(1)
    day =  match_.group(2)
    hour = match_.group(4)
    minute = match_.group(5)
    meridian = match_.group(6)
    if (meridian == "PM"):
        hour = str(int(hour) + 12)
    if (len(day) != 2):
        day = "0" + day
    if (len(month) != 2):
        month = "0" + month
    if (len(hour) != 2):
        hour = "0" + hour
    if (len(minute) != 2):
        minute = "0" + minute                            
    date = "{}-{}-{} {}:{}".format(year,month,day,hour,minute)
    row['Cleared Time'] = date
    for key in row:
        row[key] = row[key].replace('\n', ' ').replace('\r', '')
    return row

def csv_setup(filein,fileout,fields):
    f = open(filein, "r")
    fout = open(fileout,"w+", newline = '')
    csvfile = csv.DictReader(f,delimiter=',',quotechar='"')
    csvfileout = csv.DictWriter(fout,fieldnames=fields,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
    return (csvfile,csvfileout)
        
    
def main (hcsv="alarms-history.csv",hcsvout="alarms-history-out.csv",acsv="alarms-active.csv",acsvout="alarms-active-out.csv"):
    # History Manipulations
    hfields = ['ID','Device Name','Path','Description','Incident Time',
              'Cleared Time','Notes','ACK','Severity','Rules','Ticket',
              'Date Ignored','Ignore Until','Ignored By']    
    hcsvobj,hcsvobjout = csv_setup(hcsv,hcsvout,hfields)
    hcsvobjout.writeheader()
    count=0
    for row in hcsvobj:
        count+=1        
        print("HISTORY-FIX: " + str(count))                
        row = history_datefix(row)
        row = path_fix(row)
        hcsvobjout.writerow(row)        


    # Active Manipulations
    afields = ['ID', 'Device Name', 'Path', 'Description', 'Notes', 'ACK',
              'Severity', 'Rules', 'Incident Time', 'Ticket', 'Date Ignored',
              'Ignore Until', 'Reason', 'Ignored By']    
    acsvobj,acsvobjout = csv_setup(acsv,acsvout,afields)
    acsvobjout.writeheader()

    count=0
    for row in acsvobj:
        count+=1
        print("ACTIVE-FIX: " + str(count))        
        row = active_datefix(row)
        row = path_fix(row)
        acsvobjout.writerow(row)            
        
main()




