# -*- coding: utf-8 -*-

import unittest
from eprun import EPEnd


class Test_EPEnd(unittest.TestCase):
   
    def test_EPEnd(self):
        ""
        e=EPEnd(fp=r'files\eplusout.end')
        
        self.assertEqual(e.line.encode(),
                         b'EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.28sec\n')
        
        
if __name__=='__main__':
    
    unittest.main(Test_EPEnd())