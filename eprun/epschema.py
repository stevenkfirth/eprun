# -*- coding: utf-8 -*-

import json
import jsonschema

from .epschema_object_type import EPSchemaObjectType

class EPSchema():
    """A class for an EnergyPlus .schema.epJSON file.
    
    :param fp: The filepath of the .schema.epJSON file.
        This can be relative or absolute.
    :type fp: str
    
    .. rubric:: Code Example
        
    .. code-block:: python
           
       >>> from eprun import EPSchema
       >>> s=EPSchema(fp='Energy+.schema.epJSON')
       >>> print(type(s))
       <class 'eprun.epschema.EPSchema'>
       >>> print(s)
       EPSchema(version="9.4.0")
       >>> print(s.version)
       9.4.0
       >>> print(len(s.get_object_types()))
       815
       >>> print(s.get_object_types()[0])
       EPSchemaObjectType(name="Version")
       
    .. seealso::
    
       EnergyPlus Essentials, page 19.
       https://energyplus.net/quickstart
    
    """
    
    def __init__(self,
                 fp):
        ""
        with open(fp,'r') as f:
            schema_dict=json.load(f)
        
        self._dict=schema_dict
    
    
    def __repr__(self):
        ""
        return 'EPSchema(version="%s")' % (self.version)
    
    
    @property
    def _validator(self):
        """The jsonschema Draft4Validator object for the schema
        
        :rtype: jsonschema.Draft4Validator
        
        .. note::
            
           The first time this is requested, the schema itself is validated and
           the Draft4Validator object is placed in a cache.
        
        """
        if hasattr(self,'_validator_cache') and self._validator_cache:
            return self._validator_cache
        else:
            jsonschema.Draft4Validator.check_schema(self._dict)
            self._validator_cache=jsonschema.Draft4Validator(schema=self._dict)
            return self._validator_cache
    
    
    @property
    def build(self):
        """The schema build value as given by 'epJSON_schema_build' key.
        
        :rtype: str
        
        """
        return self._dict['epJSON_schema_build']
    
    
    @property
    def dict_(self):
        """The json dictionary for the schema.
        
        :rtype: dict 
        
        """
        return self._dict
    
    
    
    def get_object_type(self,
                        object_type_name):
        """Returns a schema object type in the EPSchema file.
        
        :rtype: EPSchemaObjectType
        
        """
        epso=EPSchemaObjectType()
        epso.__dict__['_eps']=self
        epso.__dict__['_name']=object_type_name
        return epso
    
    
    def get_object_types(self):
        """Returns the schema objects in the EPSchema file.
        
        :rtype: list (EPSchemaObjectType)
        
        """
        
        result=[]
        for x in self.object_type_names:
            result.append(self.get_object_type(x))
        return result
        
    
    @property
    def object_type_names(self):
        """The object type names in the schema.
        
        :rtype: list (str)
        
        """
        return list(self._dict['properties'].keys())
    
    
    @property
    def required(self):
        """The required object types list as given by the 'required' key.
        
        :rtype: list (str)
        
        """
        return self._dict['required']
    
    
    def validate_epjson(self,epjson_dict):
        """Validates an .epJSON file against the schema.
        
        :param epjson_dict: The JSON dictionary of a .epJSON file.        
        :type epjson_dict: dict
        
        :raises: jsonschema.exceptions.ValidationError - if the .epJSON file is not valid
        
        """
        try:
            self._validator.validate(epjson_dict)
        except jsonschema.exceptions.ValidationError as err:
            raise jsonschema.exceptions.ValidationError(str(err).split('\n')[0])  
        
    
    @property
    def version(self):
        """The schema version value as given by the 'epJSON_schema_version' key.
        
        :rtype: str
        
        """
        return self._dict['epJSON_schema_version']
    
    
    
    
    
    
    
    
    
    