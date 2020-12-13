# -*- coding: utf-8 -*-

import unittest
from eprun import EPEso
from pprint import pprint
import pandas as pd

class Test_EPEso(unittest.TestCase):
   
    
    def test_EPEso(self):
        ""
        #e=EPEso(fp=r'files\eplusout.eso')
        
        #pprint(e.programme_version_statement)
        
        #pprint(e.standard_items_dictionary[1])
        
        #pprint(e.variable_dictionary[7])
        
        #pprint(e.get_environments())
        
        
    def test_EPEsoSimulationEnviroment(self):
        ""
        epeso=EPEso(fp=r'files\eplusout.eso')
        se=epeso.get_environments()[0]
        
        #print(se.environment_title)
        #print(se.monthly_data)
        #pprint(se.get_monthly_variables())
        
        #pprint(se.get_monthly_data())
        
        index,freq,data,columns,column_level_names=se.get_interval_dataframe_inputs()
        
        df=pd.DataFrame(index=[pd.Period(dt,freq) for dt in index],
                        data=data,
                        columns=pd.MultiIndex.from_tuples(columns, 
                                                          names=column_level_names))
        print(df)
        df.to_csv('test.csv')
        
        print(se.get_variables())
        
        
    def test_EPEsoMonthlyPeriods(self):
        ""
        epeso=EPEso(fp=r'files\eplusout.eso')
        se=epeso.get_environments()[0]
        mp=se.get_monthly_periods()
        
        # print(mp)
        # print(mp._data)
        # print(mp.cumulative_days_of_simulation)
        # print(mp.month)
        # print(mp.get_start_times())
        # print(mp.get_end_times())
       
    
    def test_EPESOMonthlyVariable(self):
        ""
        epeso=EPEso(fp=r'files\eplusout.eso')
        se=epeso.get_environments()[0]
        mv=se.get_monthly_variables()[0]
        
        # print(mv)
        # print(mv.object_name)
        # print(mv.quantity)
        # print(mv.unit)
        # print(mv.values)
        # print(mv.min_values)
        # print(mv.min_days)
        # print(mv.min_hours)
        # print(mv.min_minutes)
        # print(mv.get_min_times())
        # print(mv.max_values)
        # print(mv.max_days)
        # print(mv.max_hours)
        # print(mv.max_minutes)
        # print(mv.get_max_times())
        
    
if __name__=='__main__':
    
    unittest.main(Test_EPEso())
    
    