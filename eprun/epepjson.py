# -*- coding: utf-8 -*-


import json
import jsonschema


from .epepjson_object_type import EPEpJSONObjectType


class EPEpJSON():
    """A class for an EnergyPlus .epJSON input file.
    
    :param fp: The filepath of a .epJSON file.
        This can be relative or absolute.
        Optional, if not used then a blank EPEpJSON object is returned.
    :type fp: str
    :param schema: The schema for the epJSON file. 
            Optional. If used then validation will be done using this schema.
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
                 fp=None,
                 schema=None):
        ""
        if fp is None:
            self._dict={}
        else:
            with open(fp,'r') as f:
                self._dict=json.load(f)
    
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
        
    
    def _get_schema(self,schema=None):
        """Returns the schema to be used in a validation method
        
        :param schema: The schema for the epJSON file. 
            Optional. If used then validation will be done on against this schema.
        :type schema: EPSchema
        
        :returns: If `schema` is provided, then this is returned. 
            If not, then if the object was initialized with a schema then this schema is returned.
            Else `None` is returned.
            
        :rtype: EPSchema or None
        
        """
        if not schema is None:
            return schema
        
        elif not self._schema is None:
            return self._schema
        
        else:
            return None
        
    
    def get_object_type(self,
                        name,
                        schema=None):
        """Returns an object type in the .epJSON file.
        
        :param name: The name of the object type.
        :type name: str
    
        :rtype: EPEpJSONObjectType
        
        """
        
        schema=self._get_schema(schema)
        if not schema is None: # if a schema exists
            if not name in schema.object_names:
                raise IndexError('Object type name "%s" does not exist in schema.' % name)
            
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
    
    
    def remove_object_type(self,name):
        """Removes the object type and all associated objects from the .epJSON file.
        
        :param name: The name of the object type.
        :type name: str
        
        """
        del self._dict[name]
    
    
    @property
    def summary(self):
        """A count of each object type in the .epJSON file.
        
        :rtype: dict

        """
        return {k:len(v.keys()) for k,v in self._dict.items()}
        
    
    def validate(self,schema=None):
        """Validates the .epJSON file against a schema.
        
        :param schema: The schema for the epJSON file. 
            Optional. If used then validation will be done on against this schema.
        :type schema: EPSchema
        
        :raises: Exception - if no schema is present to validate against.
        :raises: jsonschema.exceptions.ValidationError if the .epJSON file is not valid against the schema.
        
        .. note::
        
           Schema validation occurs in two cases:
           1. A EPSchema instance is supplied to this method using the ``schema`` argument;
           2. The :py:class:`~eprun.epepjson.EPEpJSON` object was initiated with an EPSchema instance.
        
        
        """
        schema=self._get_schema(schema)
        
        try:
            schema.validate_epjson(self._dict)
        except AttributeError:
            raise Exception('No schema is set - please provide a schema to validate against')
        
        
        
    def write(self,fp):
        """Writes to a .epJSON file.
        
        :param fp: The filename.
            This can be relative or absolute.
        :type fp: str
        
        """
        with open(fp,'w') as f:
            f.write(json.dumps(self._dict,indent=4))
        
        
        
        
        
        
        
        
        
        
        
    