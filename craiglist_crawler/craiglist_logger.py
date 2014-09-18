# -*- coding: utf-8 -*-

__author__ = 'bilibili'

import time

class craiglist_logger:
    m_file_name = ''
    m_raw_content = '----- START -----\n'
    
    # function: __init__(self, string)
    # @file_name -- string: the file name used to print the log into
    # return -- void
    def __init__(self, file_name='log.txt'):
        self.m_file_name = file_name
    
    # function: log_line(self, string)
    # @msg -- string: log a line
    # return -- void
    def log_line(self, msg):
        self.m_raw_content += str(time.strftime("%Y-%m-%d %X", time.localtime())) + ' --LOG: ' + msg + '\n'
        
    # function: log_line(self, string)
    # @msg -- string: log a line with "WARNING" mark
    # return -- void
    def log_warning(self, msg):
        self.m_raw_content += str(time.strftime("%Y-%m-%d %X", time.localtime())) + ' --WARNING: ' + msg + '\n'
        
    # function: log_line(self, string)
    # @msg -- string: log a line with "ERROR" mark
    # return -- void
    def log_error(self, msg):
        self.m_raw_content += str(time.strftime("%Y-%m-%d %X", time.localtime())) + ' --ERROR: ' + msg + '\n'
        
    # function: flush(self)
    # return -- void
    def flush(self):
        f = open(self.m_file_name, 'a')
        f.write(self.m_raw_content + '----- END -----\n\n')
        f.close()
        self.m_raw_content = '----- START -----\n'

    # static function: file_output
    # @file_name -- string: the file name used to print the message into
    # @msg -- string: the message
    # return -- void
    @staticmethod
    def file_output(file_name, msg):
        f = open(file_name, 'w')
        f.write(msg)
        f.close()