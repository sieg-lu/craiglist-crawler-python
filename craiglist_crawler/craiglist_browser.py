# -*- coding: utf-8 -*-

__author__ = 'bilibili'

import types
import mechanize
from craiglist_logger import craiglist_logger

class craiglist_browser:
    m_craiglist_url = ''
    m_logger = craiglist_logger('my_craiglist_browser.log')

    # restricted conditions
    m_min_price_embedded = '-1'
    m_max_price_embedded = '-1'
    m_pic_checked = False
    m_category = u'sss'

    # function: __init__(self, string)
    # @base_url -- string: the craiglist's base url, 'http://boston.craigslist.org/' by default
    # return: void
    def __init__(self, base_url = 'http://boston.craigslist.org/'):
        self.m_logger.log_line('base url: ' + base_url)
        self.m_craiglist_url = base_url

    # function: get_craiglist_base_url(self)
    # return -- string: craiglist base url
    def get_craiglist_base_url(self):
        return self.m_craiglist_url

    # function: __del__(self)
    # return: void
    def __del__(self):
        self.m_logger.log_line('deleting the my_craiglist_browser\n----- END -----\n')
        self.m_logger.flush()

    # function: get_raw_content(string)
    # @url -- string: the page's url
    # return -- string: the raw content of the page
    @staticmethod
    def get_raw_content(url):
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.open(url)
        return browser.response().read()
    
    # function: submit_filled_form(self, string, tuple)
    # @url -- string: the base url
    # @form_id -- string: the id string representing the form that needs to be submitted
    # @arg_tuple -- tuple: the arguments
    #                      *** (string, string), (string, bool), (string, list) ***
    #                      ***  <input>           <checkbox>      <option>
    # return -- string: the search result page's url
    def submit_filled_form(self, url, form_id, arg_tuple):
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.open(url)
        for form in browser.forms():
            if form.attrs['id'] == form_id:
                browser.form = form
                break
        for i in range(len(arg_tuple)):
            if type(arg_tuple[i][1]) == types.BooleanType:
                browser.form.find_control(name=arg_tuple[i][0]).items[0].selected = arg_tuple[i][1]
            else: # type(arg_tuple[i][1]) == types.StringType:
                browser[arg_tuple[i][0]] = arg_tuple[i][1]
        
        browser.submit()
        return browser.response().geturl()
       
    # function: get_craiglist_search_page_url(self, string)
    # @keyword -- string: the keyword for searching
    # return -- string: the search result page's url
    def get_craiglist_search_page_url(self, keyword):
        self.m_logger.log_line('keyword: ' + keyword)
        return  self.submit_filled_form(self.m_craiglist_url, 'search', (('query', keyword), ('catAbb', ['sss'])))

    # function: reset_restrictions(self):
    # return -- void
    def reset_restrictions(self):
        self.m_min_price_embedded = '-1'
        self.m_max_price_embedded = '-1'
        self.m_pic_checked = False
        self.m_category = u'sss'

    # setter function: set_min_price(self, string)
    # @price -- int: the price given to the m_min_price_embedded
    #        -- None: did nothing
    # return -- void
    def set_min_price(self, price):
        if price == None:
            return
        self.m_min_price_embedded = price

    # setter function: set_max_price(self, string)
    # @price -- int: the price given to the m_max_price_embedded
    #        -- None: did nothing
    # return -- void
    def set_max_price(self, price):
        if price == None:
            return
        self.m_max_price_embedded = price

    # setter function: set_pic_checked(self, bool)
    # @checked -- bool: the price given to the m_pic_checked
    #          -- None: did nothing
    # return -- void
    def set_pic_checked(self, checked):
        if checked == None:
            return
        self.m_pic_checked = checked

    # setter function: set_pic_checked(self, string)
    # @cate -- string: the price given to the m_category
    #       -- None: did nothing
    # return -- void
    def set_category(self, cate):
        if cate == None:
            return
        self.m_category = cate

    def log_current_restrictions(self):
        self.m_logger.log_line('current restrictions:')
        self.m_logger.log_line('m_category: ' + str(self.m_category))
        self.m_logger.log_line('m_min_price_embedded: ' + str(self.m_min_price_embedded))
        self.m_logger.log_line('m_max_price_embedded: ' + str(self.m_max_price_embedded))
        self.m_logger.log_line('m_pic_checked: ' + str(self.m_pic_checked))
        self.m_logger.flush()

    # function: get_craiglist_search_page_url_with_restrictions(string) 
    #           *** see get_craiglist_search_page_url_with_restrictions_deprecated for more details ***
    # @keyword -- string: the keyword for searching
    # return -- string: the search result page's url
    def get_craiglist_search_page_url_with_restrictions(self, keyword):
        self.log_current_restrictions()
        arg_list = [('query', keyword), ('hasPic', self.m_pic_checked), ('catAbb', [self.m_category])]
        if self.m_min_price_embedded != '-1':
            arg_list.append(('minAsk', self.m_min_price_embedded))
        if self.m_max_price_embedded != '-1':
            arg_list.append(('maxAsk', self.m_max_price_embedded))

        tmp_url = self.get_craiglist_search_page_url(keyword)
        self.m_logger.log_line('intermediate url: ' + tmp_url)
        return self.submit_filled_form(tmp_url, 'searchform', tuple(arg_list))

    # ***** deprecated *****  
    # function: get_craiglist_search_page_url_with_restrictions_deprecated(string, string, string, bool)
    # @keyword -- string: the keyword for searching
    # @min_price_embedded -- string: the MINIMUM price accepted for the search results, which is a input form in the page
    #                                *** NO "string->int" Checking ***
    # @max_price_embedded -- string: the MAXIMUM price accepted for the search results, which is a input form in the page
    #                                *** NO "string->int" Checking ***
    # @pic_checked -- bool: whether we should check the checkbox, "hasPic"
    # return -- string: the search result page's url
    #                   *** NO "min < max" Checking ***
    def get_craiglist_search_page_url_with_restrictions_deprecated(self, keyword, min_price_embedded, max_price_embedded, pic_checked):
        tmp_url = self.get_craiglist_search_page_url(keyword)
        self.m_logger.log_line('intermediate url: ' + tmp_url)
        return self.submit_filled_form(tmp_url, 'searchform', \
                                       (('query', keyword), ('minAsk', min_price_embedded), \
                                        ('maxAsk', max_price_embedded), ('hasPic', pic_checked)))

def test_craiglist_browser():
    c_browser = craiglist_browser()
    print c_browser.get_craiglist_search_page_url_with_restrictions('bmw 3')
    c_browser.set_min_price('6000')
    print c_browser.get_craiglist_search_page_url_with_restrictions('bmw 3')
    c_browser.set_max_price('8000')
    print c_browser.get_craiglist_search_page_url_with_restrictions('bmw 3')
    c_browser.set_pic_checked(True)
    print c_browser.get_craiglist_search_page_url_with_restrictions('bmw 3')
    c_browser.set_category('hhh')
    print c_browser.get_craiglist_search_page_url_with_restrictions('bmw 3')
#    print c_browser.submit_filled_form('http://boston.craigslist.org/', 'search', (('query', 'bmw 3'), ('catAbb', ['sss'])))
#    print c_browser.get_craiglist_search_page_url('bmw 3')
#    print c_browser.get_craiglist_search_page_url_with_restrictions('bmw 3', '5000', '8000', True)

