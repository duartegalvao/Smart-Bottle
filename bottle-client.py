""" The bottle-client represents the actual bottle which carries a weight sensor
and a temperature sensor respectively. The bottle records sensor readings every
READ_INTERVAL minutes and stores them locally. Every SEND_INTERVAL, it sends
the readings to the server """

import requests

# TODO Implement dynamic generation of temperature and weight using numpy
# TODO Implement timestamp
payload = {'temp': '36', 'weight': '37'}
req = requests.post('http://localhost:8000/bottleAnalytics/bottleUpdate', data=payload)
print(req.text)



