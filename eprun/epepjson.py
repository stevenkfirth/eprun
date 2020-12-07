# -*- coding: utf-8 -*-


import json

from .epepjson_object_type import EPEpJSONObjectType


class EPEpJSON():
    """A class for an EnergyPlus .epJSON input file.
    
    :param fp: The filepath of the .epJSON file.
        This can be relative or absolute.
    :type fp: str
    :param schema: The schema for the epJSON file. 
            Optional. If used then validation will be done on the 
            property name and the property value.
    :type schema: EPSchema
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPEpJSON
       >>> j=EPEpJSON(fp='1ZoneUncontrolled.epJSON')
       >>> print(j)
       EPEpJSON(fp="1ZoneUncontrolled.epJSON")
       >>> print(j.object_type_names)
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
        'Zone']
 
    .. seealso::
    
       EnergyPlus Essentials, page 19.
       https://energyplus.net/quickstart
       
    """
    
    def __init__(self,
                 fp,
                 schema=None):
        ""
        with open(fp,'r') as f:
            d=json.load(f)
        
        self._dict=d
        self._fp=fp
        self._schema=schema
        
        
    def __getitem__(self,key):
        """Returns the object type with name = key
        
        :rtype: EPEpJSONObjectType
        
        """
        return self.get_object_type(key)
        
        
    def __repr__(self):
        ""
        return 'EPEpJSON(fp="%s")' % self._fp 
        
    
    def get_object_type(self,name):
        """Returns an object type in the .epJSON file.
        
        :param name: The name of the object type.
        :type name: str
    
        :rtype: EPEpJSONObjectType
        
        """
        ot=EPEpJSONObjectType()
        ot._epjson=self
        ot._name=name
        return ot
        
        
    def get_object_types(self):
        """Returns the object types in the .epJSON file.
    
        :rtype: list
        
        """
        return [self.get_object_type(x) for x in self.object_type_names]
        
    
    @property
    def object_type_names(self):
        """The object type names in the .epJSON file.
        
        :rtype: list
        
        """
        return list(self._dict.keys())
    
    
    @property
    def summary(self):
        """A count of each object type in the .epJSON file.
        
        :rtype: dict

        """
        return {k:len(v.keys()) for k,v in self._dict.items()}
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    