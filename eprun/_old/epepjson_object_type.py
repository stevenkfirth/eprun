# -*- coding: utf-8 -*-

from .epepjson_object import EPEpJSONObject


class EPEpJSONObjectType():
    """A class representing an object type in a EPEpJSON instance.
    
    .. note::
        
       An EPEpJSONObjectType instance is returned as the result of the 
       EPEpJSON :py:meth:`~eprun.epepjson.EPEpJSON.get_object_type` function.
       It should not be instantiated directly.
    
    """
    
    def __getitem__(self,key):
        """Returns the object with name = key
        
        :rtype: EPEpJSONObject
        
        """
        return self.get_object(key)
    
    
    def __repr__(self):
        ""
        return 'EPEpJSONObjectType(name="%s")' % self._name
    
    
    @property
    def _dict(self):
        """The json dictionary for the object type.
        
        :rtype: dict
        
        """
        return self._epjson._dict[self._name]
    
    
    def _get_schema_object(self,schema):
        """Returns the schema object for the object type.
        
        :param schema: The schema for the epJSON file. 
        :type schema: EPSchema
        
        rtype: EPSchemaObject

        """
        return schema.get_object(self.name)
    
    
    def add_object(self,name,schema=None,**properties):
        """Adds an object to the .epJSON file.
        
        :param name: The name of the object. This acts as a unique ID for the object.
        :type name: str
        :param schema: The schema for the epJSON file. 
            Optional. If used then validation will be done on against this schema.
        :type schema: EPSchema
        :param properties: keyword pair values for the properties of the object.
        
        :raises: jsonschema.exceptions.ValidationError - on validation only, if the .epJSON object is not valid against the schema.
        
        :returns: The newly created object.
        :rtype: EPEpJSONObject
        
        .. note::
        
           Schema validation occurs in two cases:
           1. A EPSchema instance is supplied to this method using the ``schema`` argument;
           2. The :py:class:`~eprun.epepjson.EPEpJSON` object was initiated with an EPSchema instance.
        
        """
        
        schema=self._epjson._get_schema(schema)
        if not schema is None: # if a schema is present, then do the validation
            schema_object=schema.get_object(self._name)
            obj_dict={name:properties}
            schema_object.validate_object(obj_dict)
    
        obj_type_dict=self._epjson._dict.setdefault(self._name,{})
        obj_type_dict[name]=properties
        return self.get_object(name)
    
    
    def get_object(self,name):
        """Returns an object in the epJSON object type. 
        
        :param name: The name of the object.
        :type name: str
        
        :rtype: EPEpJSONObject
        
        """
        o=EPEpJSONObject()
        o.__dict__['_epjson_object_type']=self
        o.__dict__['_name']=name
        return o    
    
    
    def remove_object(self,name):
        """Removes an object from the .epJSON file.
        
        :param name: The name of the object.
        :type name: str
        
        """
        
        del self._dict[name]
        
        # removes the object_type if it is now empty
        if not self._dict:
            self._epjson.remove_object_type(self._name)
    
    
    def get_objects(self):
        """Returns the objects in the .epJSON file.
    
        :rtype: list
        
        """
        return [self.get_object(x) for x in self.object_names]
    
    
    @property
    def object_names(self):
        """The object names in the epJSON object type.
        
        :rtype: list  

        """
        return list(self._dict.keys())
    
    
    @property
    def name(self):
        """The name of the object type.
        
        :rtype: str
        
        """
        return self._name
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    