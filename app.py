import logging
import os
from time import sleep

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
     level=logging.INFO, 
     format= '[%(asctime)s] %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )

logging.info('App started')
urls = [
    'https://www.oreilly.com/programming/free',
    'https://www.oreilly.com/design/free/',
    'https://www.oreilly.com/data/free/',
    'https://www.oreilly.com/iot/free/',
    'https://www.oreilly.com/security/free/',
    'https://www.oreilly.com/web-platform/free/',
    'https://www.oreilly.com/webops/free/'
]
for url in urls:
    logging.info('Current download source : {}'.format(url))
    routes = url.split('https://www.oreilly.com/')
    routes = routes[0] if routes[0] else routes[1]
    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    books = ['https://www.oreilly.com/' + routes + '/files' + i['href'].split(routes)[-1].split('.csp')[0] + '.pdf'
             for i in soup.find_all('a', href=True) if routes in i['href']
             ]
    folder = routes.split('/')[0]
    if not os.path.exists(folder):
        os.mkdir(folder)

    for book in books:
        with open(os.path.join(folder, book.split('/')[-1]), 'wb') as f:
            f.write(requests.get(book).content)
        sleep(1)
        logging.info('book {} downloaded'.format(book.split('/')[-1]))
logging.info('Done. Have Fun!')
