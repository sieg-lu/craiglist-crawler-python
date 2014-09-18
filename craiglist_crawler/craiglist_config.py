# -*- coding: utf-8 -*-

__author__ = 'bilibili'

import json

class craiglist_config:
    # function: __init__(self, string)
    # @file_name -- string: the json config file name
    # return -- void
    def __init__(self, file_name='config.json'):
        f = file(file_name)
        self.m_raw_dict = json.load(f)
        f.close()
        if not self.m_raw_dict.has_key('search'):
            raise AttributeError('search tag does not exist in the context')

    # static function: get_default_attr(string)
    # @key -- string: the key to the default value
    # return -- string: default value to the key, if default value exists
    #        -- None: default value does not exist
    @staticmethod
    def get_default_attr(key):
        if key == 'catAbb':
            return u'sss'
        elif key == 'check_pic':
            return 'False'
        return None

    # function: get_max_page_searched(self)
    # return -- int: the max page depth that should be searched
    def get_max_page_searched(self):
        if not self.m_raw_dict.has_key('max_page_searched'):
            return 1
        return int(self.m_raw_dict['max_page_searched'])

    # function: get_attr(self, int, string)
    # @index -- int: the index of the searching item
    # @key -- string: the key in the dictionary
    # return -- string: the item corresponded to the key
    #        -- bool: for the checkbox item
    #        -- list: only for 'catAbb' key
    #        -- None: the key is not existed in the dict
    def get_attr(self, index, key):
        if (index >= len(self.m_raw_dict['search'])):
            return None
        if self.m_raw_dict['search'][index].has_key(key):
            content = self.m_raw_dict['search'][index][key]
        else:
            content = craiglist_config.get_default_attr(key)
        if key == 'catAbb':
            return [content]
        if content == 'True' or content == 'False':
            return bool(content)
        return content

def test_craiglist_config():
    c_config = craiglist_config()
    print c_config.get_attr(2, 'keyword')
    print c_config.get_attr(3, 'keyword')
    print c_config.get_attr(0, 'not exist')
    print c_config.get_attr(0, 'catAbb')
    print c_config.get_attr(1, 'catAbb')
    print c_config.get_max_page_searched()

# test_craiglist_config()