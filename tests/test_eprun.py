# -*- coding: utf-8 -*-

import unittest
from eprun import eprun


class Test_eprun(unittest.TestCase):
   
    
        
    def test_eprun(self):
        ""
        result=eprun(idf_filepath='1ZoneUncontrolled.idf',
                     epw_filepath='USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
                     sim_dir='sim',
                     readvars=False)
        print(result)
        
        print(result.returncode)
        print(result.stdout)
        print(result.files)
    
        print(type(result))
        print(type(result.returncode))
    
    
if __name__=='__main__':
    
    unittest.main(Test_eprun())
    
    