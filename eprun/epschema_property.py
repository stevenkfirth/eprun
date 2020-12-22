# -*- coding: utf-8 -*-

import jsonschema


class EPSchemaProperty():
    """A class representing a property of an EPSchemaObject.
    
    .. note::
        
       An EPSchemaProperty instance is returned as the result of the 
       EPSchemaObject :py:meth:`~eprun.epschema_object.EPSchemaObject.get_property` function.
       It should not be instantiated directly.
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPSchema
       >>> s=EPSchema(fp='Energy+.schema.epJSON')
       >>> o=s.get_object('Version')
       >>> p=o.get_property('version_identifier')
       >>> print(p)
       EPSchemaProperty(name="version_identifier")
       >>> print(n.type_)
       string
       >>> print(n.default)
       9.4
    
    """
    
    def __repr__(self):
        ""
        return 'EPSchemaProperty(name="%s")' % (self._name)
    
    
    @property
    def _dict(self):
        """Returns the json dictionary for the schema propoerty.
        
        :rtype: dict
        
        """
        return self._epso._dict['patternProperties'][self._pattern_properties_regex]['properties'][self._name]


    @property
    def anyOf(self):
        """The anyOf property of the schema property object.
        
        :returns: The 'anyOf' list, or None if not present.
        :rtype: list or None
        
        """
        return self._dict.get('anyOf',None)


    @property
    def data_type(self):
        """The data type property of the schema property object.
        
        :returns: The 'data_type' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('data_type',None)
    
    
    @property
    def default(self):
        """The default property of the schema property object.
        
        :returns: The 'default' string/float, or None if not present.
        :rtype: float or str or None
        
        """
        return self._dict.get('default',None)
    
    
    @property
    def enum(self):
        """The enum property of the schema property object.
        
        :returns: The 'enum' list, or None if not present.
        :rtype: list or None
        
        """
        return self._dict.get('enum',None)
    

    @property
    def exclusiveMaximum(self):
        """The exclusiveMaximum property of the schema property object.
        
        :returns: The 'exclusiveMaximum' boolean, or None if not present.
        :rtype: bool or None
        
        """
        return self._dict.get('exclusiveMaximum',None)
    

    @property
    def exclusiveMinimum(self):
        """The exclusiveMinimum property of the schema property object.
        
        :returns: The 'exclusiveMinimum' bool, or None if not present.
        :rtype: bool or None
        
        """
        return self._dict.get('exclusiveMinimum',None)
    

    @property
    def external_list(self):
        """The external_list property of the schema property object.
        
        :returns: The 'external_list' list, or None if not present.
        :rtype: list or None
        
        """
        return self._dict.get('external_list',None)
    
    
    @property
    def field_name(self):
        """The field_name of the schema property.
        
        :returns: The 'legacy_idd' field name of the property. 
        
        """
        return self._epso._dict['legacy_idd']['field_info'][self._name]['field_name']
    

    @property
    def ip_units(self):
        """The ip-units property of the schema property object.
        
        :returns: The 'ip-units' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('ip-units',None)
    

    @property
    def items(self):
        """The items property of the schema property object.
        
        :returns: The 'items' dict, or None if not present.
        :rtype: dict or None
        
        """
        return self._dict.get('items',None)
    

    @property
    def maxItems(self):
        """The maxItems property of the schema property object.
        
        :returns: The 'maxItems' integer, or None if not present.
        :rtype: int or None
        
        """
        return self._dict.get('maxItems',None)
    

    @property
    def maximum(self):
        """The maximum property of the schema property object.
        
        :returns: The 'maximum' float, or None if not present.
        :rtype: float or None
        
        """
        return self._dict.get('maximum',None)
    

    @property
    def minItems(self):
        """The minItems property of the schema property object.
        
        :returns: The 'minItems' integer, or None if not present.
        :rtype: int or None
        
        """
        return self._dict.get('minItems',None)
    

    @property
    def minimum(self):
        """The minimum property of the schema property object.
        
        :returns: The 'minimum' float, or None if not present.
        :rtype: float or None
        
        """
        return self._dict.get('minimum',None)
    
    
    @property
    def name(self):
        """The name of the schema property.
        
        :rtype: str
        
        """
        return self._name


    @property
    def note(self):
        """The note property of the schema property object.
        
        :returns: The 'note' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('note',None)
    

    @property
    def object_list(self):
        """The object_list property of the schema property object.
        
        :returns: The 'object_list' list, or None if not present.
        :rtype: list or None
        
        """
        return self._dict.get('object_list',None)
    

    @property
    def reference(self):
        """The reference property of the schema property object.
        
        :returns: The 'reference' list, or None if not present.
        :rtype: list or None
        
        """
        return self._dict.get('reference',None)
    

    @property
    def retaincase(self):
        """The retaincase property of the schema property object.
        
        :returns: The 'retaincase' boolean, or None if not present.
        :rtype: bool or None
        
        """
        return self._dict.get('retaincase',None)
    
    
    @property
    def type_(self):
        """The type property of the schema property object.
        
        :returns: The 'type' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('type',None)
    
    
    @property
    def units(self):
        """The units property of the schema property object.
        
        :returns: The 'units' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('units',None)
    
    
    @property
    def unitsBasedOnField(self):
        """The unitsBasedOnField property of the schema property object.
        
        :returns: The unitsBasedOnField'' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('unitsBasedOnField',None)
    

    def validate_value(self,value):
        """Validates a possible value for the property.
        
        :param value: The value to be validated.
        
        raises: jsonschema.exceptions.ValidationError - if the value is not valid

        """
        try:
            jsonschema.validate(value,
                                self._dict,
                                jsonschema.Draft4Validator)
        except jsonschema.exceptions.ValidationError as err:
            raise jsonschema.exceptions.ValidationError(str(err).split('\n')[0]) 
            
        