# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPEpJSON
from eprun.epepjson_object import EPEpJSONObject


class Test_EPEpJSONObject(unittest.TestCase):
   
    def test___init__(self):
        ""
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertIsInstance(o,
                              EPEpJSONObject)
        
        
    def test___getattr__(self):
        ""
        ot=j.get_object_type('Building')
        o=ot['Simple One Zone (Wireframe DXF)']
        self.assertEqual(o.north_axis,
                         0)
        
        self.assertEqual(j['Building']['Simple One Zone (Wireframe DXF)'].north_axis,
                         0)
        
        self.assertEqual(j['Building'].get_objects()[0].north_axis,
                         0)
        
        
    def test___getitem__(self):
        ""
        ot=j.get_object_type('Building')
        o=ot['Simple One Zone (Wireframe DXF)']
        self.assertEqual(o['north_axis'],
                         0)
        
        
    def test___repr__(self):
        ""
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o),
                         'EPEpJSONObject(name="Simple One Zone (Wireframe DXF)")')
        
        
    def test_get_property_value(self):
        ""
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        v=o.get_property_value('north_axis')
        self.assertEqual(v,
                         0)
        
        
    def test_get_property_values(self):
        ""
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(o.property_values,
                         {'loads_convergence_tolerance_value': 0.04, 
                          'maximum_number_of_warmup_days': 30, 
                          'minimum_number_of_warmup_days': 6, 
                          'north_axis': 0, 
                          'solar_distribution': 'MinimalShadowing', 
                          'temperature_convergence_tolerance_value': 0.004, 
                          'terrain': 'Suburbs'})
        
        
    def test_property_names(self):
        ""
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(o.property_names,
                         ['loads_convergence_tolerance_value',
                          'maximum_number_of_warmup_days',
                          'minimum_number_of_warmup_days',
                          'north_axis',
                          'solar_distribution',
                          'temperature_convergence_tolerance_value',
                          'terrain'])
        
        
    def test_name(self):
        ""
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(o.name,
                         'Simple One Zone (Wireframe DXF)')
    
    
if __name__=='__main__':
    
    j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
    unittest.main(Test_EPEpJSONObject())