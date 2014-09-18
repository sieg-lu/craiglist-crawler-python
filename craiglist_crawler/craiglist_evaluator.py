# -*- coding: utf-8 -*-

__author__ = 'bilibili'

from craiglist_browser import craiglist_browser

class craiglist_evaluator:
    # singleton class, no locks integrated, modifying in multiprocessing is forbidden
    m_instance = None

    @staticmethod
    def get_instance():
        if craiglist_evaluator.m_instance == None:
            craiglist_evaluator.m_instance = craiglist_evaluator()
        return craiglist_evaluator.m_instance

    def evaluate(self, url):
        web_content = craiglist_browser.get_raw_content(url)
        return True