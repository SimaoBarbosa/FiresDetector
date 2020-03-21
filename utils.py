import datetime
import dateutil.parser

def find_images(coords,sensing_date_FROM,sensing_date_TO,filename, sentinel=2) :
    global USERNAME
    global PASSWORD
    command = "dhusget.sh -u "+USERNAME+" -p "+PASSWORD +" -S "+sensing_date_FROM+" -E "+sensing_date_TO +" -c "+coords
    if sentinel !=0 :
        command = command + " -m Sentinel-"+ str(sentinel)
    command = command + " -q " + filename +  ".xml -C " + filename + ".csv"
    os.system(command)

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