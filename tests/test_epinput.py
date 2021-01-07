# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

import jsonschema

import eprun
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
        

    def test___get_item__(self):
        ""
        self.assertEqual(str(j['Building']),
                         """{'Simple One Zone (Wireframe DXF)': EPInputObject(name="Simple One Zone (Wireframe DXF)")}""")
        
        
        # o=j['Simple One Zone (Wireframe DXF)']
        # self.assertEqual(str(o),
        #                  'EPInputObject(name="Simple One Zone (Wireframe DXF)")')
        
        
    def test__get_object_type(self):
        ""
        self.assertEqual(j._get_object_type('Simple One Zone (Wireframe DXF)'),
                         'Building')
        
        
    def test__get_object_type_dict(self):
        ""
        self.assertEqual(j._get_object_type_dict('Building'),
                         {'Simple One Zone (Wireframe DXF)': 
                              {'loads_convergence_tolerance_value': 0.04, 
                               'maximum_number_of_warmup_days': 30, 
                               'minimum_number_of_warmup_days': 6, 
                               'north_axis': 0, 
                               'solar_distribution': 'MinimalShadowing', 
                               'temperature_convergence_tolerance_value': 0.004, 
                               'terrain': 'Suburbs'
                               }
                          })
        
            
    def test__parse_idf(self):
        ""
        s=EPSchema(fp='files/Energy+.schema.epJSON')
        i=EPInput(fp='files/1ZoneUncontrolled.idf',
                  schema=s)
        self.assertIsInstance(i._dict,
                              dict)
        self.assertEqual(len(i._dict),
                         27)
        
        
    def test_get_object(self):
        ""
        o=j.get_object('Simple One Zone (Wireframe DXF)')
        self.assertEqual(str(o),
                         'EPInputObject(name="Simple One Zone (Wireframe DXF)")')
        
        o=j.get_object('Simple One Zone (Wireframe DXF)','Building')
        self.assertEqual(str(o),
                         'EPInputObject(name="Simple One Zone (Wireframe DXF)")')
    
    
    def test_get_object_names(self):
        ""
        self.assertEqual(j.get_object_names('Building'),
                         ['Simple One Zone (Wireframe DXF)'])
    
    
    def test_get_objects(self):
        ""
        self.assertEqual(str(j.get_objects('Building')),
                         """{'Simple One Zone (Wireframe DXF)': EPInputObject(name="Simple One Zone (Wireframe DXF)")}""")
        
    
    def test_object_names(self):
        ""
        self.assertEqual(j.object_names,
                         ['Simple One Zone (Wireframe DXF)', 
                          'Zn001:Flr001', 
                          'Zn001:Roof001', 
                          'Zn001:Wall001', 
                          'Zn001:Wall002', 
                          'Zn001:Wall003', 
                          'Zn001:Wall004', 
                          'FLOOR', 
                          'R13WALL', 
                          'ROOF31', 
                          'ExtLights', 
                          'GlobalGeometryRules 1', 
                          'HeatBalanceAlgorithm 1', 
                          'C5 - 4 IN HW CONCRETE', 
                          'R13LAYER', 
                          'R31LAYER', 
                          'Test 352 minus', 
                          'Test 352a', 
                          'Output:Constructions 1', 
                          'Output:Meter:MeterFileOnly 1', 
                          'Output:Meter:MeterFileOnly 2', 
                          'Output:Meter:MeterFileOnly 3', 
                          'Output:Surfaces:Drawing 1', 
                          'Output:Table:SummaryReports 1', 
                          'Output:Variable 1', 
                          'Output:Variable 2', 
                          'Output:Variable 3', 
                          'Output:Variable 4', 
                          'Output:Variable 5', 
                          'Output:Variable 6', 
                          'Output:Variable 7', 
                          'Output:Variable 8', 
                          'Output:Variable 9', 
                          'Output:Variable 10', 
                          'Output:Variable 11', 
                          'Output:Variable 12', 
                          'Output:Variable 13', 
                          'Output:Variable 14', 
                          'Output:VariableDictionary 1', 
                          'OutputControl:Table:Style 1', 
                          'Run Period 1', 
                          'AlwaysOn', 
                          'Fraction', 
                          'On/Off', 
                          'SimulationControl 1', 
                          'Denver Centennial  Golden   N_CO_USA Design_Conditions', 
                          'Denver Centennial  Golden   N Ann Clg 1% Condns DB=>MWB', 
                          'Denver Centennial  Golden   N Ann Htg 99% Condns DB', 
                          'SurfaceConvectionAlgorithm:Inside 1', 
                          'SurfaceConvectionAlgorithm:Outside 1', 
                          'Timestep 1', 
                          'Version 1', 
                          'ZONE ONE'])
    
    
    def test_objects(self):
        ""
        self.assertIsInstance(j.objects,
                              dict)
        self.assertEqual(len(j.objects),
                         53)
    
        
    def test_object_types(self):
        ""
        self.assertEqual(j.object_types,
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
    
    
    def test_remove_object(self):
        ""
        j1=EPInput(fp='files/1ZoneUncontrolled.epJSON')
        j1.remove_object('Simple One Zone (Wireframe DXF)')
        self.assertFalse('Simple One Zone (Wireframe DXF)' in j1.object_names)
        self.assertFalse('Building' in j1.object_types)
    
    
    def test_set_object(self):
        ""
        j1=EPInput(fp='files/1ZoneUncontrolled.epJSON',
                   schema=s)
        
        # Invalid object type 
        self.assertRaises(IndexError,
                          j1.set_object,
                          'my_building','ABC')
       
        # Invalid property name 
        self.assertRaises(ValueError,
                          j1.set_object,
                          name='my_building',
                          object_type='Building',
                          my_property='ABC')
        self.assertEqual(len(j1['Building']),
                         1)
        
        # Invalid property value
        self.assertRaises(ValueError,
                          j1.set_object,
                          name='my_building',
                          object_type='Building',
                          north_axis='ABC')
        self.assertEqual(len(j1['Building']),
                         1)
        
        
        # Valid set_object
        j1.set_object(name='my_building',
                      object_type='Building',
                      north_axis=180)
        
        
    def test_schema(self):
        ""
        self.assertEqual(str(j.schema),
                         'EPSchema(version="9.4.0")')
    
    
    
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
        
        #passes
        j.schema=s
        j.validate()
        
        return
        
        #fails
        j1=EPInput(fp='files/1ZoneUncontrolled.epJSON',
                   schema=s)
        del j1._dict['Building']
        # COULD COMMENT OUT BELOW AS IT TAKES 10+ SECONDS TO RUN.
        self.assertRaises(jsonschema.exceptions.ValidationError,
                          j1.validate)
        # "jsonschema.exceptions.ValidationError: 'Building' is a required property"
        
        
    def test_write(self):
        ""
        j.write('test.epJSON')
        
        
    
if __name__=='__main__':
    
    s=EPSchema(fp='files/Energy+.schema.epJSON')
    j=EPInput(fp='files/1ZoneUncontrolled.epJSON',
              schema=s)
    
    unittest.main(Test_EPInput())