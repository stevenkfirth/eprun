# -*- coding: utf-8 -*-

import json
import jsonschema

from .epschema_object import EPSchemaObject

class EPSchema():
    """A class for an EnergyPlus .schema.epJSON file.
    
    :param fp: The filepath of the .schema.epJSON file.
        This can be relative or absolute.
    :type fp: str
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPSchema
       >>> s=EPSchema(fp='Energy+.schema.epJSON')
       >>> print(s)
       EPSchema(version="9.4.0")
       >>> print(s.version)
       9.4.0
       >>> print(len(s.get_objects()))
       815
       
    .. seealso::
    
       EnergyPlus Essentials, page 19.
       https://energyplus.net/quickstart
    
    """
    
    def __init__(self,
                 fp):
        ""
        with open(fp,'r') as f:
            schema=json.load(f)
        
        self.__dict=schema
    
    
    def __repr__(self):
        ""
        return 'EPSchema(version="%s")' % (self.version)
    
    
    @property
    def _dict(self):
        """The json dictionary for the schema.
        
        :rtype: dict
        
        """
        return self.__dict
    
    
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
        """The schema build as given by 'epJSON_schema_build'.
        
        :rtype: str
        
        """
        return self._dict['epJSON_schema_build']
    
    
    def get_object(self,
                   object_name):
        """Returns a schema object in the schema file.
        
        :rtype: EPSchemaObject
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> print(s.get_object('Version'))
           EPSchemaObject(name="Version")
        
        """
        epso=EPSchemaObject()
        epso._eps=self
        epso._name=object_name
        return epso
    
    
    def get_objects(self):
        """Returns the schema objects in the schema file.
        
        :returns: A list of EPSchemaObject instances.
        :rtype: list
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> print(s.get_objects()[0])
           EPSchemaObject(name="Version")
           >>> print(len(s.get_objects()))
           815
        
        """
        
        result=[]
        for x in self.object_names:
            result.append(self.get_object(x))
        return result
        
    
    @property
    def object_groups(self):
        """The object groups in the schema.
        
        :returns: This looks through the object names and returns the groups 
            to the left of the last colon.
            If an object name does not have a colon then it is not included here.
        :rtype: list
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> print(s.object_groups[0])
           WindowMaterial:Blind
           >>> print(len(so.object_groups))
           263
        
        """
        return list({':'.join(x.split(':')[:-1]) for x in self.object_names if ':' in x})
    
    
    @property
    def object_names(self):
        """The object names in the schema.
        
        :rtype: list
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> print(s.object_names[0])
           Version
           >>> print(len(so.object_names))
           815
        
        """
        return list(self._dict['properties'].keys())
    
    
    @property
    def required(self):
        """The required objects as given by 'required'.
        
        :returns: A list of object names as strings.
        :rtype: list
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> print(s.required)
           ['Building', 'GlobalGeometryRules']
        
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
        """The schema version as given by 'epJSON_schema_version'.
        
        :rtype: str
        
        """
        return self._dict['epJSON_schema_version']
    
    
    
    
    
    
    
    
    
    