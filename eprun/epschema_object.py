# -*- coding: utf-8 -*-

from .epschema_name import EPSchemaName
from .epschema_property import EPSchemaProperty


class EPSchemaObject():
    """A class representing an object in a EnergyPlus .schema.epJSON file.
    
    .. note::
        
       An EPSchemaObject instance is returned as the result of the EPSchema :py:meth:`~eprun.epschema.EPSchema.get_object` function.
       It should not be instantiated directly.
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPSchema
       >>> s=EPSchema(fp='Energy+.schema.epJSON')
       >>> o=s.get_object('Version')
       >>> print(o)
       EPSchemaObject(name="Version")
       >>> print(o.name)
       Version    
    
    """
    
    def __repr__(self):
        ""
        return 'EPSchemaObject(name="%s")' % (self.name)
    
    
    @property
    def _dict(self):
        """The json dictionary for the schema object
        
        :rtype: dict
        
        """
        return self._eps._dict['properties'][self.name]
    
    
    @property
    def additional_properties(self):
        """The additional properties of the schema object.
        
        :returns: The 'additionalProperties' string, or None if not present.
        :rtype: bool or None   
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.additional_properties)
           None
           >>> o1=s.get_object('ZoneCapacitanceMultiplier:ResearchSpecial')
           >>> print(o1.additional_properties)
           False
        
        """
        return self._dict.get('additionalProperties',None)
    
    
    @property
    def extensible_size(self):
        """The extensible_size of the schema object.
        
        :returns: The 'extensible_size' number, or None if not present.
        :rtype: float or None   
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.extensible_size)
           None
           >>> o1=s.get_object('ShadowCalculation')
           >>> print(o1.extensible_size)
           1.0
        
        """
        return self._dict.get('extensible_size',None)
    
    
    @property
    def fields(self):
        """The fields of the schema object.
        
        :returns: The 'legacy_idd' fields list.
        :rtype: list
        
        """
        return self._dict['legacy_idd']['fields']
    
    
    @property
    def format_(self):
        """The format of the schema object.
        
        :returns: The 'format' string, or None if not present.
        :rtype: str or None        
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.format_)
           singleLine
        
        """
        return self._dict.get('format',None)
    
    
    def get_name(self):
        """Returns a name object for the schema object.
        
        :rtype: EPSchemaName or None
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.get_name())
           None
           >>> o1=s.get_object('Building')
           >>> print(o1.get_name())
           EPSchemaName(object_name="Building")
           
        """
        if 'name' in self._dict:
            epsn=EPSchemaName()
            epsn._epso=self
            return epsn
        else:
            return None
    
    
    def get_properties(self):
        """Returns a list of EPSchemaProperty instances for the schema object.
        
        :rtype: list
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.get_properties())
           [EPSchemaProperty(name="version_identifier")]
        
        """
        result=[]
        for regex,obj_dict in self._dict['patternProperties'].items():
            for property_name,property_dict in obj_dict['properties'].items():
                p=self.get_property(property_name)
                result.append(p)
        return result
        
    
    def get_property(self,name):
        """Returns a schema property of the schema object.
        
        :param name: The name of the property.
        :type name: str
        
        :rtype: EPSchemaProperty
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.get_property('version_identifier'))
           EPSchemaProperty(name="version_identifier")
        
        """
        for regex,obj_dict in self._dict['patternProperties'].items():
            if name in obj_dict['properties']:
                epsp=EPSchemaProperty()
                epsp._name=name
                epsp._epso=self
                epsp._pattern_properties_regex=regex
                return epsp
        raise IndexError('Property with the name "%s" does not exist in the schema object "%s".' % (name,self.name))

    
    @property
    def max_properties(self):
        """The maxProperties of the schema object.
        
        :returns: The maxProperties keyword string, or None if not present.
        :rtype: int or None       
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.max_properties)
           1
        
        """
        return self._dict.get('maxProperties',None)
    
    
    @property
    def memo(self):
        """The memo of the schema object.
        
        :returns: The memo string, or None if not present.
        :rtype: str or None     
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.memo)
           Specifies the EnergyPlus version of the IDF file.
        
        """
        return self._dict.get('memo',None)
    
    
    @property
    def min_properties(self):
        """The minProperties of the schema object.
        
        :returns: The minProperties keyword string, or None if not present.
        :rtype: str or None        
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.min_properties)
           None
           >>> o1=s.get_object('Building')
           >>> print(o1.min_properties)
           1
           
        """
        return self._dict.get('minProperties',None)
    
    
    @property
    def name(self):
        """The name of the schema object.
        
        :rtype: str
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.name)
           Version
           
        """
        return self._name
    
    
    @property
    def pattern_properties_regexes(self):
        """The regex terms used in the patternProperties keyword
        
        :rtype: list
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.pattern_properties_regexes)
           ['.*']
           
        """
        return list(self._dict['patternProperties'].keys())
    
    
    @property
    def property_names(self):
        """The property names of the schema object.
        
        :rtype: list
        
        :Example:
        
        .. code-block:: python
               
           >>> from eprun import EPSchema
           >>> s=EPSchema(fp='Energy+.schema.epJSON')
           >>> o=s.get_object('Version')
           >>> print(o.property_names)
           ['version_identifier']
        
        """
        result=[]
        for regex,obj_dict in self._dict['patternProperties'].items():
            for property_name in obj_dict['properties'].keys():
                result.append(property_name)
        return result
        
        
    
    
    