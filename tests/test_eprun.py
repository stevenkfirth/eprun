# -*- coding: utf-8 -*-

import unittest

import eprun
from eprun import runsim, EPEnd, EPErr, EPEso

from pprint import pprint
import pandas as pd
import datetime


# code below creates the test files

epresult=runsim(input_filepath=r'files\1ZoneUncontrolled.idf',
                epw_filepath=r'files\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
                sim_dir='sim',
                readvars=False)
end=EPEnd(fp=r'files\eplusout.end')
err=EPErr(fp=r'files\eplusout.err')
eso=EPEso(fp=r'files\eplusout.eso')


class Test_eprun(unittest.TestCase):
    ""
   
    def test_eprun(self):
        ""
        
        self.assertIsInstance(epresult,
                              eprun.eprun.EPResult)
        
        self.assertEqual(epresult.returncode,
                          0)
        
        
        
class Test_EPResult(unittest.TestCase):
    ""
    
    def test___init__(self):
        ""
        self.assertIsInstance(epresult,
                              eprun.eprun.EPResult)
        
        
    def test_files(self):
        ""
        self.assertEqual(list(epresult.files.keys()),
                         ['audit', 'bnd', 'dxf', 'eio', 'end', 'err', 
                          'eso', 'mdd', 'mtd', 'mtr', 'rdd', 'shd', 
                          'csv', 'htm', 'tab', 'txt', 'xml'])
    
    
    def test_get_end(self):
        ""
        self.assertIsInstance(epresult.get_end(),
                              EPEnd)
        
        
    def test_get_err(self):
        ""
        self.assertIsInstance(epresult.get_err(),
                              EPErr)
        
        
    def test_get_eso(self):
        ""
        self.assertIsInstance(epresult.get_eso(),
                              EPEso)
        
    
    def test_returncode(self):
        ""
        self.assertEqual(epresult.returncode,
                         0)
        
        
    def test_stout(self):
        ""
        # this prints a long section of text
        #print(epresult.stdout)
        
        
    
class Test_EPEnd(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.end=end
   
      
    def test_EPEnd(self):
        ""
        self.assertEqual(self.end.line.encode(),
                         b'EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.28sec')
        
  

class Test_EPErr(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.err=err
    
   
    def test_EPErr(self):
        ""
        self.assertEqual(str(type(self.err)),
                         "<class 'eprun.eprun.EPErr'>")
        
        
    def test_firstline(self):
        ""
        self.assertEqual(self.err.firstline.strip(),
                         'Program Version,EnergyPlus, Version 9.4.0-998c4b761e, YMD=2020.11.13 06:25,')
        
        
    def test_lastline(self):
        ""
        self.assertEqual(self.err.lastline.strip(),
                         'EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.33sec')
        
        
    def test_lines(self):
        ""
        self.assertEqual(self.err.lines.encode(),
                         b'Program Version,EnergyPlus, Version 9.4.0-998c4b761e, YMD=2020.11.13 06:25,\n   ** Warning ** Weather file location will be used rather than entered (IDF) Location object.\n   **   ~~~   ** ..Location object=DENVER CENTENNIAL  GOLDEN   N_CO_USA DESIGN_CONDITIONS\n   **   ~~~   ** ..Weather File Location=San Francisco Intl Ap CA USA TMY3 WMO#=724940\n   **   ~~~   ** ..due to location differences, Latitude difference=[2.12] degrees, Longitude difference=[17.22] degrees.\n   **   ~~~   ** ..Time Zone difference=[1.0] hour(s), Elevation difference=[99.89] percent, [1827.00] meters.\n   ** Warning ** SetUpDesignDay: Entered DesignDay Barometric Pressure=81198 differs by more than 10% from Standard Barometric Pressure=101301.\n   **   ~~~   ** ...occurs in DesignDay=DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB, Standard Pressure (based on elevation) will be used.\n   ** Warning ** SetUpDesignDay: Entered DesignDay Barometric Pressure=81198 differs by more than 10% from Standard Barometric Pressure=101301.\n   **   ~~~   ** ...occurs in DesignDay=DENVER CENTENNIAL  GOLDEN   N ANN CLG 1% CONDNS DB=>MWB, Standard Pressure (based on elevation) will be used.\n   ************* Testing Individual Branch Integrity\n   ************* All Branches passed integrity testing\n   ************* Testing Individual Supply Air Path Integrity\n   ************* All Supply Air Paths passed integrity testing\n   ************* Testing Individual Return Air Path Integrity\n   ************* All Return Air Paths passed integrity testing\n   ************* No node connection errors were found.\n   ************* Beginning Simulation\n   ************* Simulation Error Summary *************\n   ************* EnergyPlus Warmup Error Summary. During Warmup: 0 Warning; 0 Severe Errors.\n   ************* EnergyPlus Sizing Error Summary. During Sizing: 0 Warning; 0 Severe Errors.\n   ************* EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.33sec\n')
        
        
    def test_severes(self):
        ""
        self.assertEqual(self.err.severes,
                         [])
                         #["<root> - Object required to validate 'required' properties."])
        
        
    def test_warnings(self):
        ""
        self.assertEqual(self.err.warnings[0].encode(),
                         b'Weather file location will be used rather than entered (IDF) Location object. ..Location object=DENVER CENTENNIAL  GOLDEN   N_CO_USA DESIGN_CONDITIONS ..Weather File Location=San Francisco Intl Ap CA USA TMY3 WMO#=724940 ..due to location differences, Latitude difference=[2.12] degrees, Longitude difference=[17.22] degrees. ..Time Zone difference=[1.0] hour(s), Elevation difference=[99.89] percent, [1827.00] meters.')
    
        

class Test_EPEso(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.eso=eso
   
    
    def test___init__(self):
        ""
        self.assertIsInstance(self.eso,
                              EPEso)
        
        
    def test_get_environment(self):
        ""
        se=self.eso.get_environment('RUN PERIOD 1')
        self.assertEqual(str(se),
                         'EPEsoSimuationEnvironment(environment_title="RUN PERIOD 1")')
        
    def test_get_environments(self):
        ""
        envs=self.eso.get_environments()
        #print(str(envs))
        self.assertIsInstance(envs,
                              list)
        self.assertEqual(len(envs),
                         3)
        self.assertIsInstance(envs[0],
                              eprun.eprun.EPEsoSimulationEnvironment)
        
        
    def test_programme_version_statement(self):
        ""
        self.assertEqual(self.eso.programme_version_statement,
                         {'programme': 'EnergyPlus', 
                          'version': 'Version 9.4.0-998c4b761e', 
                          'timestamp': 'YMD=2020.11.13 06:25'})
        
        
    def test_standard_items_dictionary(self):
        ""
        self.assertEqual(self.eso.standard_items_dictionary,
                         {1: {'comment': None,
                             'items': [{'name': 'Environment Title', 'unit': None},
                                       {'name': 'Latitude', 'unit': 'deg'},
                                       {'name': 'Longitude', 'unit': 'deg'},
                                       {'name': 'Time Zone', 'unit': None},
                                       {'name': 'Elevation', 'unit': 'm'}],
                             'number_of_values': 5},
                         2: {'comment': None,
                             'items': [{'name': 'Day of Simulation', 'unit': None},
                                       {'name': 'Month', 'unit': None},
                                       {'name': 'Day of Month', 'unit': None},
                                       {'name': 'DST Indicator', 'unit': '1=yes 0=no'},
                                       {'name': 'Hour', 'unit': None},
                                       {'name': 'StartMinute', 'unit': None},
                                       {'name': 'EndMinute', 'unit': None},
                                       {'name': 'DayType', 'unit': None}],
                             'number_of_values': 8},
                         3: {'comment': 'When Daily Report Variables Requested',
                             'items': [{'name': 'Cumulative Day of Simulation', 'unit': None},
                                       {'name': 'Month', 'unit': None},
                                       {'name': 'Day of Month', 'unit': None},
                                       {'name': 'DST Indicator', 'unit': '1=yes 0=no'},
                                       {'name': 'DayType', 'unit': None}],
                             'number_of_values': 5},
                         4: {'comment': 'When Monthly Report Variables Requested',
                             'items': [{'name': 'Cumulative Days of Simulation', 'unit': None},
                                       {'name': 'Month', 'unit': None}],
                             'number_of_values': 2},
                         5: {'comment': 'When Run Period Report Variables Requested',
                             'items': [{'name': 'Cumulative Days of Simulation', 'unit': None}],
                             'number_of_values': 1},
                         6: {'comment': 'When Annual Report Variables Requested',
                             'items': [{'name': 'Calendar Year of Simulation', 'unit': None}],
                             'number_of_values': 1}}    
                         )
        
            
    def test_variable_dictionary(self):
        ""
        self.assertEqual(list(self.eso.variable_dictionary.keys()),
                         [7, 8, 9, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 
                          60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77])
        self.assertEqual(self.eso.variable_dictionary[7],
                         {'comment': 'Hourly',
                          'number_of_values': 1,
                          'object_name': 'Environment',
                          'quantity': 'Site Outdoor Air Drybulb Temperature',
                          'unit': 'C'}
                         )
        
        
        
class Test_EPEsoSimulationEnvironment(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.env=eso.get_environments()[0]
        
    
    def test___init__(self):
        ""
        self.assertIsInstance(self.env._data,
                              dict)    
        self.assertEqual(self.env._epeso,
                         eso)
        self.assertEqual(self.env._index,
                         0)
    
    
    def test_elevation(self):
        ""
        self.assertEqual(self.env.elevation,
                         2)
    
    
    def test_environment_title(self):
        ""
        self.assertEqual(self.env.environment_title,
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
        df=self.env.get_daily_dataframe()
        #print(df)
        #df.to_csv(r'files\test.csv')
        
        
    def test_get_daily_periods(self):
        ""
        self.assertIsInstance(self.env.get_daily_periods(),
                              eprun.eprun.EPEsoDailyPeriods)
    
    
    def test_get_daily_summary(self):
        ""
        self.assertEqual(self.env.get_daily_summary().encode(),
                         b'Starts at 2001-12-21T00:00:00+00:00, 1 periods @ 1 day intervals\n51 - ZN001:WALL001 - Surface Inside Face Temperature (C)\n52 - ZN001:WALL001 - Surface Outside Face Temperature (C)\n53 - ZN001:WALL001 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n54 - ZN001:WALL001 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n55 - ZN001:WALL002 - Surface Inside Face Temperature (C)\n56 - ZN001:WALL002 - Surface Outside Face Temperature (C)\n57 - ZN001:WALL002 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n58 - ZN001:WALL002 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n59 - ZN001:WALL003 - Surface Inside Face Temperature (C)\n60 - ZN001:WALL003 - Surface Outside Face Temperature (C)\n61 - ZN001:WALL003 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n62 - ZN001:WALL003 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n63 - ZN001:WALL004 - Surface Inside Face Temperature (C)\n64 - ZN001:WALL004 - Surface Outside Face Temperature (C)\n65 - ZN001:WALL004 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n66 - ZN001:WALL004 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n67 - ZN001:FLR001 - Surface Inside Face Temperature (C)\n68 - ZN001:FLR001 - Surface Outside Face Temperature (C)\n69 - ZN001:FLR001 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n70 - ZN001:ROOF001 - Surface Inside Face Temperature (C)\n71 - ZN001:ROOF001 - Surface Outside Face Temperature (C)\n72 - ZN001:ROOF001 - Surface Inside Face Convection Heat Transfer Coefficient (W/m2-K)\n73 - ZN001:ROOF001 - Surface Outside Face Convection Heat Transfer Coefficient (W/m2-K)\n8 - Environment - Site Daylight Saving Time Status (-)\n9 - Environment - Site Day Type Index (-)')
    
    
    def test_get_daily_variables(self):
        ""
        self.assertEqual(str(self.env.get_daily_variables()),
                         '(EPEsoDailyVariable(report_code=51), EPEsoDailyVariable(report_code=52), EPEsoDailyVariable(report_code=53), EPEsoDailyVariable(report_code=54), EPEsoDailyVariable(report_code=55), EPEsoDailyVariable(report_code=56), EPEsoDailyVariable(report_code=57), EPEsoDailyVariable(report_code=58), EPEsoDailyVariable(report_code=59), EPEsoDailyVariable(report_code=60), EPEsoDailyVariable(report_code=61), EPEsoDailyVariable(report_code=62), EPEsoDailyVariable(report_code=63), EPEsoDailyVariable(report_code=64), EPEsoDailyVariable(report_code=65), EPEsoDailyVariable(report_code=66), EPEsoDailyVariable(report_code=67), EPEsoDailyVariable(report_code=68), EPEsoDailyVariable(report_code=69), EPEsoDailyVariable(report_code=70), EPEsoDailyVariable(report_code=71), EPEsoDailyVariable(report_code=72), EPEsoDailyVariable(report_code=73), EPEsoDailyVariable(report_code=8), EPEsoDailyVariable(report_code=9))')
        
        
    def test_get_daily_variable(self):
        ""
        self.assertEqual(str(self.env.get_daily_variable(51)),
                         'EPEsoDailyVariable(report_code=51)')
                         
            
    def test_get_interval_dataframe(self):
        ""
        df=self.env.get_interval_dataframe()
        #print(df)
        #df.to_csv(r'files\test.csv')
        
        
    def test_get_interval_periods(self):
        ""
        #self.assertIsInstance(self.env.get_interval_periods(),
        #                      eprun.epeso_interval_periods.EPEsoIntervalPeriods)
    
    
    def test_get_interval_summary(self):
        ""
        self.assertEqual(self.env.get_interval_summary().encode(),
                         b'Starts at 2001-12-21T00:00:00+00:00, 24 periods @ 60 minute intervals\n7 - Environment - Site Outdoor Air Drybulb Temperature (C)\n47 - ZONE ONE - Zone Total Internal Latent Gain Energy (J)\n74 - ZONE ONE - Zone Mean Radiant Temperature (C)\n75 - ZONE ONE - Zone Mean Air Temperature (C)\n76 - ZONE ONE - Zone Air Heat Balance Surface Convection Rate (W)\n77 - ZONE ONE - Zone Air Heat Balance Air Energy Storage Rate (W)')
    
    
    def test_get_interval_variable(self):
        ""
        self.assertEqual(str(self.env.get_interval_variable(7)),
                         'EPEsoIntervalVariable(report_code=7)')
        
    
    def test_get_interval_variables(self):
        ""
        self.assertEqual(str(self.env.get_interval_variables()),
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
        self.assertEqual(self.env.get_number_of_variables(),
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
        #print(se.summary())

        
    def test_time_zone(self):
        ""
        
        
        
class Test_EPEsoDailyPeriods(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.env=eso.get_environments()[0]
        self.daily_periods=self.env.get_daily_periods()
        
    
    def test___init__(self):
        ""
        self.assertIsInstance(self.daily_periods._data,
                              tuple)
        self.assertEqual(self.daily_periods._epesose,
                         self.env)
        
    
    def test_cumulative_days_of_simulation(self):
        ""
        self.assertEqual(self.daily_periods.cumulative_days_of_simulation,
                         (1, ))
        
        
    def test_days_of_month(self):
        ""
        self.assertEqual(self.daily_periods.days_of_month,
                         (21, ))
        
        
    def test_dst_indicators(self):
        ""
        self.assertEqual(self.daily_periods.dst_indicators,
                         (0, ))
        
        
    def test_get_end_times(self):
        ""
        self.assertEqual(self.daily_periods.get_end_times(),
                         (datetime.datetime(2001, 12, 22, 0, 0, tzinfo=datetime.timezone.utc), ))
        
        
    def test_get_interval(self):
        ""
        self.assertEqual(self.daily_periods.get_interval(),
                         datetime.timedelta(days=1))
        
        
    def test_get_periods(self):
        ""
        self.assertEqual(str(self.daily_periods.get_periods()),
                         "[Period('2001-12-21 00:00:00', '86400S')]")
        
        
    def test_get_start_times(self):
        ""
        self.assertEqual(self.daily_periods.get_start_times(),
                         (datetime.datetime(2001, 12, 21, 0, 0, tzinfo=datetime.timezone.utc), ))
    
        
    def test_months(self):
        ""
        self.assertEqual(self.daily_periods.months,
                         (12,))
    
        
    def test_summary(self):
        ""
        self.assertEqual(self.daily_periods.summary(),
                         'Starts at 2001-12-21T00:00:00+00:00, 1 periods @ 1 day intervals')
        
        
        
class Test_EPEsoDailyVariable(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.env=eso.get_environments()[0]
        self.daily_variable=self.env.get_daily_variables()[0]
        
    
    def test___init__(self):
        ""
        self.assertEqual(str(self.daily_variable),
                         'EPEsoDailyVariable(report_code=51)')
        self.assertEqual(self.daily_variable._epesose,
                         self.env)
        self.assertEqual(self.daily_variable._report_code,
                         51)
            
        
    def test_get_dataframe(self):
        ""
        df=self.daily_variable.get_dataframe()
        #print(df)
        
        
    def test_get_max_times(self):
        ""
        self.assertEqual(self.daily_variable.get_max_times(),
                         (datetime.datetime(2001, 12, 21, 0, 14, 
                                            tzinfo=datetime.timezone.utc),))
        
        
    def test_get_min_times(self):
        ""
        self.assertEqual(self.daily_variable.get_min_times(),
                         (datetime.datetime(2001, 12, 21, 23, 59, 
                                            tzinfo=datetime.timezone.utc),))
        
        
    def test_max_hours(self):
        ""
        self.assertEqual(self.daily_variable.max_hours,
                         (1,))
        
        
    def test_max_minutes(self):
        ""
        self.assertEqual(self.daily_variable.max_minutes,
                         (15,))
        
        
    def test_max_values(self):
        ""
        self.assertEqual(self.daily_variable.max_values,
                         (-18.1438609435393,))
        
        
    def test_min_hours(self):
        ""
        self.assertEqual(self.daily_variable.min_hours,
                         (24,))
        
        
    def test_min_minutes(self):
        ""
        self.assertEqual(self.daily_variable.min_minutes,
                         (60,))
        
        
    def test_min_values(self):
        ""
        self.assertEqual(self.daily_variable.min_values,
                         (-18.145500357130768,))
        
    
    def test_object_name(self):
        ""
        self.assertEqual(self.daily_variable.object_name,
                         'ZN001:WALL001')
        
        
    def test_plot(self):
        ""
        #v.plot()
        
        
    def test_quantity(self):
        ""
        self.assertEqual(self.daily_variable.quantity,
                         'Surface Inside Face Temperature')
        
     
    def test_report_code(self):
        ""
        self.assertEqual(self.daily_variable.report_code,
                         51)

        
    def test_summary(self):
        ""
        self.assertEqual(self.daily_variable.summary(),
                         '51 - ZN001:WALL001 - Surface Inside Face Temperature (C)')
        
        
    def test_unit(self):
        ""
        self.assertEqual(self.daily_variable.unit,
                         'C')
                
        
    def test_values(self):
        ""
        self.assertEqual(self.daily_variable.values,
                         (-18.14473130427405,))   
        
        
        
class Test_EPEsoIntervalPeriods(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.env=eso.get_environments()[0]
        self.interval_periods=self.env.get_interval_periods()
        
    
    def test___init__(self):
        ""
        self.assertIsInstance(self.interval_periods._data,
                              tuple)
        self.assertEqual(self.interval_periods._epesose,
                         self.env)
        
    
    def test_day_types(self):
        ""
        self.assertEqual(self.interval_periods.day_types,
                         ('WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay', 'WinterDesignDay'))
     
    
    def test_days_of_month(self):
        ""
        self.assertEqual(self.interval_periods.days_of_month,
                         (21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21))
     
    
    def test_days_of_simulation(self):
        ""
        self.assertEqual(self.interval_periods.days_of_simulation,
                         (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1))
        
        
    def test_dst_indicators(self):
        ""
        self.assertEqual(self.interval_periods.dst_indicators,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
     
        
    def test_end_minutes(self):
        ""
        self.assertEqual(self.interval_periods.end_minutes,
                         (60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60))
        
    
    def test_get_end_times(self):
        ""
        self.assertEqual(self.interval_periods.get_end_times(),
                         (datetime.datetime(2001, 12, 21, 1, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 2, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 3, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 4, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 5, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 6, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 7, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 8, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 9, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 10, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 11, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 12, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 13, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 14, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 15, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 16, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 17, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 18, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 19, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 20, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 21, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 22, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 23, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 22, 0, 0, tzinfo=datetime.timezone.utc)))
        
        
    def test_get_interval(self):
        ""
        self.assertEqual(self.interval_periods.get_interval(),
                         datetime.timedelta(minutes=60))
        
        
    def test_get_periods(self):
        ""
        self.assertEqual(str(self.interval_periods.get_periods()),
                         "[Period('2001-12-21 00:00:00', '3600S'), Period('2001-12-21 01:00:00', '3600S'), Period('2001-12-21 02:00:00', '3600S'), Period('2001-12-21 03:00:00', '3600S'), Period('2001-12-21 04:00:00', '3600S'), Period('2001-12-21 05:00:00', '3600S'), Period('2001-12-21 06:00:00', '3600S'), Period('2001-12-21 07:00:00', '3600S'), Period('2001-12-21 08:00:00', '3600S'), Period('2001-12-21 09:00:00', '3600S'), Period('2001-12-21 10:00:00', '3600S'), Period('2001-12-21 11:00:00', '3600S'), Period('2001-12-21 12:00:00', '3600S'), Period('2001-12-21 13:00:00', '3600S'), Period('2001-12-21 14:00:00', '3600S'), Period('2001-12-21 15:00:00', '3600S'), Period('2001-12-21 16:00:00', '3600S'), Period('2001-12-21 17:00:00', '3600S'), Period('2001-12-21 18:00:00', '3600S'), Period('2001-12-21 19:00:00', '3600S'), Period('2001-12-21 20:00:00', '3600S'), Period('2001-12-21 21:00:00', '3600S'), Period('2001-12-21 22:00:00', '3600S'), Period('2001-12-21 23:00:00', '3600S')]")
        
        
    def test_get_start_times(self):
        ""
        self.assertEqual(self.interval_periods.get_start_times(),
                         (datetime.datetime(2001, 12, 21, 0, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 1, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 2, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 3, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 4, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 5, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 6, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 7, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 8, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 9, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 10, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 11, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 12, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 13, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 14, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 15, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 16, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 17, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 18, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 19, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 20, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 21, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 22, 0, tzinfo=datetime.timezone.utc), datetime.datetime(2001, 12, 21, 23, 0, tzinfo=datetime.timezone.utc)))
        
        
    def test_hours(self):
        ""
        self.assertEqual(self.interval_periods.hours,
                         (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24))
          
        
    def test_months(self):
        ""
        self.assertEqual(self.interval_periods.months,
                         (12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12))
      
        
    def test_start_minutes(self):
        ""
        self.assertEqual(self.interval_periods.start_minutes,
                         (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        
        
    def test_summary(self):
        ""
        self.assertEqual(self.interval_periods.summary(),
                         'Starts at 2001-12-21T00:00:00+00:00, 24 periods @ 60 minute intervals')
        

    
class Test_EPEsoIntervalVariable(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.env=eso.get_environments()[0]
        self.interval_variable=self.env.get_interval_variables()[0]
        
    
    def test___init__(self):
        ""
        self.assertEqual(str(self.interval_variable),
                         'EPEsoIntervalVariable(report_code=7)')
        self.assertEqual(self.interval_variable._epesose,
                         self.env)
        self.assertEqual(self.interval_variable._report_code,
                         7)
            
        
    def test_get_dataframe(self):
        ""
        df=self.interval_variable.get_dataframe()
        #print(df)
        
        
    def test_get_series(self):
        s=self.interval_variable.get_series()
        #print(s)
        
    
    def test_object_name(self):
        ""
        self.assertEqual(self.interval_variable.object_name,
                         'Environment')
        
        
    def test_plot(self):
        ""
        #for v in vs:
        #    v.plot()
        
        
    def test_quantity(self):
        ""
        self.assertEqual(self.interval_variable.quantity,
                         'Site Outdoor Air Drybulb Temperature')
        
        
    def test_report_code(self):
        ""
        self.assertEqual(self.interval_variable.report_code,
                         7)
        
        
    def test_summary(self):
        ""
        self.assertEqual(self.interval_variable.summary(),
                         '7 - Environment - Site Outdoor Air Drybulb Temperature (C)')
        
        
    def test_unit(self):
        ""
        self.assertEqual(self.interval_variable.unit,
                         'C')
                
        
    def test_values(self):
        ""
        self.assertEqual(len(self.interval_variable.values),
                         24)
        self.assertEqual(str(self.interval_variable.values[0]),
                         '-15.5')
        
        
        
class Test_EPEsoMonthlyPeriods(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.env=eso.get_environments()[0]
        self.monthly_periods=self.env.get_monthly_periods()
        
   
    def test___init__(self):
        ""
        self.assertIsInstance(self.monthly_periods._data,
                              tuple)
        self.assertEqual(self.monthly_periods._epesose,
                         self.env)
        
    
    def test_cumulative_days_of_simulation(self):
        ""
        self.assertEqual(self.monthly_periods.cumulative_days_of_simulation,
                         (1, ))
        
        
    def test_get_end_times(self):
        ""
        self.assertEqual(self.monthly_periods.get_end_times(),
                         (datetime.datetime(2002, 1, 1, 0, 0, 
                                            tzinfo=datetime.timezone.utc), ))
        
        
    def test_get_periods(self):
        ""
        self.assertEqual(str(self.monthly_periods.get_periods()),
                         "[Period('2001-12', 'M')]")
        
        
    def test_get_start_times(self):
        ""
        self.assertEqual(self.monthly_periods.get_start_times(),
                         (datetime.datetime(2001, 12, 1, 0, 0, tzinfo=datetime.timezone.utc), ))
    
        
    def test_months(self):
        ""
        self.assertEqual(self.monthly_periods.months,
                         (12,))
    
                
    def test_summary(self):
        ""
        self.assertEqual(self.monthly_periods.summary(),
                         'Starts at 2001-12-01T00:00:00+00:00, 1 periods @ 1 month intervals')
        
        
        
class Test_EPEsoMonthlyVariable(unittest.TestCase):
    ""
    
    def setUp(self):
        ""
        self.env=eso.get_environments()[0]
        self.monthly_variable=self.env.get_monthly_variables()[0]
        
    
    def test___init__(self):
        ""
        self.assertEqual(str(self.monthly_variable),
                         'EPEsoMonthlyVariable(report_code=48)')
        self.assertEqual(self.monthly_variable._epesose,
                         self.env)
        self.assertEqual(self.monthly_variable._report_code,
                         48)
            
        
    def test_get_dataframe(self):
        ""
        df=self.monthly_variable.get_dataframe()
        #print(df)
        
        
    def test_get_max_times(self):
        ""
        self.assertEqual(self.monthly_variable.get_max_times(),
                         (datetime.datetime(2001, 12, 21, 1, 15, 
                                            tzinfo=datetime.timezone.utc),))
        
        
    def test_get_min_times(self):
        ""
        self.assertEqual(self.monthly_variable.get_min_times(),
                         (datetime.datetime(2001, 12, 21, 1, 15, 
                                            tzinfo=datetime.timezone.utc),))
        
        
    def test_max_hours(self):
        ""
        self.assertEqual(self.monthly_variable.max_hours,
                         (1,))
        
        
    def test_max_minutes(self):
        ""
        self.assertEqual(self.monthly_variable.max_minutes,
                         (15,))
        
        
    def test_max_values(self):
        ""
        self.assertEqual(self.monthly_variable.max_values,
                         (316800.0,))
        
        
    def test_min_hours(self):
        ""
        self.assertEqual(self.monthly_variable.min_hours,
                         (1,))
        
        
    def test_min_minutes(self):
        ""
        self.assertEqual(self.monthly_variable.min_minutes,
                         (15,))
        
        
    def test_min_values(self):
        ""
        self.assertEqual(self.monthly_variable.min_values,
                         (316800.0,))
        
    
    def test_object_name(self):
        ""
        self.assertEqual(self.monthly_variable.object_name,
                         'TEST 352A')
        
        
    def test_plot(self):
        ""
        #v.plot()
        
        
    def test_quantity(self):
        ""
        self.assertEqual(self.monthly_variable.quantity,
                         'Other Equipment Total Heating Energy')
        
     
    def test_report_code(self):
        ""
        self.assertEqual(self.monthly_variable.report_code,
                         48)

        
    def test_summary(self):
        ""
        self.assertEqual(self.monthly_variable.summary(),
                         '48 - TEST 352A - Other Equipment Total Heating Energy (J)')
        
        
    def test_unit(self):
        ""
        self.assertEqual(self.monthly_variable.unit,
                         'J')
                
        
    def test_values(self):
        ""
        self.assertEqual(self.monthly_variable.values,
                         (30412800.0,))   

        
        
    
if __name__=='__main__':
    
    unittest.main()
    
    