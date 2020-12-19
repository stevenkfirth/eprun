# -*- coding: utf-8 -*-

import unittest
from eprun import EPEso
from pprint import pprint
import pandas as pd
import datetime


class Test_EPEsoDailyPeriods(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        self.assertIsInstance(p._data,
                              tuple)
        self.assertEqual(p._epesose,
                         se)
        
    
    def test_cumulative_days_of_simulation(self):
        ""
        self.assertEqual(p.cumulative_days_of_simulation,
                         (1, ))
        
        
    def test_days_of_month(self):
        ""
        self.assertEqual(p.days_of_month,
                         (21, ))
        
        
    def test_dst_indicators(self):
        ""
        self.assertEqual(p.dst_indicators,
                         (0, ))
        
        
    def test_get_end_times(self):
        ""
        self.assertEqual(p.get_end_times(),
                         (datetime.datetime(2001, 12, 22, 0, 0, tzinfo=datetime.timezone.utc), ))
        
        
    def test_get_interval(self):
        ""
        self.assertEqual(p.get_interval(),
                         datetime.timedelta(days=1))
        
        
    def test_get_periods(self):
        ""
        self.assertEqual(str(p.get_periods()),
                         "[Period('2001-12-21 00:00:00', '86400S')]")
        
        
    def test_get_start_times(self):
        ""
        self.assertEqual(p.get_start_times(),
                         (datetime.datetime(2001, 12, 21, 0, 0, tzinfo=datetime.timezone.utc), ))
    
        
    def test_months(self):
        ""
        self.assertEqual(p.months,
                         (12,))
    
        
        
    def test_summary(self):
        ""
        self.assertEqual(p.summary(),
                         'Starts at 2001-12-21T00:00:00+00:00, 1 periods @ 1 day intervals')
        
        
        
        
        
    
if __name__=='__main__':
    
    e=EPEso(fp=r'files\eplusout.eso')
    envs=e.get_environments()
    se=envs[0]
    p=se.get_daily_periods()
    unittest.main(Test_EPEsoDailyPeriods())
    
    