# -*- coding: utf-8 -*-
# try something like
import urllib2
import json
import datetime
import threading
from skyscanner.skyscanner import Flights
from multiprocessing import Process, Pool

json_list=[]


def index():
    rows = db((db.airport_info.three_letter_code)).select(db.airport_info.city,db.airport_info.three_letter_code)
    json_data = json.dumps([{'name':r.city, 'code':r.three_letter_code} for r in rows])
    return dict(json_data=json_data)




def get_airport_code():
    src = db((db.user_airport_code.created_by==auth.user.id)).select(db.user_airport_code.three_letter_code)
    if not src:
        src = ''
    else:
        src = src.first().three_letter_code
    return src

def get_user_id():
    user_id = auth.user.id
    return user_id



def get_city_from_code(three_letter_code):
    if(three_letter_code):
        dest = db((db.airport_info.three_letter_code==three_letter_code)).select(db.airport_info.city).first().city
    else:
        dest = ''
    return dest


def process_data():
    dest_list = []
    start_index = request.args[0]
    start_index = start_index.replace('D','')
    ttl_duration = request.args[1]
    ttl_duration = ttl_duration.replace('F','')
    source = request.args[2]
    dest_count = len(request.args) - 3
    for i in range(3, 3+dest_count):
        dest_list.append(request.args[i])
    start_index = int(start_index)
    ttl_duration = int(ttl_duration)
    weekend_dates = populate_weekend_dates(start_index, ttl_duration)
    data = call_all_destinations(source, weekend_dates,dest_list, start_index)
    data = XML(response.json(data))
    return data



def request_flights(start_index, weekend_dates,departure_airport, dest):
    json_list=[]
    for arrival_airport in dest:
        for date in weekend_dates:
            departure_date = datetime.datetime.strftime(date,'%Y-%m-%d')
            return_date = ''
            if(start_index==4):
                return_date = datetime.datetime.strftime(date+datetime.timedelta(3),'%Y-%m-%d')
            elif(start_index==5):
                return_date = datetime.datetime.strftime(date+datetime.timedelta(2),'%Y-%m-%d')
            url = "http://partners.api.skyscanner.net/apiservices/browsedates/v1.0/US/USD/EN/"+departure_airport+"/"+arrival_airport+"/"+departure_date+"/"+return_date+"?apiKey=if781234598447854911313432786612"
            flight_list = []
            flight_info = { 'price': None, 'airline': None, 'departure_date': None, 'return_date':None, 'departure_airport': None, 'arrival_airport': None, 'url': None}
            try:
                json_text = json.load( urllib2.urlopen(url))
                if len(json_text["Quotes"]) > 0:
                    flight_info["price"] = json_text["Quotes"][0].get("MinPrice", "")
                    flight_info["airline"] = json_text["Carriers"][0].get("Name", "")
                else:
                    flight_info["price"] = None
                    flight_info["airline"] = "No Airline"

                flight_info["departure_date"] = departure_date
                flight_info["return_date"] = return_date
                flight_info["departure_airport"] = departure_airport
                flight_info["arrival_airport"] = arrival_airport
                flight_info["url"] = "https://www.skyscanner.net/transport/flights/" + departure_airport + "/" + arrival_airport + "/" + departure_date[2:4] + departure_date[5:7] + departure_date[8:10] +"/" + return_date[2:4] + return_date[5:7] + return_date[8:10]
                json_list.append(flight_info)
            except urllib2.HTTPError, e:
                json_text = e.read()
                json_list = json_text
    return json.loads(json.dumps(json_list))


def populate_weekend_dates(start_index, ttl_duration):
    today = datetime.datetime.today().weekday()
    weekend_dates = []
    start= ''
    if(today>=1):
        start = datetime.datetime.now() + datetime.timedelta(days=3)
    else:
        start = datetime.datetime.now()
    #3 months into the future
    end =  (start + datetime.timedelta(ttl_duration*365/12))
    begin = start
    delta = datetime.timedelta(days=1)
    diff = 0
    #ONLY CALCULATE FRIDAY SINCE YOU CAN DO THE MATH FOR SUNDAY..
    weekend = ''
    if(start_index==4):
        weekend = set([3])
    elif(start_index==5):
        weekend = set([4])
    else:
        weekend = set([4])
    while(begin<=end):
            if(begin.weekday() in weekend):
                    weekend_dates.append(begin)
                    diff+=1
            begin+=delta
    return weekend_dates

def call_all_destinations(source, weekend_dates,dest, start_index):
        data = request_flights(start_index, weekend_dates,source,dest)
        return data
