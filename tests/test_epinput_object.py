# -*- coding: utf-8 -*-

import unittest
from pprint import pprint
from jsonschema.exceptions import ValidationError

from eprun import EPInput, EPSchema
from eprun.epinput_object import EPInputObject


class Test_EPInputObject(unittest.TestCase):
    
    def test___init__(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertIsInstance(o,
                              EPInputObject)
        
        
    def test___getattr__(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(o.north_axis,
                          0)
        
        self.assertEqual(j['Building']['Simple One Zone (Wireframe DXF)'].north_axis,
                          0)
        
        
    def test___setattr__(self):
        ""
        j1=EPInput(fp='files/1ZoneUncontrolled.epJSON',
                   schema=s)
        o=j1.get_object('Simple One Zone (Wireframe DXF)')
        
        o.north_axis=180
        self.assertEqual(o.north_axis,
                         180)
        
        
    def test___getitem__(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(o['north_axis'],
                          0)
        
        
    def test___setitem__(self):
        ""
        j1=EPInput(fp='files/1ZoneUncontrolled.epJSON',
                   schema=s)
        o=j1.get_object('Simple One Zone (Wireframe DXF)')
        
        o['north_axis']=180
        self.assertEqual(o['north_axis'],
                          180)
        
        
    def test___repr__(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o),
                          'EPInputObject(name="Simple One Zone (Wireframe DXF)")')
        
        
    def test__get_schema_property(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o._get_schema_property(name='north_axis')),
                          'EPSchemaProperty(name="north_axis")')
        
        
    def test__schema_object_type(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o._schema_object_type),
                         'EPSchemaObjectType(name="Building")')
        
        
    def test__schema(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o._schema),
                         'EPSchema(version="9.4.0")')
        
        
    def test__validate_property_name(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertRaises(ValueError,
                          o._validate_property_name,
                          'ABC')
        
        
    def test__validate_property_value(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertRaises(ValueError,
                          o._validate_property_value,
                          'north_axis','ABC')
        
        
    def test_get_property_value(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        v=o.get_property_value('north_axis')
        self.assertEqual(v,
                          0)
        
        
    def test_get_property_values(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
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
        o=j.get_object('Simple One Zone (Wireframe DXF)')
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
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(o.name,
                          'Simple One Zone (Wireframe DXF)')
    
    
    def test_object_name(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(o.object_type,
                         'Building')
    
    
    def test_set_property_values(self):
        ""
        j1=EPInput(fp='files/1ZoneUncontrolled.epJSON',
                   schema=s)
        o=j1.get_object('Simple One Zone (Wireframe DXF)')
        o.set_property_value('north_axis',180)
        self.assertEqual(o.north_axis,
                          180)
        
        o.set_property_value('north_axis',180)
        
        # type validation error - string - passes
        o.set_property_value('terrain','City')
        
        # type validation error - string - fails
        self.assertRaises(ValueError,
                          o.set_property_value,
                          'terrain',0)
        # ValueError: 0 is not of type 'string' in property 'terrain'

        # type validation error - number - passes
        o.set_property_value('north_axis',180)
        
        # type validation error - number - fails
        self.assertRaises(ValueError,
                          o.set_property_value,
                          'north_axis','City')

        # type validation error - array - passes
        o1=j1['BuildingSurface:Detailed']['Zn001:Flr001']
        o1.set_property_value('vertices',
                              [{"vertex_x_coordinate": 15.24,
                                "vertex_y_coordinate": 0.0,
                                "vertex_z_coordinate": 0.0}],
                              )
        
        # type validation error - array - fails
        self.assertRaises(ValueError,
                          o1.set_property_value,
                          'vertices',0)
        
        # enum validation error - string - passes
        o.set_property_value('terrain','City')
        
        # enum validation error - string - fails
        self.assertRaises(ValueError,
                          o.set_property_value,
                          'terrain','MyMegaCity')
        
        # test with schema set on EPInput object.
        j2=EPInput(fp='files/1ZoneUncontrolled.epJSON',
                   schema=s)
        o=j2.get_object('Simple One Zone (Wireframe DXF)')
        o.set_property_value('north_axis',180)
        self.assertRaises(ValueError,
                          o.set_property_value,
                          'north_axis','City')
        
    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    j=EPInput(fp='files/1ZoneUncontrolled.epJSON',
              schema=s)
    unittest.main(Test_EPInputObject())