# -*- coding: utf-8 -*-

import unittest
import eprun


class Test_eprun(unittest.TestCase):
   
    
    def test_eprun(self):
        ""
        result=eprun.eprun(input_filepath=r'files\1ZoneUncontrolled.idf',
                           epw_filepath=r'files\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
                           sim_dir='sim',
                           print_call=True,
                           readvars=False)
        
        self.assertIsInstance(result,
                              eprun.epresult.EPResult)
        
        self.assertEqual(result.returncode,
                         0)
        
    
    
if __name__=='__main__':
    
    unittest.main(Test_eprun())
    
    