# -*- coding: utf-8 -*-

import unittest
from eprun import eprun, EPEnd, EPErr


class Test_eprun(unittest.TestCase):
   
    
        
    def _test_eprun(self):
        ""
        result=eprun(idf_filepath=r'files\1ZoneUncontrolled.idf',
                     epw_filepath=r'files\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
                     sim_dir='sim',
                     readvars=False)
        print(result)
        
        print(result.returncode)
        print(result.stdout)
        print(result.files)
    
        print(type(result))
        print(type(result.returncode))
        
        print(result.get_end().line)
    
    
    def test_EPEnd(self):
        ""
        e=EPEnd(fp=r'files\eplusout.end')
        
        self.assertEqual(e.line.encode(),
                         b'EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.28sec\n')
        
        
    def test_EPErr(self):
        ""
        e=EPErr(fp=r'files\eplusout.err')
        #print(e.lines)
        print(e.firstline)
        print(e.warnings[0])
        print(e.lastline)
    
    
if __name__=='__main__':
    
    unittest.main(Test_eprun())
    
    