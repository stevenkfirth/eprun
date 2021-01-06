# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

import jsonschema

from eprun import EPInput, EPSchema


class Test_EPInput(unittest.TestCase):
   
    def test___init__(self):
        ""
        j=EPInput(fp='files/1ZoneUncontrolled.epJSON')
        self.assertIsInstance(j,
                              EPInput)
        self.assertIsInstance(j._dict,
                              dict)
        self.assertEqual(len(j._dict),
                         27)
        
        s=EPSchema(fp='files/Energy+.schema.epJSON')
        i=EPInput(fp='files/1ZoneUncontrolled.idf',
                  schema=s)
        pprint(i._dict)  ### NEED TO CONVERT STRINGS TO NUMBERS ###
        
    
        
    def test___get_item__(self):
        ""
        ot=j['Building']
        self.assertEqual(str(ot),
                         'EPEpJSONObjectType(name="Building")')
        
        
    def test_get_object_type(self):
        ""
        # valid object type name
        ot=j.get_object_type('Building')
        self.assertEqual(str(ot),
                         'EPEpJSONObjectType(name="Building")')
        
         # invalid name, but no schema validation
        ot=j.get_object_type('MyObjectType')
        
        # invalid name, schema validation
        self.assertRaises(IndexError,
                          j.get_object_type,
                          'MyObjectType',schema=s)
        
        
    def test_get_object_types(self):
        ""
        ots=j.get_object_types()
        self.assertEqual(len(ots),
                         27)
        self.assertEqual(str(ots[0]),
                         'EPEpJSONObjectType(name="Building")')
        
        
    def test_object_type_names(self):
        ""
        self.assertEqual(j.object_type_names,
                         ['Building', 
                          'BuildingSurface:Detailed', 
                          'Construction', 
                          'Exterior:Lights', 
                          'GlobalGeometryRules', 
                          'HeatBalanceAlgorithm', 
                          'Material', 
                          'Material:NoMass', 
                          'OtherEquipment', 
                          'Output:Constructions', 
                          'Output:Meter:MeterFileOnly', 
                          'Output:Surfaces:Drawing', 
                          'Output:Table:SummaryReports', 
                          'Output:Variable', 
                          'Output:VariableDictionary', 
                          'OutputControl:Table:Style', 
                          'RunPeriod', 
                          'Schedule:Constant', 
                          'ScheduleTypeLimits', 
                          'SimulationControl', 
                          'Site:Location', 
                          'SizingPeriod:DesignDay', 
                          'SurfaceConvectionAlgorithm:Inside', 
                          'SurfaceConvectionAlgorithm:Outside', 
                          'Timestep', 
                          'Version', 
                          'Zone'])
    
    
    def test_remove_object_type(self):
        ""
        j1=EPInput(fp='files/1ZoneUncontrolled.epJSON')
        j1.remove_object_type('Building')
        self.assertFalse('Building' in j1.object_type_names)
    
    
    
    def test_summary(self):
        ""
        self.assertEqual(j.summary,
                         {'Building': 1, 
                          'BuildingSurface:Detailed': 6, 
                          'Construction': 3, 
                          'Exterior:Lights': 1, 
                          'GlobalGeometryRules': 1, 
                          'HeatBalanceAlgorithm': 1, 
                          'Material': 1, 
                          'Material:NoMass': 2, 
                          'OtherEquipment': 2, 
                          'Output:Constructions': 1, 
                          'Output:Meter:MeterFileOnly': 3, 
                          'Output:Surfaces:Drawing': 1, 
                          'Output:Table:SummaryReports': 1, 
                          'Output:Variable': 14, 
                          'Output:VariableDictionary': 1, 
                          'OutputControl:Table:Style': 1, 
                          'RunPeriod': 1, 
                          'Schedule:Constant': 1, 
                          'ScheduleTypeLimits': 2, 
                          'SimulationControl': 1, 
                          'Site:Location': 1, 
                          'SizingPeriod:DesignDay': 2, 
                          'SurfaceConvectionAlgorithm:Inside': 1, 
                          'SurfaceConvectionAlgorithm:Outside': 1, 
                          'Timestep': 1, 
                          'Version': 1, 
                          'Zone': 1})
        
    
    def test_validate(self):
        ""
        
        return
        
        #no schema
        self.assertRaises(Exception,
                          j.validate)
        # "Exception: No schema is set - please provide a schema to validate against"
        
        #passes
        j.validate(schema=s)
        
        return
        
        #fails
        j1=EPInput(fp='files/1ZoneUncontrolled.epJSON')
        del j1._dict['Building']
        # COULD COMMENT OUT BELOW AS IT TAKES 10+ SECONDS TO RUN.
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          j1.validate,
                          s)
        # "jsonschema.exceptions.ValidationError: 'Building' is a required property"
        
        
    def test_write(self):
        ""
        j.write('test.epJSON')
        
        
    
if __name__=='__main__':
    
    j=EPInput(fp='files/1ZoneUncontrolled.epJSON')
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    unittest.main(Test_EPInput())