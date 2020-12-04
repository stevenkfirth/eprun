# -*- coding: utf-8 -*-

import unittest
from pprint import pprint

from eprun import EPEpJSON


class Test_EPEpJSON(unittest.TestCase):
   
    def test___init__(self):
        ""
        self.assertIsInstance(j,
                              EPEpJSON)
        
    def test___repr__(self):
        ""
        self.assertEqual(str(j),
                         'EPEpJSON(fp="files/1ZoneUncontrolled.epJSON")')
        
        
    def test___get_item__(self):
        ""
        ot=j['Building']
        self.assertEqual(str(ot),
                         'EPEpJSONObjectType(name="Building")')
        
        
    def test_get_object_type(self):
        ""
        ot=j.get_object_type('Building')
        self.assertEqual(str(ot),
                         'EPEpJSONObjectType(name="Building")')
        
        
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
        
    
    
if __name__=='__main__':
    
    j=EPEpJSON(fp='files/1ZoneUncontrolled.epJSON')
    unittest.main(Test_EPEpJSON())