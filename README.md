# Streaming flights data

There are few sources of streaming data to learn, so this is an attempt to create a self-contained and fairly interesting example of streaming data.

The streaming data is the 2015 flights data found on Kaggle (https://www.kaggle.com/usdot/flight-delays), streamed on the exact day and time of the flight. There are two streams (topics): Takeoffs (at time of takeoff) and landings (of time of landing). The streaming producer is capable of streaming both, but it should be done as two separate producers.

## What is here, and what isn't? 

- The data has to be downloaded from Kaggle and rearranged. The make_data folder is largely undocumented, but hopefully provides a startingpoint. In a future version I hope to provide this data as well, but the files are 1.3GB each, and doesn't fit nicely in VCS. In the meantime, there are some tiny samples in the picke files in /data
- The producer (docker image) is fairly flexible, if you look at `python_producer_image/flights_producer.py`, the main production function takes an iterable that must return JSONs, and each JSON must have a time field containing a datatime for when the message should be sent. Also, the data should be ordered by time. Data can be streamed to other places, by adding a new `sink` function.
- The flights-consumer image is far from 

Departing and arriving flights can be joined on the flight ID, a new sythetic column to uniquely identify the exact flight.