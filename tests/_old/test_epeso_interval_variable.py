# -*- coding: utf-8 -*-

import unittest
from eprun import EPEso


class Test_EPEsoIntervalVariable(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        self.assertEqual(str(v),
                         'EPEsoIntervalVariable(report_code=7)')
        self.assertEqual(v._epesose,
                         se)
        self.assertEqual(v._report_code,
                         7)
            
        
    def test_get_dataframe(self):
        ""
        df=vs[0].get_dataframe()
        #print(df)
        
        
    def test_get_series(self):
        s=vs[0].get_series()
        #print(s)
        
    
    def test_object_name(self):
        ""
        self.assertEqual(v.object_name,
                         'Environment')
        
        
    def test_plot(self):
        ""
        for v in vs:
            v.plot()
        
        
    def test_quantity(self):
        ""
        self.assertEqual(v.quantity,
                         'Site Outdoor Air Drybulb Temperature')
        
        
    def test_report_code(self):
        ""
        self.assertEqual(v.report_code,
                         7)
        
        
    def test_summary(self):
        ""
        self.assertEqual(v.summary(),
                         '7 - Environment - Site Outdoor Air Drybulb Temperature (C)')
        
        
    def test_unit(self):
        ""
        self.assertEqual(v.unit,
                         'C')
                
        
    def test_values(self):
        ""
        self.assertEqual(len(v.values),
                         24)
        self.assertEqual(str(v.values[0]),
                         '-15.5')
        

    
if __name__=='__main__':
    
    e=EPEso(fp=r'files\eplusout.eso')
    envs=e.get_environments()
    se=envs[0]
    vs=se.get_interval_variables()
    v=vs[0]
    unittest.main(Test_EPEsoIntervalVariable())
    
    