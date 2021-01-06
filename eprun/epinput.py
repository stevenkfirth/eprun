# -*- coding: utf-8 -*-


import json
import os
import re
from uuid import uuid4

from .epepjson_object_type import EPEpJSONObjectType


class EPInput():
    """A class for an EnergyPlus .idf or .epJSON input file.
    
    :param fp: The filepath of an .idf or .epJSON file.
        This can be relative or absolute.
        Optional, if not supplied then a blank EPInput object is returned.
    :type fp: str
    
    ..
      :param schema: The schema for the epJSON file. 
              Optional. If used then validation will be done using this schema.
      :type schema: EPSchema
    
    .. rubric:: Code Example
        
    .. code-block:: python
           
       >>> from eprun import EPEpJSON
       >>> epinput=EPInput(fp='1ZoneUncontrolled.idf')
       >>> print(input)
       EPInput(fp="1ZoneUncontrolled.idf")
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
        
        self._fp=fp
        self._schema=schema
        
        
        if fp is None:
            self._dict={}
            
        elif os.path.splitext(fp)[1]=='.epJSON':
            with open(fp,'r') as f:
                self._dict=json.load(f)
                
        elif os.path.splitext(fp)[1]=='.idf':
            with open(fp,'r') as f:
                st=f.read()
                self._dict=self._parse_idf(st)
                
        
    def __getitem__(self,key):
        """Returns the object type with name = key
        
        :rtype: EPEpJSONObjectType
        
        """
        return self.get_object_type(key)
        
    
    def _parse_idf(self,st):
        """Parses an idf string and returns a dictionary equivalent to the .epJSON dict
        
        :param st: A string of the entire .idf file
        :type st: str
        
        :rtype: dict
        
        """
        def _convert_arg_to_value(arg,schema_property_object):
            ""
            p=schema_property_object
            try:
                type_=p['type'] # schema property has a 'type' property
            
                if type_=='number':
                    
                    if arg=='':
                        raise ValueError()
                    else:
                        value=float(arg)
                
                elif type_=='string':
                    
                    value=arg
                    
                else:
                    
                    raise Exception()
                
                
            except KeyError: # schema property does not have a 'type' property
                
                if 'anyOf' in p:
                    
                    try:
                        value=float(arg)
                    except ValueError:
                        value=arg
                        
                else:
                    
                    raise Exception()
                
            return value
        
        #print(st.encode())
        
        # removes the comments
        st=re.sub(r'!.*\n','',st)
        #print(st)
        
        # split by ';'
        a=st.split(';')  # gives a list of object strings
        #print(a)
        
        # split by ','
        b=[a1.split(',') for a1 in a] # a list of object lists
        #print(b)
        
        # remove whitespace and empty objects
        b=[[b2.strip() for b2 in b1] for b1 in b if len(b1)>1]
        #print(b)
        
        # form dictionary
        d={}
        for object_type,*args in b:
            
            print('object_type:',object_type)
            
            # get schema objects
            schema_object_type=self.schema.get_object_type(object_type)
            legacy_idd_fields=schema_object_type.legacy_idd_fields
            property_names=schema_object_type.property_names
            
            # adjustments if object has a defined name in the schema
            if 'name' in schema_object_type:
                object_name=args[0]
                args=args[1:]
                legacy_idd_fields=legacy_idd_fields[1:]
            else:
                object_name=uuid4()
                
            #print('object_name',object_name)
            #print('args',args)
            #print('fields',fields)
            #print('property_names',property_names)
            
            # create the object properties dictionary
            properties={}
            i=0
            while i<len(args):
                
                try:
                    
                    # get property value and key
                    arg=args[i]
                    legacy_idd_field=legacy_idd_fields[i] # this will raise the IndexError is the object is 'extensible'
                    
                    #print('arg:',arg)
                    #print('legacy_idd_field:',legacy_idd_field)
                    
                    # get schema property object
                    p=schema_object_type.get_property(legacy_idd_field)
                    
                    try:
                        value=_convert_arg_to_value(arg, p)
                        properties[legacy_idd_field]=value
                    except ValueError:
                        pass
                    
                    i+=1
                    
                    
                except IndexError: # if the object includes extensible properties
                    
                    # get extensible property name
                    property_name=property_names[-1] 
                
                    #print('property_name', property_name)
                    
                    # get schema property object
                    p=schema_object_type.get_property(property_name)
                    
                    d1=properties.setdefault(p.name,[])
                    
                    d2={}
                    for k,v in p['items']['properties'].items():
                        
                        if v['type']=='number':
                            value=float(args[i])  
                        elif v['type']=='string':
                            value=args[i]
                        else:
                            raise Exception()
                        #print('value',value)
                        
                        
                        d2[k]=value
                        i+=1
                    
                    d1.append(d2)
                
                     
            #print('properties',properties)
            
            # get (or create) the object_type_dict
            obj_type_dict=d.setdefault(object_type,{})
            
            # add object item to object_type_dict
            obj_type_dict[object_name]=properties
            
        #print('d',d)
        
        return d
        
        
    
    
    # def _get_schema(self,schema=None):
    #     """Returns the schema to be used in a validation method
        
    #     :param schema: The schema for the epJSON file. 
    #         Optional. If used then validation will be done on against this schema.
    #     :type schema: EPSchema
        
    #     :returns: If `schema` is provided, then this is returned. 
    #         If not, then if the object was initialized with a schema then this schema is returned.
    #         Else `None` is returned.
            
    #     :rtype: EPSchema or None
        
    #     """
    #     if not schema is None:
    #         return schema
        
    #     elif not self._schema is None:
    #         return self._schema
        
    #     else:
    #         return None
        
    
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
            if not name in schema.object_type_names:
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
    def schema(self):
        """The schema for the EnergyPlus input file.
        
        :raises Exception: If the schema has not been defined for the EPInput object.
        
        :rtype: EPSchema
        
        """
        if self._schema is None:
            raise Exception('This operation requires an EPSchema to be defined. '
                            'This is done by supplying the "schema" argument or setting the .schema attribute')
        else:
            return self._schema
    
    
    @schema.setter
    def schema(self,value):
        """
        :param value:
        :type value: EPSchema

        """
        self._schema=value
        
    
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
        
        
        
        
        
        
        
        
        
        
        
    