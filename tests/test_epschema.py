# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPSchema


class Test_EPSchema(unittest.TestCase):
   
    def test___init__(self):
        ""
        #print(s)
        self.assertEqual(str(s),
                         'EPSchema(version="9.4.0")')
        
        
    def test_build(self):
        ""
        #print(s.build)
        self.assertEqual(s.build,
                         '998c4b761e')
        
        
    def test_get_object(self):
        ""
        o=s.get_object('Version')
        #print(o)
        self.assertEqual(str(o),
                         'EPSchemaObject(name="Version")')
        
        
    def test_get_objects(self):
        ""
        objs=s.get_objects()
        #print(objs)
        self.assertEqual(len(objs),
                         815)
        self.assertEqual(str(objs[0]),
                         'EPSchemaObject(name="Version")')

    
    def test_object_names(self):
        ""
        names=s.object_names
        #print(len(names))
        self.assertEqual(len(names),
                         815)
        self.assertEqual(names[0],
                         'Version')
        
        
    def test_object_groups(self):
        ""
        groups=s.object_groups
        #print(groups)
        self.assertEqual(len(groups),
                         263)
        self.assertEqual(groups[0],
                         'WindowMaterial:Blind')
        
        
    def test_required(self):
        ""
        r=s.required
        self.assertEqual(r,
                         ['Building', 'GlobalGeometryRules'])
        
        
    def test_version(self):
        ""
        v=s.version
        self.assertEqual(v,
                         '9.4.0')
        

class Test_EPSchemaObject(unittest.TestCase):
    ""
    
    def test_0(self):
        "A routine to determine the available keys of the object dictionaries"
        result={}
        for k,v in s._dict['properties'].items():
            for k1 in v:
                if not k1 in result:
                    result[k1]=k
        #pprint(result)
        {'additionalProperties': 'ZoneCapacitanceMultiplier:ResearchSpecial',
         'extensible_size': 'ShadowCalculation',
         'format': 'Version',
         'legacy_idd': 'Version',
         'maxProperties': 'Version',
         'memo': 'Version',
         'minProperties': 'Building',
         'min_fields': 'SimulationControl',
         'name': 'Building',
         'patternProperties': 'Version',
         'type': 'Version'}
        
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
        
        
    def test_name(self):
        ""
        so=s.get_object('Version')
        self.assertEqual(so.name,
                         'Version')
        
        
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
    
    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchema())
    
    unittest.main(Test_EPSchemaObject())