import datetime
import dateutil.parser
import time
import re
import os

def date_to_iso_format (date,time,before=True):
    date = str(date)
    if (date=="nan") :
        return "nan"
    splited = date.split('/')
    dt = datetime.datetime(int(splited[2]), int(splited[1]),  int(splited[0]))
    iso = str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day)
    newtime = "T" + time + ".000Z"
    iso = iso +  newtime
    return iso

def iso_to_ymd(iso_date):
	return str(dateutil.parser.parse(iso_date).date())


def dmy_to_ymd (date):
    date = str(date)
    if (date=="nan") :
        return "nan"
    splited = date.split('/')
    dt = datetime.datetime(int(splited[2]), int(splited[1]),  int(splited[0]))
    return str(dt.date())

def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'E' or direction == 'N':
        dd *= -1
    return dd;

def dms_to_decimal(text,direction):
    splited = text.split(':')
    if len(splited) < 3 : 
        return "0"
    else :
        degrees = splited[0]
        minutes = splited[1]
        seconds = splited[2].replace('\'', "")
    result = dms2dd(degrees, minutes, seconds, direction)
    return result

def wait_for_downloads(sleep_time,num_imgs):
	downloadpath = "C:/Users/SimãoPauloLealBarbos/Downloads/"
	regexp = re.compile(r'.*tar.gz')
	downloaded = 0
	downloads = []
	while ( True ) : 
	    possible_downloads = os.listdir(downloadpath) 
	    downloaded = 0
	    downloads = []
	    for download in possible_downloads :
	        if regexp.search(download) :
	            downloaded+=1
	            downloads.append(download)
	    if downloaded < num_imgs :
	    	time.sleep(sleep_time)
	    else :
	    	return downloads