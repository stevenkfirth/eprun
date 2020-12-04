# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPSchema


class Test_EPSchemaName(unittest.TestCase):
   
   def test_1(self):
        "Determines the possible properties of the 'name' property"
        
        # gives the keys and their value types
        result={}
        for epso in s.get_objects():
            d=epso._dict
            if 'name' in d:
                for k,v in d['name'].items():
                    result.setdefault(k,set())
                    result[k].add(type(v))
        #pprint(result)
        # {'data_type': {<class 'str'>},
        #  'default': {<class 'str'>},
        #  'is_required': {<class 'bool'>},
        #  'note': {<class 'str'>},
        #  'object_list': {<class 'list'>},
        #  'reference': {<class 'list'>},
        #  'reference-class-name': {<class 'list'>},
        #  'retaincase': {<class 'bool'>},
        #  'type': {<class 'str'>}}
        
        # gives the keys and the first object where they occur
        result={}
        for epso in s.get_objects():
            d=epso._dict
            if 'name' in d:
                for k,v in d['name'].items():
                    if not k in result:
                        result[k]=epso.name
        #pprint(result)
        # {'data_type': 'WeatherProperty:SkyTemperature',
        #  'default': 'Building',
        #  'is_required': 'ZoneCapacitanceMultiplier:ResearchSpecial',
        #  'note': 'SizingPeriod:WeatherFileDays',
        #  'object_list': 'WeatherProperty:SkyTemperature',
        #  'reference': 'SizingPeriod:DesignDay',
        #  'reference-class-name': 'SwimmingPool:Indoor',
        #  'retaincase': 'Building',
        #  'type': 'Building'} 
   
    
   def test_data_type(self):
       ""
       so=s.get_object('WeatherProperty:SkyTemperature')
       n=so.get_name()
       self.assertEqual(n.data_type,
                        'object_list')
       
       
   def test_default(self):
       ""
       so=s.get_object('Building')
       n=so.get_name()
       self.assertEqual(n.default,
                        'NONE')
       
       
   def test_is_required(self):
       ""
       so=s.get_object('ZoneCapacitanceMultiplier:ResearchSpecial')
       n=so.get_name()
       self.assertEqual(n.is_required,
                        True)
       
       
   def test_note(self):
       ""
       so=s.get_object('SizingPeriod:WeatherFileDays')
       n=so.get_name()
       self.assertEqual(n.note,
                        'user supplied name for reporting')
       
       
   def test_object_list(self):
       ""
       so=s.get_object('WeatherProperty:SkyTemperature')
       n=so.get_name()
       self.assertEqual(n.object_list,
                        ['RunPeriodsAndDesignDays'])
       
       
   def test_reference(self):
       ""
       so=s.get_object('SizingPeriod:DesignDay')
       n=so.get_name()
       self.assertEqual(n.reference,
                        ['RunPeriodsAndDesignDays'])
       
       
   def test_reference_class_name(self):
       ""
       so=s.get_object('SwimmingPool:Indoor')
       n=so.get_name()
       self.assertEqual(n.reference_class_name,
                        ['validBranchEquipmentTypes'])
       
       
   def test_retaincase(self):
       ""
       so=s.get_object('Building')
       n=so.get_name()
       self.assertEqual(n.retaincase,
                        True)
       
   

    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchemaName())