# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPSchema, EPInput


class Test_EPSchema(unittest.TestCase):
   
    def test___init__(self):
        ""
        #print(s)
        self.assertEqual(str(s),
                         'EPSchema(version="9.4.0")')
        
        
    def test__validator(self):
        #print(s._validator)
        self.assertEqual(str(type(s._validator)),
                         "<class 'jsonschema.validators.create.<locals>.Validator'>")
        
        
    def test_build(self):
        ""
        #print(s.build)
        self.assertEqual(s.build,
                         '998c4b761e')
        
        
    def test_dict_(self):
        ""
        self.assertIsInstance(s.dict_,
                              dict)
        
        
    def test_get_object_type(self):
        ""
        o=s.get_object_type('Version')
        #print(o)
        self.assertEqual(str(o),
                         'EPSchemaObjectType(name="Version")')
        
        
    def test_get_object_types(self):
        ""
        objs=s.get_object_types()
        #print(objs)
        self.assertEqual(len(objs),
                         815)
        self.assertEqual(str(objs[0]),
                         'EPSchemaObjectType(name="Version")')

    
    def test_object_type_names(self):
        ""
        names=s.object_type_names
        #print(len(names))
        self.assertEqual(len(names),
                         815)
        self.assertEqual(names[0],
                         'Version')
        
        
    def test_required(self):
        ""
        r=s.required
        self.assertEqual(r,
                         ['Building', 'GlobalGeometryRules'])
        
        
    def test_validate_epjson(self):
        ""
        j=EPInput(fp='files/1ZoneUncontrolled.epJSON')
        s.validate_epjson(j._dict)
        
        
    def test_validate_object_type_name(self):
        ""
        s.validate_object_type_name('Building')
        
        self.assertRaises(IndexError,
                          s.validate_object_type_name,
                          'ABC')
        
        
        
    def test_version(self):
        ""
        v=s.version
        self.assertEqual(v,
                         '9.4.0')
        


if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPSchema())
    
    