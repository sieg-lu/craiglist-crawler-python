# -*- coding: utf-8 -*-

__author__ = 'bilibili'

from time import time

from bs4 import BeautifulSoup
import mechanize

from craiglist_browser import craiglist_browser
from craiglist_logger import craiglist_logger
from craiglist_config import craiglist_config
from craiglist_crawler import craiglist_crawler

def prettify(content):
    soup = BeautifulSoup(''.join(content))
    return soup.prettify().encode('utf-8')

def test():
    c_browser = craiglist_browser()
#    url = c_browser.get_craiglist_search_page_url_with_restrictions('bmw 3', '5000', '8000', True)
    url = c_browser.get_craiglist_search_page_url('bmw 3')
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.open(url)
    web_content = browser.response().read()
    soup = BeautifulSoup(''.join(web_content))
    p_list = soup.findAll('p', {'class': 'row'})
    for i in p_list:
        for j in i.findAll('a', {'class': 'i'}):
            tmp = j.get('href')
            if tmp.endswith('.html'):
                print(j.get('href'))
    
    print soup.find('a', {'class': 'button next'})
    
#    logger.file_output('test.txt', )

def main():
    c_crawler = craiglist_crawler()
    c_crawler.run_crawler()

if __name__ == '__main__':
    start_time = time()
    main()
    end_time = time()
    print(str(end_time - start_time) + 's')

