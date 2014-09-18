# -*- coding: utf-8 -*-

__author__ = 'bilibili'

import multiprocessing
from bs4 import BeautifulSoup
from craiglist_logger import craiglist_logger
from craiglist_config import craiglist_config
from craiglist_browser import craiglist_browser
from craiglist_evaluator import craiglist_evaluator

class craiglist_filter_result:
    def __init__(self, wanted, url):
        self.m_wanted = wanted
        self.m_url = url

# function: thread_job(string, ?)
# @url -- string: the page that needs to be checked
# return -- craiglist_filter_result: whether this url is great or not
def process_url(url):
    return craiglist_filter_result(craiglist_evaluator.get_instance().evaluate(url), url)

class craiglist_crawler:
    m_logger = craiglist_logger('my_craiglist_crawler.log')
    m_config = craiglist_config()
    m_browser = craiglist_browser()

    MAX_DEPTH_ALLOWED = 5

    m_current_index = 0

    # function: collect_href_urls_within_page(self, string)
    # @raw_content -- string: the raw content of the page
    # return -- list: a list that contains all the available hrefs on this page
    def collect_href_urls_within_page(self, raw_content):
        soup = BeautifulSoup(''.join(raw_content))
        p_list = soup.findAll('p', {'class': 'row'})
        res_list = []
        for i in p_list:
            for j in i.findAll('a', {'class': 'i'}):
                tmp = j.get('href')
                if tmp.endswith('.html'):
                    if not tmp.startswith('http'):
                        res_list.append(self.m_browser.get_craiglist_base_url() + tmp[1 : len(tmp)])
                    else:
                        res_list.append(tmp)
        return res_list

    # function: get_next_or_prev(self, string, bool)
    # @raw_content -- string: the raw content of the page
    # @next -- bool: get next page? False = prev page
    # return -- string: the next/prev page's url
    #        -- None: no next/prev page
    def get_next_or_prev(self, raw_content, next):
        soup = BeautifulSoup(''.join(raw_content))
        if next:
            button_tag = 'button next'
        else:
            button_tag = 'button prev'
        button = soup.find('a', {'class': button_tag})
        if button != None:
            tmp = button.get('href')
            return self.m_browser.get_craiglist_base_url() + tmp[1 : len(tmp)]
        return None

    # function: get_next_page(self, string)
    # @raw_content -- string: the raw content of the page
    # return -- string: the next page's url
    #        -- None: no next page
    def get_next_page(self, raw_content):
        return self.get_next_or_prev(raw_content, True)

    # function: get_next_page(self, string)
    # @raw_content -- string: the raw content of the page
    # return -- string: the prev page's url
    #        -- None: no prev page
    def get_prev_page(self, raw_content):
        return self.get_next_or_prev(raw_content, False)

    # function: collect_pages_url_within_max_depth(self, string, string)
    #           collecting the urls through the "next" button recursively, limited by the initial depth
    # @current_url -- string: the current url the crawler is visiting
    # @current_depth -- int: the current depth
    # return -- list: the urls that are collected
    # exception -- IndexError: if the depth is larger than MAX_DEPTH_ALLOWED
    def collect_pages_url_within_max_depth(self, current_url, current_depth):
        if current_depth > self.MAX_DEPTH_ALLOWED:
            raise IndexError("you are searching too deep!")
        if current_depth <= 0:
            return []
        web_content = craiglist_browser.get_raw_content(current_url)
        next_url = self.get_next_page(web_content)
        res = [current_url]
        if next_url == None:
            return res
        res.extend(self.collect_pages_url_within_max_depth(next_url, current_depth - 1))
        return res

    # function: collect_item_urls(self, list)
    # @page_urls -- list: the list of urls pointing to the page that are needed to be searched
    # return -- list: all the item urls
    def collect_item_urls(self, page_urls):
        res = []
        for i in range(len(page_urls)):
            web_content = craiglist_browser.get_raw_content(page_urls[i])
            res.extend(self.collect_href_urls_within_page(web_content))
        return res

    # function: filter_urls_multiprocessing(self, list)
    # @urls -- list: the collection of urls that needs to be checked
    # return -- list: the GREAT url collection which pass the evaluation
    def filter_urls_multiprocessing(self, urls):
        pool = multiprocessing.Pool(10)
        tmp = pool.map(process_url, urls)
        res = []
        for i in range(len(tmp)):
            if tmp[i].m_wanted:
                res.append(tmp[i].m_url)
        return res

    # function: filter_urls_singleprocess(self, list)
    # @urls -- list: the collection of urls that needs to be checked
    # return -- list: the GREAT url collection which pass the evaluation
    def filter_urls_singleprocess(self, urls):
        res = []
        for i in range(len(urls)):
            if craiglist_evaluator.evaluate(urls[i]):
                res.append(urls[i])
        return res

    # function: run_crawler(self)
    # return -- void
    def run_crawler(self):
        self.m_browser.reset_restrictions()
        self.m_browser.set_min_price(self.m_config.get_attr(self.m_current_index, 'min_price'))
        self.m_browser.set_max_price(self.m_config.get_attr(self.m_current_index, 'max_price'))
        self.m_browser.set_pic_checked(self.m_config.get_attr(self.m_current_index, 'check_pic'))
        url = self.m_browser.get_craiglist_search_page_url_with_restrictions( \
                self.m_config.get_attr(self.m_current_index, 'keyword'))
        print url
        
#        web_content = craiglist_browser.get_raw_content(url)
#        print self.collect_href_urls_within_page(web_content)
#        print self.get_next_page(web_content)
        tmp = self.collect_pages_url_within_max_depth(url, self.m_config.get_max_page_searched())
        urls = self.collect_item_urls(tmp)
        print len(self.filter_urls_multiprocessing(urls))
        #self.filter_urls(urls)
