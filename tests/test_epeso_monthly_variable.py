# -*- coding: utf-8 -*-

import unittest
from eprun import EPEso
import datetime


class Test_EPEsoMonthlyVariable(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        self.assertEqual(str(v),
                         'EPEsoMonthlyVariable(report_code=48)')
        self.assertEqual(v._epesose,
                         se)
        self.assertEqual(v._report_code,
                         48)
            
        
    def test_get_dataframe(self):
        ""
        df=vs[0].get_dataframe()
        #print(df)
        
        
    def test_get_max_times(self):
        ""
        self.assertEqual(v.get_max_times(),
                         (datetime.datetime(2001, 12, 21, 1, 15, tzinfo=datetime.timezone.utc),))
        
        
    def test_get_min_times(self):
        ""
        self.assertEqual(v.get_min_times(),
                         (datetime.datetime(2001, 12, 21, 1, 15, tzinfo=datetime.timezone.utc),))
        
        
    def test_max_hours(self):
        ""
        self.assertEqual(v.max_hours,
                         (1,))
        
        
    def test_max_minutes(self):
        ""
        self.assertEqual(v.max_minutes,
                         (15,))
        
        
    def test_max_values(self):
        ""
        self.assertEqual(v.max_values,
                         (316800.0,))
        
        
    def test_min_hours(self):
        ""
        self.assertEqual(v.min_hours,
                         (1,))
        
        
    def test_min_minutes(self):
        ""
        self.assertEqual(v.min_minutes,
                         (15,))
        
        
    def test_min_values(self):
        ""
        self.assertEqual(v.min_values,
                         (316800.0,))
        
    
    def test_object_name(self):
        ""
        self.assertEqual(v.object_name,
                         'TEST 352A')
        
        
    def test_plot(self):
        ""
        #v.plot()
        
        
    def test_quantity(self):
        ""
        self.assertEqual(v.quantity,
                         'Other Equipment Total Heating Energy')
        
     
    def test_report_code(self):
        ""
        self.assertEqual(v.report_code,
                         48)

        
    def test_summary(self):
        ""
        self.assertEqual(v.summary(),
                         '48 - TEST 352A - Other Equipment Total Heating Energy (J)')
        
        
    def test_unit(self):
        ""
        self.assertEqual(v.unit,
                         'J')
                
        
    def test_values(self):
        ""
        self.assertEqual(v.values,
                         (30412800.0,))   

    
if __name__=='__main__':
    
    e=EPEso(fp=r'files\eplusout.eso')
    envs=e.get_environments()
    se=envs[0]
    vs=se.get_monthly_variables()
    v=vs[0]
    unittest.main(Test_EPEsoMonthlyVariable())
    
    