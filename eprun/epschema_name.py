# -*- coding: utf-8 -*-


class EPSchemaName():
    """A class representing a name object of a EPSchemaObject.
    
    .. note::
        
       An EPSchemaName instance is returned as the result of the 
       EPSchemaObject :py:meth:`~eprun.epschema_object.EPSchemaObject.get_name` function.
       It should not be instantiated directly.
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPSchema
       >>> s=EPSchema(fp='Energy+.schema.epJSON')
       >>> o=s.get_object('Building')
       >>> n=o.get_name()
       >>> print(n)
       EPSchemaName(object_name="Building")
       >>> print(n.default)
       NONE
       >>> print(o=n.retaincase)
       True
    
    """
    
    def __repr__(self):
        ""
        return 'EPSchemaName(object_name="%s")' % (self._epso.name)
    
    @property
    def _dict(self):
        """Returns the json dict of the name object
        """
        return self._epso._dict['name']
    
    @property
    def data_type(self):
        """The data type property of the name object.
        
        :returns: The 'data_type' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('data_type',None)
    
    @property
    def default(self):
        """The default property of the name object.
        
        :returns: The 'default' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('default',None)
    
    
    @property
    def is_required(self):
        """The is_required property of the name object.
        
        :returns: The 'is_required' boolean, or None if not present.
        :rtype: bool or None
        
        """
        return self._dict.get('is_required',None)
    
    
    @property
    def note(self):
        """The note property of the name object.
        
        :returns: The 'note' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('note',None)
    
    
    @property
    def object_list(self):
        """The object_list property of the name object.
        
        :returns: The 'object_list' string, or None if not present.
        :rtype: str or None
        
        """
        return self._dict.get('object_list',None)
    
    
    @property
    def reference(self):
        """The reference property of the name object.
        
        :returns: The 'reference' list, or None if not present.
        :rtype: list or None
        
        """
        return self._dict.get('reference',None)
    
    
    @property
    def reference_class_name(self):
        """The reference_class_name of the name object.
        
        :returns: The 'reference-class-name' list, or None if not present.
        :rtype: list or None
        
        """
        return self._dict.get('reference-class-name',None)
    
    
    @property
    def retaincase(self):
        """The retaincase property of the name object.
        
        :returns: The 'retaincase' boolean, or None if not present.
        :rtype: bool or None
        
        """
        return self._dict.get('retaincase',None)
