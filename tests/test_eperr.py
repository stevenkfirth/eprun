# -*- coding: utf-8 -*-

import unittest
from eprun import EPErr


class Test_EPErr(unittest.TestCase):
   
        
    def test_EPErr(self):
        ""
        e=EPErr(fp=r'files\eplusout.err')
        #print(e.lines)
        print(e.firstline)
        print(e.warnings[0])
        print(e.lastline)
    
    
if __name__=='__main__':
    
    unittest.main(Test_EPErr())

