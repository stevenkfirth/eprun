# -*- coding: utf-8 -*-

import unittest
from eprun import EPEso
import datetime


class Test_EPEsoDailyVariable(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        self.assertEqual(str(v),
                         'EPEsoDailyVariable(report_code=51)')
        self.assertEqual(v._epesose,
                         se)
        self.assertEqual(v._report_code,
                         51)
            
        
    def test_get_dataframe(self):
        ""
        df=vs[0].get_dataframe()
        #print(df)
        
        
    def test_get_max_times(self):
        ""
        self.assertEqual(v.get_max_times(),
                         (datetime.datetime(2001, 12, 21, 0, 14, tzinfo=datetime.timezone.utc),))
        
        
    def test_get_min_times(self):
        ""
        self.assertEqual(v.get_min_times(),
                         (datetime.datetime(2001, 12, 21, 23, 59, tzinfo=datetime.timezone.utc),))
        
        
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
                         (-18.1438609435393,))
        
        
    def test_min_hours(self):
        ""
        self.assertEqual(v.min_hours,
                         (24,))
        
        
    def test_min_minutes(self):
        ""
        self.assertEqual(v.min_minutes,
                         (60,))
        
        
    def test_min_values(self):
        ""
        self.assertEqual(v.min_values,
                         (-18.145500357130768,))
        
    
    def test_object_name(self):
        ""
        self.assertEqual(v.object_name,
                         'ZN001:WALL001')
        
        
    def test_plot(self):
        ""
        #v.plot()
        
        
    def test_quantity(self):
        ""
        self.assertEqual(v.quantity,
                         'Surface Inside Face Temperature')
        
     
    def test_report_code(self):
        ""
        self.assertEqual(v.report_code,
                         51)

        
    def test_summary(self):
        ""
        self.assertEqual(v.summary(),
                         '51 - ZN001:WALL001 - Surface Inside Face Temperature (C)')
        
        
    def test_unit(self):
        ""
        self.assertEqual(v.unit,
                         'C')
                
        
    def test_values(self):
        ""
        self.assertEqual(v.values,
                         (-18.14473130427405,))   

    
if __name__=='__main__':
    
    e=EPEso(fp=r'files\eplusout.eso')
    envs=e.get_environments()
    se=envs[0]
    vs=se.get_daily_variables()
    v=vs[0]
    unittest.main(Test_EPEsoDailyVariable())
    
    