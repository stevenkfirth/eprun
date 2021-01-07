# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

import jsonschema
from eprun import EPSchema


class Test_EPSchemaObjectType(unittest.TestCase):
    ""

    def test___init__(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(list(so.keys()),
                         ['patternProperties', 'legacy_idd', 'type', 'maxProperties', 'memo', 'format'])

        
    def test_dict_(self):
        ""
        so=s.get_object_type('Version')
        self.assertIsInstance(so.dict_,
                              dict)
        
        
    def test_legacy_idd_fields(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.legacy_idd_fields,
                         ['version_identifier'])
        
        
    def test_get_properties(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(str(so.get_properties()),
                         '[EPSchemaProperty(name="version_identifier")]')
        
    
    def test_get_property(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(str(so.get_property('version_identifier')),
                         'EPSchemaProperty(name="version_identifier")')
        
        
    def test_name(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.name,
                         'Version')
    
        
    def test_pattern_properties_regexes(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.pattern_properties_regexes,
                         ['.*'])
        
        
    def test_property_names(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.property_names,
                         ['version_identifier'])
        
        
    def test_validate_property_name(self):
        ""
        so=s.get_object_type('Version')
        so.validate_property_name('version_identifier')
        
        self.assertRaises(IndexError,
                          so.validate_property_name,
                          'my_property')
        
    
    def test_validate_object(self):
        ""
        so=s.get_object_type('Building')
        building={
                    "Simple One Zone (Wireframe DXF)": {
                        "loads_convergence_tolerance_value": 0.04,
                        "maximum_number_of_warmup_days": 30,
                        "minimum_number_of_warmup_days": 6,
                        "north_axis": 0,
                        "solar_distribution": "MinimalShadowing",
                        "temperature_convergence_tolerance_value": 0.004,
                        "terrain": "Suburbs"
                    }
                }
        so.validate_object(building)
        
        building={}
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          so.validate_object,
                          building)
        # jsonschema.exceptions.ValidationError: {} does not have enough properties
    
        building='my_building'
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          so.validate_object,
                          building)
        # jsonschema.exceptions.ValidationError: 'my_building' is not of type 'object'
        
        # the schema does not have required properties
        building={'my_building':{}}
        so.validate_object(building)
        
        # the schema does not restrict additional properties
        building={'my_building':{'ABC':'abc'}}
        so.validate_object(building)
        
        
        
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchemaObjectType())