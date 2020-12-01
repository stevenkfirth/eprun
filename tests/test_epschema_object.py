# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPSchema


class Test_EPSchemaObject(unittest.TestCase):
    ""
    
    def _test_0(self):
        "A routine to determine the available keys of the object dictionaries"
        
        # gives the keys and their value types
        result={}
        for object_name in s.object_names:
            object_dict=s._dict['properties'][object_name]
            for k,v in object_dict.items():
                result.setdefault(k,set())
                result[k].add(type(v))
        pprint(result)
        # {'additionalProperties': {<class 'bool'>},
        #  'extensible_size': {<class 'float'>},
        #  'format': {<class 'str'>},
        #  'legacy_idd': {<class 'dict'>},
        #  'maxProperties': {<class 'int'>},
        #  'memo': {<class 'str'>},
        #  'minProperties': {<class 'int'>},
        #  'min_fields': {<class 'float'>},
        #  'name': {<class 'dict'>},
        #  'patternProperties': {<class 'dict'>},
        #  'type': {<class 'str'>}}
        
        # gives the keys and the first object where they occur
        result={}
        for object_name in s.object_names:
            object_dict=s._dict['properties'][object_name]
            for k,v in object_dict.items():
                if not k in result:
                    result[k]=object_name
        pprint(result)
        # {'additionalProperties': 'ZoneCapacitanceMultiplier:ResearchSpecial',
        #  'extensible_size': 'ShadowCalculation',
        #  'format': 'Version',
        #  'legacy_idd': 'Version',
        #  'maxProperties': 'Version',
        #  'memo': 'Version',
        #  'minProperties': 'Building',
        #  'min_fields': 'SimulationControl',
        #  'name': 'Building',
        #  'patternProperties': 'Version',
        #  'type': 'Version'}
        
        
    def test_additional_properties(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.additional_properties,
                         None)
        
        so=s.get_object('ZoneCapacitanceMultiplier:ResearchSpecial')
        self.assertEqual(so.additional_properties,
                         False)
        
        
    def test_extensible_size(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.extensible_size,
                         None)
        
        so=s.get_object('ShadowCalculation')
        self.assertEqual(so.extensible_size,
                         1.0)
        
        
    def test_format(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.format_,
                         'singleLine')
        
        
    def test_get_properties(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(str(so.get_properties()),
                         '[EPSchemaProperty(name="version_identifier")]')
        
    
    def test_get_properties(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(str(so.get_property('version_identifier')),
                         'EPSchemaProperty(name="version_identifier")')
        
        
    def test_get_name(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.get_name(),
                         None)
        
        so=s.get_object('Building')
        self.assertEqual(str(so.get_name()),
                         'EPSchemaName(object_name="Building")')
        
        
    def test_max_properties(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.max_properties,
                         1)
        
    
    def test_memo(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.memo,
                         'Specifies the EnergyPlus version of the IDF file.')
        
        
    def test_min_properties(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.min_properties,
                         None)
        
        so=s.get_object('Building')
        self.assertEqual(so.min_properties,
                         1)
        
        
    def test_name(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.name,
                         'Version')
        
        
    def test_pattern_properties_regexes(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.pattern_properties_regexes,
                         ['.*'])
        
        
    def test_property_names(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.property_names,
                         ['version_identifier'])
        
        
        
        
    
    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchemaObject())