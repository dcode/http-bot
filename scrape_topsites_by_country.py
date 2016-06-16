#!/usr/bin/env python2
from bs4 import BeautifulSoup
import requests
import sys
from math import ceil
from time import sleep
from random import randint

BASE_URL='http://www.alexa.com/topsites/countries;%d/%s'
USER_AGENT = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}


if __name__ == '__main__':

    if len(sys.argv) != 3:
        sys.stderr.write('Usage: COUNTRY-CODE TOP-N\n')
        sys.exit(1)

    country_code = sys.argv[1].upper()
    number = int(sys.argv[2])
    delimiter = ','

    page_numbers = int(ceil(number/25.0))

    for page_num in range(0, page_numbers):
        response = requests.get(BASE_URL % (page_num, country_code), headers=USER_AGENT)

        soup = BeautifulSoup(response.text, 'lxml')
        bullets = soup.find_all('li', {'class':'site-listing'})

        for bullet in bullets:
            rank = bullet.find('div', {'class':"count"}).get_text()
            site = bullet.find('div', {'class': 'desc-container'}).p.a.get_text().lower()
            print('%s%s%s' % (rank, delimiter, site))

        sleep(randint(0,5))