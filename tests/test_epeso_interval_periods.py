# -*- coding: utf-8 -*-

import unittest
from eprun import EPEso
from pprint import pprint
import pandas as pd
import datetime


class Test_EPEsoIntervalPeriods(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        self.assertIsInstance(p._data,
                              tuple)
        self.assertEqual(p._epesose,
                         se)
        
    
    def test_days_of_simulation(self):
        ""
        self.assertEqual(p.days_of_simulation,
                         (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
        
        
    def test_months(self):
        ""
        self.assertEqual(p.months,
                         (12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12))
        
        
    def test_days_of_month(self):
        ""
        self.assertEqual(p.days_of_month,
                         (21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21))
        
        
    def test_dst_indicators(self):
        ""
        self.assertEqual(p.dst_indicators,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        
        
    def test_hours(self):
        ""
        self.assertEqual(p.hours,
                         (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24))
        
        
    def test_start_minutes(self):
        ""
        self.assertEqual(p.start_minutes,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        
        
    def test_end_minutes(self):
        ""
        self.assertEqual(p.end_minutes,
                         (60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60))
        
        
    def test_day_types(self):
        ""
        self.assertEqual(p.day_types,
                         ('WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay'))
        
        
    def test_get_start_times(self):
        ""
        self.assertEqual(p.get_start_times(),
                         (datetime.datetime(2001, 12, 21, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 1, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 2, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 3, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 4, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 5, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 6, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 7, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 8, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 9, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 10, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 11, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 12, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 13, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 14, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 15, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 16, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 17, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 18, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 19, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 20, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 21, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 22, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 23, 0, tzinfo=datetime.timezone.utc)))
        
        
    def test_get_end_times(self):
        ""
        self.assertEqual(p.get_end_times(),
                         (datetime.datetime(2001, 12, 21, 1, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 2, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 3, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 4, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 5, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 6, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 7, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 8, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 9, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 10, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 11, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 12, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 13, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 14, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 15, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 16, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 17, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 18, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 19, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 20, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 21, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 22, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 23, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 22, 0, 0, tzinfo=datetime.timezone.utc)))
        
        
    def test_get_interval(self):
        ""
        self.assertEqual(p.get_interval(),
                         datetime.timedelta(minutes=60))
        
        
    def test_get_periods(self):
        ""
        self.assertEqual(str(p.get_periods()),
                         "[Period('2001-12-21 00:00:00', '3600S'), Period('2001-12-21 01:00:00', '3600S'), Period('2001-12-21 02:00:00', '3600S'), Period('2001-12-21 03:00:00', '3600S'), Period('2001-12-21 04:00:00', '3600S'), Period('2001-12-21 05:00:00', '3600S'), Period('2001-12-21 06:00:00', '3600S'), Period('2001-12-21 07:00:00', '3600S'), Period('2001-12-21 08:00:00', '3600S'), Period('2001-12-21 09:00:00', '3600S'), Period('2001-12-21 10:00:00', '3600S'), Period('2001-12-21 11:00:00', '3600S'), Period('2001-12-21 12:00:00', '3600S'), Period('2001-12-21 13:00:00', '3600S'), Period('2001-12-21 14:00:00', '3600S'), Period('2001-12-21 15:00:00', '3600S'), Period('2001-12-21 16:00:00', '3600S'), Period('2001-12-21 17:00:00', '3600S'), Period('2001-12-21 18:00:00', '3600S'), Period('2001-12-21 19:00:00', '3600S'), Period('2001-12-21 20:00:00', '3600S'), Period('2001-12-21 21:00:00', '3600S'), Period('2001-12-21 22:00:00', '3600S'), Period('2001-12-21 23:00:00', '3600S')]")
        
        
    def test_summary(self):
        ""
        self.assertEqual(p.summary(),
                         'Starts at 2001-12-21T00:00:00+00:00, 24 periods @ 60 minute intervals')
        
    
if __name__=='__main__':
    
    e=EPEso(fp=r'files\eplusout.eso')
    envs=e.get_environments()
    se=envs[0]
    p=se.get_interval_periods()
    unittest.main(Test_EPEsoIntervalPeriods())
    
    