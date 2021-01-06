# -*- coding: utf-8 -*-

import unittest
from pprint import pprint
import jsonschema

from eprun import EPSchema


class Test_EPSchemaProperty(unittest.TestCase):
   
    
    def test___init__(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        print(p)
        print(dir(p))
        print(list(p.keys()))
        
        
    def test_anyOf(self):
        ""
        so=s.get_object_type('WindowMaterial:Screen')
        p=so.get_property('angle_of_resolution_for_screen_transmittance_output_map')
        self.assertEqual(p.anyOf,
                         [{'type': 'number', 
                           'enum': [0, 1, 2, 3, 5]}, 
                          {'type': 'string', 
                           'enum': ['']}
                          ])
        

    def test_data_type(self):
        ""
        so=s.get_object_type('ZoneAirContaminantBalance')
        p=so.get_property('outdoor_carbon_dioxide_schedule_name')
        self.assertEqual(p.data_type,
                         'object_list')
        

    def test_default(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        self.assertEqual(p.default,
                         '9.4')
        

    def test_enum(self):
        ""
        so=s.get_object_type('SimulationControl')
        p=so.get_property('do_zone_sizing_calculation')
        self.assertEqual(p.enum,
                         ['', 'No', 'Yes'])
        

    def test_exclusiveMaximum(self):
        ""
        so=s.get_object_type('Site:Location')
        p=so.get_property('elevation')
        self.assertEqual(p.exclusiveMaximum,
                         True)
        

    def test_exclusiveMinimum(self):
        ""
        so=s.get_object_type('Building')
        p=so.get_property('loads_convergence_tolerance_value')
        self.assertEqual(p.exclusiveMinimum,
                         True)
        

    def test_external_list(self):
        ""
        so=s.get_object_type('EnergyManagementSystem:Sensor')
        p=so.get_property('output_variable_or_output_meter_name')
        self.assertEqual(p.external_list,
                         ['autoRDDvariableMeter'])
    
    
    def test_field_name(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        self.assertEqual(p.field_name,
                         'Version Identifier')
        

    def test_ip_units(self):
        ""
        so=s.get_object_type('SizingPeriod:DesignDay')
        p=so.get_property('barometric_pressure')
        self.assertEqual(p.ip_units,
                         'inHg')
        

    # def test_items(self):
    #     ""
    #     so=s.get_object_type('ShadowCalculation')
    #     p=so.get_property('shading_zone_groups')
    #     self.assertEqual(p.items,
    #                      {'properties': 
    #                           {'shading_zone_group_zonelist_name': 
    #                                {'type': 'string', 
    #                                 'note': 'Specifies a group of zones which are controlled by the Disable Self-Shading fields.', 
    #                                 'data_type': 'object_list', 
    #                                 'object_list': ['ZoneListNames']
    #                                 }
    #                            }, 
    #                      'type': 'object'})
        

    def test_maxItems(self):
        ""
        so=s.get_object_type('Schedule:Year')
        p=so.get_property('schedule_weeks')
        self.assertEqual(p.maxItems,
                         53)
        

    def test_maximum(self):
        ""
        so=s.get_object_type('PerformancePrecisionTradeoffs')
        p=so.get_property('maxzonetempdiff')
        self.assertEqual(p.maximum,
                         3.0)
        

    def test_minItems(self):
        ""
        so=s.get_object_type('Schedule:Year')
        p=so.get_property('schedule_weeks')
        self.assertEqual(p.minItems,
                         1)
        

    def test_minimum(self):
        ""
        so=s.get_object_type('SimulationControl')
        p=so.get_property('maximum_number_of_hvac_sizing_simulation_passes')
        self.assertEqual(p.minimum,
                         1.0)
        
    
    def test_name(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        self.assertEqual(p.name,
                         'version_identifier')
        
        

    def test_note(self):
        ""
        so=s.get_object_type('SimulationControl')
        p=so.get_property('do_zone_sizing_calculation')
        self.assertEqual(p.note,
                         'If Yes, Zone sizing is accomplished from corresponding Sizing:Zone objects and autosize fields.')
        

    def test_object_list(self):
        ""
        so=s.get_object_type('ZoneAirContaminantBalance')
        p=so.get_property('outdoor_carbon_dioxide_schedule_name')
        self.assertEqual(p.object_list,
                         ['ScheduleNames'])
        

    def test_reference(self):
        ""
        so=s.get_object_type('AirflowNetwork:MultiZone:Zone')
        p=so.get_property('zone_name')
        self.assertEqual(p.reference,
                         ['AirFlowNetworkMultizoneZones'])
        

    def test_retaincase(self):
        ""
        so=s.get_object_type('SizingPeriod:WeatherFileConditionType')
        p=so.get_property('period_selection')
        self.assertEqual(p.retaincase,
                         True)
        

    def test_type_(self):
        ""
        so=s.get_object_type('Version')
        p=so.get_property('version_identifier')
        self.assertEqual(p.type_,
                         'string')
        

    def test_units(self):
        ""
        so=s.get_object_type('Building')
        p=so.get_property('north_axis')
        self.assertEqual(p.units,
                         'deg')
        

    def test_unitsBasedOnField(self):
        ""
        so=s.get_object_type('ScheduleTypeLimits')
        p=so.get_property('lower_limit_value')
        self.assertEqual(p.unitsBasedOnField,
                         'unit_type')
        

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