import pickle
import queue
import datetime
import dateutil
from time import sleep
from kafka import KafkaProducer
from json import dumps

class custom_clock():
    import datetime
    
    def __init__(self, starttime = datetime.datetime.now()):
        self.invocation_time = datetime.datetime.now()
        self.starttime = starttime
    
    def get_time(self):
        elapsed = datetime.datetime.now() - self.invocation_time
        return(self.starttime + elapsed)
    
    
def produce_flights(flights_pickle, 
                    sink,
                    start_time = datetime.datetime.now(), 
                    data_year = 2015):
    
    handle = open(flights_pickle, 'rb')
    departures = pickle.load(handle)
    q = queue.Queue()
    for i in departures:
    q.put(i)

    DATA_YEAR = 2015

    clock = custom_clock(datetime.datetime.strptime('20200101 06:15', '%Y%m%d %H:%M'))
    years_to_add = clock.get_time().year - DATA_YEAR
    years_delta = dateutil.relativedelta.relativedelta(years=years_to_add)

     while not q.empty():
        departure = q.get()
        departure['departure_dt'] = departure['departure_dt'] + years_delta
        wait =  (departure['departure_dt'] - clock.get_time()).total_seconds()
        departure['departure_dt'] = str(departure['departure_dt'])
        keybite = bytes(departure['id'], encoding='utf-8')
        try:
            sleep(wait)
            producer.send("departures", key=keybite, value=departure)
            producer.flush()
        except:
            pass
            
            
if __name__ == '__main__':
    
    start_time = datetime.datetime.strptime('20200101 06:15', '%Y%m%d %H:%M')
    
    produce_flights('/app/departures.pickle', None, start_time = start_time)
            
            
            
            