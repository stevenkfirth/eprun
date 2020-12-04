# -*- coding: utf-8 -*-


class EPEpJSONObject():
    """A class representing an object in a EPEpJSON instance.
    
    .. note::
        
       An EPEpJSONObject instance is returned as the result of the 
       EPEpJSONObjectType :py:meth:`~eprun.epepjson_object_type.EPEpJSONObjectType.get_object` function.
       It should not be instantiated directly.
    
    """
    
    def __getattr__(self,name):
        """Returns the property value with name = name
        
        :param name: The name of the property.
        :type name: str
        
        :rtype: str or float or int or list or dict or bool
        
        """
        return self.get_property_value(name)
    
    
    def __getitem__(self,key):
        """Returns the property value with name = key
        
        :param key: The name of the property.
        :type key: str
        
        :rtype: str or float or int or list or dict or bool
        
        """
        return self.get_property_value(key)
    
    
    def __repr__(self):
        ""
        return 'EPEpJSONObject(name="%s")' % self._name
    
    
    @property
    def _dict(self):
        """The json dictionary for the object.
        
        :rtype: dict
        
        """
        return self._epjson_object_type._dict[self._name]
    
    
    def get_property_value(self,name):
        """Returns the values of a property of the object.
        
        :param name: The name of the property.
        :type name: str
        
        :rtype: str or float or int or list or dict or bool
        
        """
        return self._dict[name]
    
    
    @property
    def property_values(self):
        """The values of the properties of the object.
        
        :rtype: dict
        
        """
        return self._dict
        
    
    @property
    def property_names(self):
        """The names of the properties of the object.
        
        :rtype: list
        
        """
        return list(self._dict.keys())
    
    
    @property
    def name(self):
        """The name of the object type.
        
        :rtype: str
        
        """
        return self._name