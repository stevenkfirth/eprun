# -*- coding: utf-8 -*-

import unittest

import eprun
from eprun import EPJSON, read_idf, read_epjson

from pprint import pprint
import os
import jsonschema
from jsonpi import read_json_schema

fp_idf='files/1ZoneUncontrolled.idf'
fp_epJSON='files/1ZoneUncontrolled.epJSON'
fp_schema='files/Energy+.schema.epJSON'

schema=read_json_schema(fp_schema)

epjson=read_epjson(fp_epJSON,
                   schema)


class Test_read_idf(unittest.TestCase):
    ""
    
    def test_read_idf(self):
        ""
        x=read_idf(fp_idf,
                   schema)
        self.assertIsInstance(x,
                              EPJSON)
        self.assertEqual(len(x),
                         len(epjson))
        
        
    # def test_read_ep_example_file_idfs(self):
    #     ""
    #     example_files_dir=r'C:\EnergyPlusV9-4-0\ExampleFiles'
    #     schema_fp=r'C:\EnergyPlusV9-4-0\Energy+.schema.epJSON'
    #     schema=read_jsonschema(schema_fp)
    #     files=[os.path.join(example_files_dir,x) for x in os.listdir(example_files_dir) 
    #            if os.path.isfile(os.path.join(example_files_dir,x))]
    #     files_idf=[x for x in files if os.path.splitext(x)[1]=='.idf']
        
    #     start=141
    #     for i,idf_fp in enumerate(files_idf[141:]):
    #         print(i+start, idf_fp)
    #         d=read_idf(idf_fp,schema)
        



class Test_EPJSON(unittest.TestCase):
    ""
    
    def test___init__(self):
        ""
        self.assertIsInstance(epjson,
                              EPJSON)
        
        
    def test_add_input_object(self):
        ""
        e=EPJSON({},schema)
        e.add_input_object(input_type='Building',
                           name='building1',
                           north_axis=0
                           )
        self.assertEqual(e.Building.names()[0],
                         'building1')
        self.assertEqual(e.Building.building1.north_axis,
                         0)
        
        
    def test_get_input_object(self):
        ""
        io=epjson.get_input_object(name='Simple One Zone (Wireframe DXF)')
        self.assertEqual(io.north_axis,
                         0)
        self.assertEqual(io.name(),
                         'Simple One Zone (Wireframe DXF)')
        self.assertEqual(io.obj(),
                         epjson.Building)
        self.assertEqual(io.input_type(),
                         'Building')
        
        
    def test_get_input_objects(self):
        ""
        objs=epjson.get_input_objects()
        self.assertEqual(len(objs),
                         53)
        
        objs=epjson.get_input_objects(input_type='Building')
        self.assertEqual(len(objs),
                         1)
        
        
    def test_remove_input_object(self):
        ""
        e=EPJSON({},schema)
        e.add_input_object(input_type='Building',
                           name='building1',
                           north_axis=0
                           )
        self.assertEqual(len(e.get_input_objects()),
                         1)
        e.remove_input_object(input_type='Building',
                              name='building1')
        self.assertEqual(len(e.get_input_objects()),
                         0)
        
        
    def test_schema(self):
        ""
        self.assertEqual(epjson.schema(),
                         schema)
        
        
    def test_summary(self):
        ""
        self.assertEqual(epjson.summary(),
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
        

    def test_write_json(self):
        ""
        epjson.write_json(r'files/test.epjson')



# class Test_EPInput_old(unittest.TestCase):
   
#     def _test___init__epjson(self):
#         ""
#         self.assertIsInstance(epi,
#                               EPInput)
        
        
#     def _test___init__idf(self):
#         ""
#         epi_idf=EPInput(fp='files/1ZoneUncontrolled.idf',
#                         schema=schema)
#         self.assertIsInstance(epi_idf,
#                               EPInput)
        
        
#         epi_idf=EPInput(fp='files/1ZoneDataCenterCRAC_wApproachTemp.idf',
#                         schema=schema)
#         self.assertIsInstance(epi_idf,
#                               EPInput)
        
    
    
#     def _test_get_object(self):
#         ""
#         o=epi.get_object('Simple One Zone (Wireframe DXF)')
#         self.assertEqual(o.name,
#                          'Simple One Zone (Wireframe DXF)')
#         #print(o)
        
        
#     def _test_get_objects(self):
#         ""
#         objs=epi.get_objects(name='Simple One Zone (Wireframe DXF)')
#         self.assertEqual(objs[0].name,
#                          'Simple One Zone (Wireframe DXF)')
            
#         objs=epi.get_objects(surface_type='Floor')
#         #print(objs); return
#         self.assertEqual(objs[0].name,
#                          'Zn001:Flr001')
    
    
    
        

    # def test___get_item__(self):
    #     ""
    #     self.assertEqual(str(j['Building']),
    #                      """{'Simple One Zone (Wireframe DXF)': EPInputObject(name="Simple One Zone (Wireframe DXF)")}""")
        
        
    #     # o=j['Simple One Zone (Wireframe DXF)']
    #     # self.assertEqual(str(o),
    #     #                  'EPInputObject(name="Simple One Zone (Wireframe DXF)")')
        
        
    # def test__get_object_type(self):
    #     ""
    #     self.assertEqual(j._get_object_type('Simple One Zone (Wireframe DXF)'),
    #                      'Building')
        
        
    # def test__get_object_type_dict(self):
    #     ""
    #     self.assertEqual(j._get_object_type_dict('Building'),
    #                      {'Simple One Zone (Wireframe DXF)': 
    #                           {'loads_convergence_tolerance_value': 0.04, 
    #                            'maximum_number_of_warmup_days': 30, 
    #                            'minimum_number_of_warmup_days': 6, 
    #                            'north_axis': 0, 
    #                            'solar_distribution': 'MinimalShadowing', 
    #                            'temperature_convergence_tolerance_value': 0.004, 
    #                            'terrain': 'Suburbs'
    #                            }
    #                       })
        
            
    # def test__parse_idf(self):
    #     ""
    #     s=EPSchema(fp='files/Energy+.schema.epJSON')
    #     i=EPInput(fp='files/1ZoneUncontrolled.idf',
    #               schema=s)
    #     self.assertIsInstance(i._dict,
    #                           dict)
    #     self.assertEqual(len(i._dict),
    #                      27)
        
        
    
    
    # def test_get_object_names(self):
    #     ""
    #     self.assertEqual(j.get_object_names('Building'),
    #                      ['Simple One Zone (Wireframe DXF)'])
    
    
    
    
    # def test_object_names(self):
    #     ""
    #     self.assertEqual(j.object_names,
    #                      ['Simple One Zone (Wireframe DXF)', 
    #                       'Zn001:Flr001', 
    #                       'Zn001:Roof001', 
    #                       'Zn001:Wall001', 
    #                       'Zn001:Wall002', 
    #                       'Zn001:Wall003', 
    #                       'Zn001:Wall004', 
    #                       'FLOOR', 
    #                       'R13WALL', 
    #                       'ROOF31', 
    #                       'ExtLights', 
    #                       'GlobalGeometryRules 1', 
    #                       'HeatBalanceAlgorithm 1', 
    #                       'C5 - 4 IN HW CONCRETE', 
    #                       'R13LAYER', 
    #                       'R31LAYER', 
    #                       'Test 352 minus', 
    #                       'Test 352a', 
    #                       'Output:Constructions 1', 
    #                       'Output:Meter:MeterFileOnly 1', 
    #                       'Output:Meter:MeterFileOnly 2', 
    #                       'Output:Meter:MeterFileOnly 3', 
    #                       'Output:Surfaces:Drawing 1', 
    #                       'Output:Table:SummaryReports 1', 
    #                       'Output:Variable 1', 
    #                       'Output:Variable 2', 
    #                       'Output:Variable 3', 
    #                       'Output:Variable 4', 
    #                       'Output:Variable 5', 
    #                       'Output:Variable 6', 
    #                       'Output:Variable 7', 
    #                       'Output:Variable 8', 
    #                       'Output:Variable 9', 
    #                       'Output:Variable 10', 
    #                       'Output:Variable 11', 
    #                       'Output:Variable 12', 
    #                       'Output:Variable 13', 
    #                       'Output:Variable 14', 
    #                       'Output:VariableDictionary 1', 
    #                       'OutputControl:Table:Style 1', 
    #                       'Run Period 1', 
    #                       'AlwaysOn', 
    #                       'Fraction', 
    #                       'On/Off', 
    #                       'SimulationControl 1', 
    #                       'Denver Centennial  Golden   N_CO_USA Design_Conditions', 
    #                       'Denver Centennial  Golden   N Ann Clg 1% Condns DB=>MWB', 
    #                       'Denver Centennial  Golden   N Ann Htg 99% Condns DB', 
    #                       'SurfaceConvectionAlgorithm:Inside 1', 
    #                       'SurfaceConvectionAlgorithm:Outside 1', 
    #                       'Timestep 1', 
    #                       'Version 1', 
    #                       'ZONE ONE'])
    
    
    # def test_objects(self):
    #     ""
    #     self.assertIsInstance(j.objects,
    #                           dict)
    #     self.assertEqual(len(j.objects),
    #                      53)
    
        
    # def test_object_types(self):
    #     ""
    #     self.assertEqual(j.object_types,
    #                      ['Building', 
    #                       'BuildingSurface:Detailed', 
    #                       'Construction', 
    #                       'Exterior:Lights', 
    #                       'GlobalGeometryRules', 
    #                       'HeatBalanceAlgorithm', 
    #                       'Material', 
    #                       'Material:NoMass', 
    #                       'OtherEquipment', 
    #                       'Output:Constructions', 
    #                       'Output:Meter:MeterFileOnly', 
    #                       'Output:Surfaces:Drawing', 
    #                       'Output:Table:SummaryReports', 
    #                       'Output:Variable', 
    #                       'Output:VariableDictionary', 
    #                       'OutputControl:Table:Style', 
    #                       'RunPeriod', 
    #                       'Schedule:Constant', 
    #                       'ScheduleTypeLimits', 
    #                       'SimulationControl', 
    #                       'Site:Location', 
    #                       'SizingPeriod:DesignDay', 
    #                       'SurfaceConvectionAlgorithm:Inside', 
    #                       'SurfaceConvectionAlgorithm:Outside', 
    #                       'Timestep', 
    #                       'Version', 
    #                       'Zone'])
    
    
    # def test_remove_object(self):
    #     ""
    #     j1=EPInput(fp='files/1ZoneUncontrolled.epJSON')
    #     j1.remove_object('Simple One Zone (Wireframe DXF)')
    #     self.assertFalse('Simple One Zone (Wireframe DXF)' in j1.object_names)
    #     self.assertFalse('Building' in j1.object_types)
    
    
    # def test_set_object(self):
    #     ""
    #     j1=EPInput(fp='files/1ZoneUncontrolled.epJSON',
    #                schema=s)
        
    #     # Invalid object type 
    #     self.assertRaises(IndexError,
    #                       j1.set_object,
    #                       'my_building','ABC')
       
    #     # Invalid property name 
    #     self.assertRaises(ValueError,
    #                       j1.set_object,
    #                       name='my_building',
    #                       object_type='Building',
    #                       my_property='ABC')
    #     self.assertEqual(len(j1['Building']),
    #                      1)
        
    #     # Invalid property value
    #     self.assertRaises(ValueError,
    #                       j1.set_object,
    #                       name='my_building',
    #                       object_type='Building',
    #                       north_axis='ABC')
    #     self.assertEqual(len(j1['Building']),
    #                      1)
        
        
    #     # Valid set_object
    #     j1.set_object(name='my_building',
    #                   object_type='Building',
    #                   north_axis=180)
        
        
    # def test_schema(self):
    #     ""
    #     self.assertEqual(str(j.schema),
    #                      'EPSchema(version="9.4.0")')
    
    
    
    # def test_summary(self):
    #     ""
    #     self.assertEqual(j.summary,
    #                      {'Building': 1, 
    #                       'BuildingSurface:Detailed': 6, 
    #                       'Construction': 3, 
    #                       'Exterior:Lights': 1, 
    #                       'GlobalGeometryRules': 1, 
    #                       'HeatBalanceAlgorithm': 1, 
    #                       'Material': 1, 
    #                       'Material:NoMass': 2, 
    #                       'OtherEquipment': 2, 
    #                       'Output:Constructions': 1, 
    #                       'Output:Meter:MeterFileOnly': 3, 
    #                       'Output:Surfaces:Drawing': 1, 
    #                       'Output:Table:SummaryReports': 1, 
    #                       'Output:Variable': 14, 
    #                       'Output:VariableDictionary': 1, 
    #                       'OutputControl:Table:Style': 1, 
    #                       'RunPeriod': 1, 
    #                       'Schedule:Constant': 1, 
    #                       'ScheduleTypeLimits': 2, 
    #                       'SimulationControl': 1, 
    #                       'Site:Location': 1, 
    #                       'SizingPeriod:DesignDay': 2, 
    #                       'SurfaceConvectionAlgorithm:Inside': 1, 
    #                       'SurfaceConvectionAlgorithm:Outside': 1, 
    #                       'Timestep': 1, 
    #                       'Version': 1, 
    #                       'Zone': 1})
        
    
    # def test_validate(self):
    #     ""
        
    #     return
        
    #     #passes
    #     j.schema=s
    #     j.validate()
        
    #     return
        
    #     #fails
    #     j1=EPInput(fp='files/1ZoneUncontrolled.epJSON',
    #                schema=s)
    #     del j1._dict['Building']
    #     # COULD COMMENT OUT BELOW AS IT TAKES 10+ SECONDS TO RUN.
    #     self.assertRaises(jsonschema.exceptions.ValidationError,
    #                       j1.validate)
    #     # "jsonschema.exceptions.ValidationError: 'Building' is a required property"
        
        
    # def test_write_json(self):
    #     ""
    #     j.write_json('test.epJSON')
        
        
    # def test_write_idf(self):
    #     ""
    #     j.write_idf('test.idf')
    
        
        
    
if __name__=='__main__':
    

    unittest.main()