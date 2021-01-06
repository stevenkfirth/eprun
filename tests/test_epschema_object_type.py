# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

import jsonschema
from eprun import EPSchema


class Test_EPSchemaObjectType(unittest.TestCase):
    ""
    
    
        
    def test_additional_properties(self):
        ""
        so=s.get_object_type('ZoneCapacitanceMultiplier:ResearchSpecial')
        self.assertEqual(so.additional_properties,
                         False)
        
        
    def test_dict_(self):
        ""
        so=s.get_object_type('Version')
        self.assertIsInstance(so.dict_,
                              dict)
        
        
    def test_extensible_size(self):
        ""
        so=s.get_object_type('ShadowCalculation')
        self.assertEqual(so.extensible_size,
                         1.0)
        
        
    def test_legacy_idd_fields(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.legacy_idd_fields,
                         ['version_identifier'])
        
        
    def test_format(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.format_,
                         'singleLine')
        
        
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
        
        
    def test_max_properties(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.max_properties,
                         1)
        
    
    def test_memo(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.memo,
                         'Specifies the EnergyPlus version of the IDF file.')
        
        
    def test_min_properties(self):
        ""
        so=s.get_object_type('Building')
        self.assertEqual(so.min_properties,
                         1)
        
        
    def test_name(self):
        ""
        so=s.get_object_type('Version')
        self.assertEqual(so.name,
                         'Version')
        
        
    def test_name_property(self):
        ""
        so=s.get_object_type('Building')
        self.assertEqual(so.name_property,
                         {'type': 'string', 
                          'retaincase': True, 
                          'default': 'NONE'})
        
        
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
        
        building={'my_building':{}}
        so.validate_object(building)
        
        
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchemaObjectType())