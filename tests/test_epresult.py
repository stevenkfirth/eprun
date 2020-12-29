# -*- coding: utf-8 -*-

import unittest
import eprun


class Test_EPResult(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        self.assertIsInstance(epresult,
                              eprun.epresult.EPResult)
        
        
    def test_files(self):
        ""
        self.assertEqual(list(epresult.files.keys()),
                         ['audit', 'bnd', 'dxf', 'eio', 'end', 'err', 'eso', 'mdd', 'mtd', 'mtr', 'rdd', 'shd', 'csv', 'htm', 'tab', 'txt', 'xml'])
        print(epresult.files)
    
    
    def test_get_end(self):
        ""
        self.assertIsInstance(epresult.get_end(),
                              eprun.epend.EPEnd)
        
    def test_get_err(self):
        ""
        self.assertIsInstance(epresult.get_err(),
                              eprun.eperr.EPErr)
        
    def test_get_eso(self):
        ""
        self.assertIsInstance(epresult.get_eso(),
                              eprun.epeso.EPEso)
        
    
    def test_returncode(self):
        ""
        self.assertEqual(epresult.returncode,
                         0)
        
        
    def test_stout(self):
        ""
        # this prints a long section of text
        #print(epresult.stdout)
        
    
    
if __name__=='__main__':
    
    epresult=eprun.eprun(input_filepath=r'files\1ZoneUncontrolled.idf',
                         epw_filepath=r'files\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
                         sim_dir='sim',
                         readvars=False)
    
    unittest.main(Test_EPResult())
    
    