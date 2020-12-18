# -*- coding: utf-8 -*-

import unittest
from eprun import EPEso
import eprun
from pprint import pprint
import pandas as pd

class Test_EPEsoSimulationEnvironment(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        self.assertIsInstance(se._data,
                              dict)    
        self.assertEqual(se._epeso,
                         e)
        self.assertEqual(se._index,
                         0)
    
    
    def test_elevation(self):
        ""
        self.assertEqual(se.elevation,
                         2)
    
    
    def test_environment_title(self):
        ""
        self.assertEqual(se.environment_title,
                         'DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB')


    def test_get_annual_dataframe(self):
        ""

    
    
    def test_get_annual_periods(self):
        ""
        

    def test_get_annual_summary(self):
        ""


        
    def test_get_annual_variables(self):
        ""
        
        
    def test_get_annual_variable(self):
        ""
        
        
        
    def test_get_daily_dataframe(self):
        ""
        df=se.get_daily_dataframe()
        #print(df)
        #df.to_csv(r'files\test.csv')
        
        
    def test_get_daily_periods(self):
        ""
        self.assertIsInstance(se.get_daily_periods(),
                              eprun.epeso_daily_periods.EPEsoDailyPeriods)
    
    
    def test_get_daily_summary(self):
        ""
        self.assertEqual(se.get_daily_summary().encode(),
                         b'Starts at 2001-12-21T00:00:00+00:00, 1 periods @ 1 day intervals\n51 - ZN001:WALL001 - Surface Inside Face Temperature (C)\n52 - ZN001:WALL001 - Surface Outside Face Temperature (C)\n53 - ZN001:WALL001 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n54 - ZN001:WALL001 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n55 - ZN001:WALL002 - Surface Inside Face Temperature (C)\n56 - ZN001:WALL002 - Surface Outside Face Temperature (C)\n57 - ZN001:WALL002 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n58 - ZN001:WALL002 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n59 - ZN001:WALL003 - Surface Inside Face Temperature (C)\n60 - ZN001:WALL003 - Surface Outside Face Temperature (C)\n61 - ZN001:WALL003 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n62 - ZN001:WALL003 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n63 - ZN001:WALL004 - Surface Inside Face Temperature (C)\n64 - ZN001:WALL004 - Surface Outside Face Temperature (C)\n65 - ZN001:WALL004 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n66 - ZN001:WALL004 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n67 - ZN001:FLR001 - Surface Inside Face Temperature (C)\n68 - ZN001:FLR001 - Surface Outside Face Temperature (C)\n69 - ZN001:FLR001 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n70 - ZN001:ROOF001 - Surface Inside Face Temperature (C)\n71 - ZN001:ROOF001 - Surface Outside Face Temperature (C)\n72 - ZN001:ROOF001 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n73 - ZN001:ROOF001 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n8 - Environment - Site Daylight Saving Time Status (-)\n9 - Environment - Site Day Type Index (-)')
    
    
    def test_get_daily_variables(self):
        ""
        self.assertEqual(str(se.get_daily_variables()),
                         '(EPEsoDailyVariable(report_code=51), EPEsoDailyVariable(report_code=52), EPEsoDailyVariable(report_code=53), EPEsoDailyVariable(report_code=54), EPEsoDailyVariable(report_code=55), EPEsoDailyVariable(report_code=56), EPEsoDailyVariable(report_code=57), EPEsoDailyVariable(report_code=58), EPEsoDailyVariable(report_code=59), EPEsoDailyVariable(report_code=60), EPEsoDailyVariable(report_code=61), EPEsoDailyVariable(report_code=62), EPEsoDailyVariable(report_code=63), EPEsoDailyVariable(report_code=64), EPEsoDailyVariable(report_code=65), EPEsoDailyVariable(report_code=66), EPEsoDailyVariable(report_code=67), EPEsoDailyVariable(report_code=68), EPEsoDailyVariable(report_code=69), EPEsoDailyVariable(report_code=70), EPEsoDailyVariable(report_code=71), EPEsoDailyVariable(report_code=72), EPEsoDailyVariable(report_code=73), EPEsoDailyVariable(report_code=8), EPEsoDailyVariable(report_code=9))')
        
        
    def test_get_daily_variable(self):
        ""
        self.assertEqual(str(se.get_daily_variable(51)),
                         'EPEsoDailyVariable(report_code=51)')
                         
            
    def test_get_interval_dataframe(self):
        ""
        df=se.get_interval_dataframe()
        #print(df)
        #df.to_csv(r'files\test.csv')
        
        
    def test_get_interval_periods(self):
        ""
        self.assertIsInstance(se.get_interval_periods(),
                              eprun.epeso_interval_periods.EPEsoIntervalPeriods)
    
    
    def test_get_interval_summary(self):
        ""
        self.assertEqual(se.get_interval_summary().encode(),
                         b'Starts at 2001-12-21T00:00:00+00:00, 24 periods @ 60 minute intervals\n7 - Environment - Site Outdoor Air Drybulb Temperature (C)\n47 - ZONE ONE - Zone Total Internal Latent Gain Energy (J)\n74 - ZONE ONE - Zone Mean Radiant Temperature (C)\n75 - ZONE ONE - Zone Mean Air Temperature (C)\n76 - ZONE ONE - Zone Air Heat Balance Surface Convection Rate (W)\n77 - ZONE ONE - Zone Air Heat Balance Air Energy Storage Rate (W)')
    
    
    def test_get_interval_variable(self):
        ""
        self.assertEqual(str(se.get_interval_variable(7)),
                         'EPEsoIntervalVariable(report_code=7)')
        
    
    def test_get_interval_variables(self):
        ""
        self.assertEqual(str(se.get_interval_variables()),
                         '[EPEsoIntervalVariable(report_code=7), EPEsoIntervalVariable(report_code=47), EPEsoIntervalVariable(report_code=74), EPEsoIntervalVariable(report_code=75), EPEsoIntervalVariable(report_code=76), EPEsoIntervalVariable(report_code=77)]')
        
    
        
    def test_get_monthly_dataframe(self):
        ""
        
        
    def test_get_monthly_periods(self):
        ""
        
        
    def test_get_monthly_summary(self):
        ""
        
        
    def test_get_monthly_variables(self):
        ""
        
    def test_get_monthly_variable(self):
        ""
        
        
        
    def test_get_number_of_variables(self):
        ""
        self.assertEqual(se.get_number_of_variables(),
                         {'interval': 6, 
                          'daily': 25, 
                          'monthly': 3, 
                          'runperiod': 0, 
                          'annual': 0})
        
        
    def test_get_run_period_dataframe(self):
        ""
        
        
    def test_get_run_period_periods(self):
        ""
        
    def test_get_run_period_summary(self):
        ""
        
        
    def test_get_run_period_variables(self):
        ""
        
    def test_get_run_period_variable(self):
        ""
        
        
        
    def test_get_timezone(self):
        ""
        
        
    def test_get_variables(self):
        ""    
        #print(se.get_variables())
        
    
    def test_latitude(self):
        ""
        
    def test_longitude(self):
        ""

    def test_summary(self):
        ""
        print(se.summary())

        
    def test_time_zone(self):
        ""
        
        
        
        
    
if __name__=='__main__':
    
    e=EPEso(fp=r'files\eplusout.eso')
    envs=e.get_environments()
    se=envs[0]
    unittest.main(Test_EPEsoSimulationEnvironment())
    
    