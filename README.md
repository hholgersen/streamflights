# Streaming flights data

There are few sources of streaming data to learn, so this is an attempt to create a self-contained and fairly interesting example of streaming data.

The streaming data is the 2015 flights data found on Kaggle (https://www.kaggle.com/usdot/flight-delays), streamed on the exact day and time of the flight. There are two streams (topics): Takeoffs (at time of takeoff) and landings (of time of landing).

Departing and arriving flights can be joined on the flight ID, a new sythetic column to uniquely identify the exact flight.

