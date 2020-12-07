# -*- coding: utf-8 -*-

import jsonschema



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
        if name.startswith('_'):
            raise Exception()
        return self.get_property_value(name)
    
    
    def __setattr__(self,name,value):
        """Sets the property value with name = name
        
        :param name: The name of the property.
        :type name: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        
        """
        
        
        
        #return self.set_property_value(name,value)
    
    
    def __getitem__(self,key):
        """Returns the property value with name = key
        
        :param key: The name of the property.
        :type key: str
        
        :rtype: str or float or int or list or dict or bool
        
        """
        return self.get_property_value(key)
    
    
    def __setitem__(self,key,value):
        """Sets the property value with name = key
        
        :param key: The name of the property.
        :type key: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        
        """
        return self.set_property_value(key,value)
    
    
    def __repr__(self):
        ""
        return 'EPEpJSONObject(name="%s")' % self._name
    
    
    @property
    def _dict(self):
        """The json dictionary for the object.
        
        :rtype: dict
        
        """
        return self._epjson_object_type._dict[self._name]
    
    
    def _get_schema_property(self,name,schema):
        """Returns the schema property for a property of the object.
        
        :param name: The name of the property.
        :type name: str
        :param schema: The schema for the epJSON file. 
        :type schema: EPSchema
        
        rtype: EPSchemaProperty
        
        """
        schema_object=self._epjson_object_type._get_schema_object(schema)
        schema_property=schema_object.get_property(name)
        return schema_property
    
    
    @property
    def _schema(self):
        """The schema of the parent EPEpJSON instance.
        
        :rtype: EPSchema or None
        
        """
        return self._epjson_object_type._epjson._schema
    
    
    def _validate_property_value(self,name,value,schema):
        """Validates the value of a property using the package jsonschema.
        
        :param name: The name of the new or existing property.
        :type name: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        :param schema: The schema for the epJSON file. 
        :type schema: EPSchema
        
        :raises: jsonschema.exceptions.ValidationError
        
        """
        schema_property=self._get_schema_property(name,schema)
        schema_property_json_dict=schema_property._dict
        jsonschema.validate(value,
                            schema_property_json_dict,
                            jsonschema.Draft4Validator)
    
    
    def get_property_value(self,name):
        """Returns the value of a property of the object.
        
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
        """The name of the object.
        
        :rtype: str
        
        """
        return self._name
    
    
    def set_property_value(self,name,value,schema=None):
        """Sets the value of a property of the object.
        
        :param name: The name of the new or existing property.
        :type name: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        :param schema: The schema for the epJSON file. 
            Optional. If used then validation will be done on the 
            property name and the property value.
        :type schema: EPSchema
        
        :returns: None
        
        .. note::
        
           When setting a property value, the value can be validated against a JSON schema.
           Schema validation occurs in two cases:
           1. A EPSchema instance is supplied to this method using the `schema` argument;
           2. The parent :py:class:`~eprun.epepjson.EPEpJSON` class was initiated with an EPSchema instance.
        
        """
        
        # if schema is not supplied, look to see if the EPEpJSON instance has a schema
        if schema is None:
            schema=self._schema # if the EPEpJSON instance does not have a schema then this is set to None.
        
        if not schema is None:
            self._validate_property_value(name,value,schema)
            
        self._dict[name]=value
        
    
    
        
    
    