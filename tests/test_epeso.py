# -*- coding: utf-8 -*-

import unittest
import eprun
from eprun import EPEso
from pprint import pprint
import pandas as pd

class Test_EPEso(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        self.assertIsInstance(e,
                              EPEso)
        
        
    def test_get_environment(self):
        ""
        se=e.get_environment('RUN PERIOD 1')
        self.assertEqual(str(se),
                         'EPEsoSimuationEnvironment(environment_title="RUN PERIOD 1")')
        
    def test_get_environments(self):
        ""
        envs=e.get_environments()
        #print(str(envs))
        self.assertIsInstance(envs,
                              list)
        self.assertEqual(len(envs),
                         3)
        self.assertIsInstance(envs[0],
                              eprun.epeso_simulation_environment.EPEsoSimulationEnvironment)
        
        
    def test_programme_version_statement(self):
        ""
        self.assertEqual(e.programme_version_statement,
                         {'programme': 'EnergyPlus', 
                          'version': 'Version 9.4.0-998c4b761e', 
                          'timestamp': 'YMD=2020.11.13 06:25'})
        
        
    def test_standard_items_dictionary(self):
        ""
        self.assertEqual(e.standard_items_dictionary,
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
        self.assertEqual(list(e.variable_dictionary.keys()),
                         [7, 8, 9, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 
                          60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77])
        self.assertEqual(e.variable_dictionary[7],
                         {'comment': 'Hourly',
                          'number_of_values': 1,
                          'object_name': 'Environment',
                          'quantity': 'Site Outdoor Air Drybulb Temperature',
                          'unit': 'C'}
                         )
        
    
if __name__=='__main__':
    
    e=EPEso(fp=r'files\eplusout.eso')
    unittest.main(Test_EPEso())
    
    