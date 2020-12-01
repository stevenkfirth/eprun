# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPSchema


class Test_EPSchemaName(unittest.TestCase):
   
   def test_1(self):
        "Determines the possible properties of the 'name' property"
        result={}
        for epso in s.get_objects():
            d=epso._dict
            if 'name' in d:
                for k,v in d['name'].items():
                    if not k in result:
                        result[k]=epso.name
        #pprint(result)
        {'data_type': 'WeatherProperty:SkyTemperature',
         'default': 'Building',
         'is_required': 'ZoneCapacitanceMultiplier:ResearchSpecial',
         'note': 'SizingPeriod:WeatherFileDays',
         'object_list': 'WeatherProperty:SkyTemperature',
         'reference': 'SizingPeriod:DesignDay',
         'reference-class-name': 'SwimmingPool:Indoor',
         'retaincase': 'Building',
         'type': 'Building'} 
   
   def test_(self):
       ""
    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchemaName())