# -*- coding: utf-8 -*-

import jsonschema



class EPInputObject():
    """A class representing an EnergyPlus input object in an .idf or .epJSON file.
    
    .. note::
        
       An EPInputObject instance is returned as the result of the 
       `EPInput.get_object` method (or the other access methods in the `EPInput` class).
       It should not be instantiated directly.
    
    """
    
    def __getattr__(self,key):
        """Returns the property value with name = key
        
        :param name: The name of the property.
        :type name: str
        
        :rtype: str or float or int or list or dict or bool
        
        """
        if key in self.property_names:
            return self.get_property_value(key)
        else:
            raise AttributeError('%s' % key)
    
    
    def __getitem__(self,key):
        """Returns the property value with name = key
        
        :param key: The name of the property.
        :type key: str
        
        :rtype: str or float or int or list or dict or bool
        
        """
        return self.get_property_value(key)
        
        
    def __setattr__(self,key,value):
        """Sets the property value with name = key
        
        :param name: The name of the property.
        :type name: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        
        """
        if key in self.property_names:
            return self.set_property_value(key,value)
        else:
            raise AttributeError('%s' % key)
    
    
    def __setitem__(self,key,value):
        """Sets the property value with name = key
        
        :param key: The name of the property.
        :type key: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        
        """
        self.set_property_value(key,value)
        
        
    def __repr__(self):
        ""
        return 'EPInputObject(name="%s")' % self._name
    
    
    @property
    def _dict(self):
        """The json dictionary for the object.
        
        :rtype: dict
        
        """
        return self._epinput._dict[self._object_type][self._name]
    
    
    def _get_schema_property(self,name):
        """Returns the schema property for a property of the object.
        
        :param name: The name of the property.
        :type name: str
        
        rtype: EPSchemaProperty
        
        """
        schema_property=self._schema_object_type.get_property(name)
        return schema_property
    
    
    @property
    def _schema_object_type(self):
        """The EPSchemaObjectType which relates to this object.
        
        """
        return self._schema.get_object_type(self._object_type)
    
    
    @property
    def _schema(self):
        """The schema of the parent EPInput instance.
        
        :raises Exception: If the schema has not been defined for the parent EPInput object.
        
        :rtype: EPSchema
        
        """
        return self._epinput.schema
    

    def _validate_property_name(self,name):
        """Validates the value of a property using the package jsonschema.
        
        :param name: The name of the new or existing property.
        :type name: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        
        :raises: ValueError
        
        """
        schema_object_type=self._schema.get_object_type(self._object_type)
        if not name in schema_object_type.property_names:
            raise ValueError("name '%s' is not a property of object '%s'" % (name,self._name))
        
        
    
    def _validate_property_value(self,name,value):
        """Validates the value of a property using the package jsonschema.
        
        :param name: The name of the new or existing property.
        :type name: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        
        :raises: ValueError
        
        """
        schema_property=self._get_schema_property(name)
        schema_property_json_dict=schema_property._dict
        try:
            jsonschema.validate(value,
                                schema_property_json_dict,
                                jsonschema.Draft4Validator)
        except jsonschema.exceptions.ValidationError as err:
            raise ValueError(str(err).split('\n')[0] + " in property '%s'" % name)
    
    
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
    
    
    @property
    def object_type(self):
        """The object_type of the EPInputObject object.
        
        :rtype: str
        
        """
        return self._object_type
        
    
    def set_property_value(self,name,value,validate=True):
        """Sets the value of a property of the object.
        
        :param name: The name of the new or existing property.
        :type name: str
        :param value: The value of the property. 
        :type value: str or float or int or list or dict or bool
        :param validate: If True, then property name and value are validated 
            against schema. 
        :type validate: bool
        
        :raises: ValueError - if either the property name or the property value is not valid.
        
        """
        
        if validate:
            self._validate_property_name(name)
            self._validate_property_value(name,value)
        
        self._dict[name]=value
        
    

        
    
    