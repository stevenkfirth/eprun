# -*- coding: utf-8 -*-

import jsonschema
import collections


class EPSchemaProperty(collections.abc.Mapping):
    """A class representing a property of an EPSchemaObjectType.
    
    An EPSchemaProperty can act as a dictionary to access its properties and values.
    For example it has the `keys <dict.keys>`, `values <dict.values>` and 
    `items <dict.items>` attributes.
    
    .. note::
        
       An EPSchemaProperty instance is returned as the result of the 
       `EPSchemaObjectType.get_property` function.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
           
       >>> from eprun import EPSchema
       >>> s=EPSchema(fp='Energy+.schema.epJSON')
       >>> ot=s.get_object_type('Building')
       >>> p=ot.get_property('north_axis')
       >>> print(type(p))
       <class 'eprun.epschema_property.EPSchemaProperty'>
       >>> print(p.name)
       north_axis
       >>> print(list(p.keys()))
       ['type', 'note', 'units', 'default']
       >>> print(p['units'])
       deg
       
    """
    def __getitem__(self,key):
        ""
        return self._dict[key]
        
    
    def __iter__ (self):
        ""
        return iter(self._dict)
        
    
    def __len__ (self):
        ""
        return len(self._dict)
    
    
    def __repr__(self):
        ""
        return 'EPSchemaProperty(name="%s")' % (self._name)
    
    
    @property
    def _dict(self):
        ""
        return self._epsot._dict['patternProperties'][self._pattern_properties_regex]['properties'][self._name]
    
    
    @property
    def dict_(self):
        """The json dictionary for the EpSchemaProperty.
        
        :rtype: dict
        
        """
        return self._dict
    
    
    @property
    def idd_legacy_field_name(self):
        """The 'legacy_idd' field name of the EPSchemaProperty.
        
        :rtype: str
        
        """
        return self._epsot._dict['legacy_idd']['field_info'][self._name]['field_name']
    

    @property
    def name(self):
        """The name of the EPSchemaProperty.
        
        :rtype: str
        
        """
        return self._name


    def validate_value(self,value):
        """Validates a possible value for the EPSchemaProperty.
        
        :param value: The value to be validated.
        
        raises: jsonschema.exceptions.ValidationError - if the value is not valid

        """
        try:
            jsonschema.validate(value,
                                self._dict,
                                jsonschema.Draft4Validator)
        except jsonschema.exceptions.ValidationError as err:
            raise jsonschema.exceptions.ValidationError(str(err).split('\n')[0]) 
            
        