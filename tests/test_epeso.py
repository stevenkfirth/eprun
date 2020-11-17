# -*- coding: utf-8 -*-

import unittest
from eprun import EPEso
from pprint import pprint

class Test_EPEso(unittest.TestCase):
   
    
    def test_EPEso(self):
        ""
        e=EPEso(fp=r'files\eplusout.eso')
        
        #print(e._data_dictionary)
        pprint(e._data[0]['frequency'][2])
        
        envs=e.get_environments()
        
        pprint(envs)
        
        env1=envs[0]
        
        print(env1.elevation)
        
        print(env1.get_interval_variables())
        print(env1.get_daily_variables())
        print(env1.get_monthly_variables())
        print(env1.get_run_period_variables())
        print(env1.get_annual_variables())
        
        print(env1.get_interval_variables()[0].values)
        print(env1.get_interval_variables()[0].location)
        print(env1.get_interval_variables()[0].quantity)
        print(env1.get_interval_variables()[0].units)
        
        #pprint(env1.get_interval_periods().get_start_times())
        #print(env1.time_zone)
    
if __name__=='__main__':
    
    unittest.main(Test_EPEso())
    
    