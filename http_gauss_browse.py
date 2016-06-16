#!/usr/bin/env python2
from multiprocessing import Pool
from time import sleep
from random import randint, gauss
import os, sys
import requests

from crawler import Crawler

## TODO
# . recursively download linked resources:
#   . images
#   . javascript
#   . css
#   . others?
# . follow redirects
#   . meta-refresh
#   . HTTP 300 codes
# . Vary user-agent

min_batch = 15  # Minimum time between batches is 15 secs
max_batch = 900 # Maxmimum time between batches i 15 mins

worker_sleep_min = 0
worker_sleep_max = 5

min_i = 1
max_i = 999   # Index of 1M
mu    = 500    # Pick the middle of 500
sigma = 150    # Guessing that 68.3% of traffic will be in top 150

def web_request(url):
    sleep(randint(worker_sleep_min, worker_sleep_max))
    r = requests.get(url, headers=USER_AGENT)
    return

def mainloop(argv=[]):
    pool = Pool(processes=6)              # start 6 worker processes
    if( len(argv) == 1):
        print "Usage: %s filename" % argv[0]
        sys.exit()

    filename = argv[1]
    alexa_sites = []
    with open(filename,'ro') as f:
        alexa_sites = f.readlines()

    print "Read %d entries." % len(alexa_sites)

    while True:
        # queue up to 1000 requests
        res = None
        for x in range(1000):
            result = gauss(mu, sigma)
            while (min_i < result < max_i) == False:
                result = gauss(mu, sigma)

            # Get distance from mean
            offset = int(abs(mu - result))
            url = "http://www.%s" % alexa_sites[offset].split(',')[1].strip()
            num_items = randint( 2, 50 )
            res = pool.apply_async(Crawler, (url, num_items ))

        print "Batch complete. Sleeping."
        sleep(randint(min_batch, max_batch))

    pool.close()
    pool.join()



if __name__ == '__main__':
    mainloop(sys.argv)
