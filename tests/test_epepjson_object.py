# -*- coding: utf-8 -*-

import unittest
from pprint import pprint
from jsonschema.exceptions import ValidationError

from eprun import EPEpJSON, EPSchema
from eprun.epepjson_object import EPEpJSONObject


class Test_EPEpJSONObject(unittest.TestCase):
    
    def test___init__(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertIsInstance(o,
                              EPEpJSONObject)
        
        
        
    def test___getattr__(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot['Simple One Zone (Wireframe DXF)']
        self.assertEqual(o.north_axis,
                          0)
        
        self.assertEqual(j['Building']['Simple One Zone (Wireframe DXF)'].north_axis,
                          0)
        
        self.assertEqual(j['Building'].get_objects()[0].north_axis,
                          0)
        
        
    # def test___setattr__(self):
    #     ""
    #     j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
    #     ot=j.get_object_type('Building')
    #     o=ot['Simple One Zone (Wireframe DXF)']
        
    #     #o.north_axis=180
    #     #self.assertEqual(o.north_axis,
    #     #                 180)
        
        
    def test___getitem__(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot['Simple One Zone (Wireframe DXF)']
        self.assertEqual(o['north_axis'],
                          0)
        
        
    def test___setitem__(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot['Simple One Zone (Wireframe DXF)']
        o['north_axis']=180
        self.assertEqual(o['north_axis'],
                          180)
        
        
    def test___repr__(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o),
                          'EPEpJSONObject(name="Simple One Zone (Wireframe DXF)")')
        
        
    def test__get_schema_property(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o._get_schema_property(name='north_axis',
                                                    schema=s)),
                          'EPSchemaProperty(name="north_axis")')
        
        
    def test__validate_property_name(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertRaises(ValueError,
                          o._validate_property_name,
                          'ABC',s)
        
        
    def test_get_property_value(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        v=o.get_property_value('north_axis')
        self.assertEqual(v,
                          0)
        
        
    def test_get_property_values(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
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
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
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
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(o.name,
                          'Simple One Zone (Wireframe DXF)')
    
    
    def test_set_property_values(self):
        ""
        j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        o.set_property_value('north_axis',180)
        self.assertEqual(o.north_axis,
                          180)
        
        o.set_property_value('north_axis',180,schema=s)
        
        # type validation error - string - passes
        o.set_property_value('terrain','City',schema=s)
        
        # type validation error - string - fails
        self.assertRaises(ValueError,
                          o.set_property_value,
                          'terrain',0,schema=s)

        # type validation error - number - passes
        o.set_property_value('north_axis',180,schema=s)
        
        # type validation error - number - fails
        self.assertRaises(ValueError,
                          o.set_property_value,
                          'north_axis','City',schema=s)

        # type validation error - array - passes
        o1=j['BuildingSurface:Detailed']['Zn001:Flr001']
        o1.set_property_value('vertices',
                              [{"vertex_x_coordinate": 15.24,
                                "vertex_y_coordinate": 0.0,
                                "vertex_z_coordinate": 0.0}],
                              schema=s)
        
        # type validation error - array - fails
        self.assertRaises(ValueError,
                          o1.set_property_value,
                          'vertices',0,schema=s)
        
        # enum validation error - string - passes
        o.set_property_value('terrain','City',schema=s)
        
        # enum validation error - string - fails
        self.assertRaises(ValueError,
                          o.set_property_value,
                          'terrain','MyMegaCity',schema=s)
        
        # test with schema set on EPEpJSON object.
        j1=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON',schema=s)
        ot=j1.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        o.set_property_value('north_axis',180)
        self.assertRaises(ValueError,
                          o.set_property_value,
                          'north_axis','City')
        
    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPEpJSONObject())