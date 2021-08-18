# -*- coding: utf-8 -*-

import unittest
from pprint import pprint
import jsonschema

from eprun import EPSchema


class Test_EPSchemaProperty(unittest.TestCase):
    ""
    
    def test___init__(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        self.assertEqual(list(p.keys()),
                         ['type', 'default'])
        
        
    def test_dict_(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        self.assertEqual(p.dict_,
                         {'type': 'string', 'default': '9.4'})
        
        
    def test_idd_legacy_field_name(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        self.assertEqual(p.idd_legacy_field_name,
                         'Version Identifier')
    
    
    def test_name(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        self.assertEqual(p.name,
                         'version_identifier')
        
        
    def test_validate_value(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        p.validate_value('my_string')
    
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          p.validate_value,
                          2)
    
    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchemaProperty())