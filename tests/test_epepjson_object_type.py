# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPEpJSON, EPSchema
from eprun.epepjson_object_type import EPEpJSONObjectType


class Test_EPEpJSONObjectType(unittest.TestCase):
   
    def test___init__(self):
        ""
        ot=j.get_object_type('Building')
        self.assertIsInstance(ot,
                              EPEpJSONObjectType)
        
        
    def test___getitem__(self):
        ""
        ot=j.get_object_type('Building')
        o=ot['Simple One Zone (Wireframe DXF)']
        self.assertEqual(str(o),
                         'EPEpJSONObject(name="Simple One Zone (Wireframe DXF)")')
        
        
    def test___repr__(self):
        ""
        ot=j.get_object_type('Building')
        self.assertEqual(str(ot),
                         'EPEpJSONObjectType(name="Building")')
        
        
    def test__get_schema_object(self):
        ""
        ot=j.get_object_type('Building')
        self.assertEqual(str(ot._get_schema_object(s)),
                         'EPSchemaObject(name="Building")')
        
        
        
    def test_get_object(self):
        ""
        ot=j.get_object_type('Building')
        o=ot.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o),
                         'EPEpJSONObject(name="Simple One Zone (Wireframe DXF)")')
        
        
    def test_get_objects(self):
        ""
        ot=j.get_object_type('Building')
        os=ot.get_objects()
        self.assertEqual(len(os),
                         1)
        self.assertEqual(str(os[0]),
                         'EPEpJSONObject(name="Simple One Zone (Wireframe DXF)")')
        
        
    def test_object_names(self):
        ""
        ot=j.get_object_type('Building')
        self.assertEqual(ot.object_names,
                         ['Simple One Zone (Wireframe DXF)'])
        
        
    def test_name(self):
        ""
        ot=j.get_object_type('Building')
        self.assertEqual(ot.name,
                         'Building')
    
    
if __name__=='__main__':
    
    j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPEpJSONObjectType())