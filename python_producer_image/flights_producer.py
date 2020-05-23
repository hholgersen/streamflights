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
    
    
producer = KafkaProducer(
   value_serializer=lambda m: dumps(m).encode('utf-8'), 
   bootstrap_servers=['kafka:9093'])


def send_flights(message):
    keybite = bytes(message['id'], encoding='utf-8')
    producer.send("departures", key=keybite, value=message)
    producer.flush()

def flightsgenerator(filepath):
    with open(filepath) as f:
        for line in f:
            yield line
    
def produce_flights(json_obj, 
                    sink,
                    time_field,
                    start_time = datetime.datetime.now()
                   ):
    '''
    Send elements of a JSON file to a sink, at a specified time specified in the JSON.
    The time field must be of type datetime, and the field name must be specified in `time_field`.
    
    Known bug: Really a design flaw, but many events at the same time will result in not all being sent.
        Need to create a "send window" instead of fixed moment.
    
    @param json_obj: List or iterable returning JSON
    @param sink: Callback function that gets called for each element
    @param time_field: Datetime object containing the time it gets sent. This gets serialized before sinking.
    @param start_time: Optional datetime for simulating a different time.
    '''
    
    q = queue.Queue()
    
    for i in json_obj:
        q.put(i)

    clock = custom_clock(start_time)

    while not q.empty():
        departure = q.get()

        wait =  (departure[time_field] - clock.get_time()).total_seconds()
        departure[time_field] = str(departure[time_field])
        
        if wait>=0:
            sleep(wait)
            sink(departure)


            
if __name__ == '__main__':
        
    departures = flightsgenerator('flights/arrivals.txt')
    
    start_time = datetime.datetime.strptime('20150101 06:15', '%Y%m%d %H:%M')
    
    produce_flights(departures, send_flights, 'departure_dt', start_time = start_time)
            
            
            
            