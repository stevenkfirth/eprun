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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    