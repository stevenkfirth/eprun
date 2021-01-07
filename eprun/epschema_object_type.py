# -*- coding: utf-8 -*-

import jsonschema
import collections

from .epschema_property import EPSchemaProperty


class EPSchemaObjectType(collections.abc.Mapping):
    """A class representing an object in a EnergyPlus .schema.epJSON file.
    
    An EPSchemaObectType can act as a dictionary to access its properties and values.
    For example it has the `keys <dict.keys>`, `values <dict.values>` and 
    `items <dict.items>` attributes.
    
    .. note::
        
       An EPSchemaObjectType instance is returned as the result of the 
       `EPSchema.get_object_type` method.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
           
       >>> from eprun import EPSchema
       >>> s=EPSchema(fp='Energy+.schema.epJSON')
       >>> ot=s.get_object_type('Building')
       >>> print(type(ot))
       <class 'eprun.epschema_object_type.EPSchemaObjectType'>
       >>> print(ot)
       EPSchemaObjectType(name="Building")
       >>> print(ot.name)
       Building
       >>> print(ot.get_properties())
       [EPSchemaProperty(name="north_axis"), 
        EPSchemaProperty(name="terrain"), 
        EPSchemaProperty(name="loads_convergence_tolerance_value"), 
        EPSchemaProperty(name="temperature_convergence_tolerance_value"), 
        EPSchemaProperty(name="solar_distribution"), 
        EPSchemaProperty(name="maximum_number_of_warmup_days"), 
        EPSchemaProperty(name="minimum_number_of_warmup_days")]
       >>> print(list(ot.keys()))
       ['patternProperties', 'name', 'legacy_idd', 'type', 'minProperties', 
        'maxProperties', 'memo', 'min_fields']
       >>> print(ot['memo'])
       Describes parameters that are used during the simulation of the building. 
       There are necessary correlations between the entries for this object and 
       some entries in the Site:WeatherStation and Site:HeightVariation objects, 
       specifically the Terrain field.
       
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
        return 'EPSchemaObjectType(name="%s")' % (self.name)
    
    
    @property
    def _dict(self):
        ""
        return self._eps._dict['properties'][self.name]
    
    
    @property
    def dict_(self):
        """The json dictionary for the EPSchemaObjectType.
        
        :rtype: dict 
        
        """
        return self._dict
    
    
    @property
    def legacy_idd_fields(self):
        """The 'legacy_idd' fields of the EPSchemaObjectType.
        
        :rtype: list (str)
        
        """
        return self._dict['legacy_idd']['fields']
    
    
    def get_properties(self):
        """Returns a list of EPSchemaProperty instances for the schema object.
        
        :rtype: list (EPSchemaProperty)
                
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
        
        """
        for regex,obj_dict in self._dict['patternProperties'].items():
            if name in obj_dict['properties']:
                epsp=EPSchemaProperty()
                epsp.__dict__['_name']=name
                epsp.__dict__['_epsot']=self
                epsp.__dict__['_pattern_properties_regex']=regex
                return epsp
        raise IndexError('Property with the name "%s" does not exist in the schema object "%s".' % (name,self.name))

    
    @property
    def name(self):
        """The name of the EPSchemaObjectType.
        
        :rtype: str
        
        """
        return self._name
    
    
    @property
    def pattern_properties_regexes(self):
        """The regex terms used in the 'patternProperties' object.
        
        :rtype: list (str)
        
        """
        return list(self._dict['patternProperties'].keys())
    
    
    @property
    def property_names(self):
        """The names of the EPSchemaProperty objects of the EPSchemaObjectType.
        
        :rtype: list
        
        """
        result=[]
        for regex,obj_dict in self._dict['patternProperties'].items():
            result+=list(obj_dict['properties'].keys())
            #for property_name in obj_dict['properties'].keys():
            #    result.append(property_name)
        return result
        
        
    def validate_property_name(self,property_name):
        """Validates if a EPSchemaProperty name is valid for the EPSchemaObjectType.
        
        :param property_name: The name of the EPSchemaProperty object.
        :type property_name: str
        
        :raises: IndexError - if the property_name does not exist in *self.property_names*

        """
        if not property_name in self.property_names:
            raise IndexError('"%s" is not a property of a "%s" schema object' % (property_name,self.name))
    
    
    def validate_object(self,obj_dict):
        """Validates a .epJSON object against the EPSchemaObjectType.
        
        :param obj_dict: the JSON for the .epJSON object.
        :type obj_dict: dict
        
        :raises: jsonschema.exceptions.ValidationError - if the .epJSON object is not valid
    
        """
        try:
            jsonschema.validate(obj_dict,
                                self._dict,
                                jsonschema.Draft4Validator)
        except jsonschema.exceptions.ValidationError as err:
            raise jsonschema.exceptions.ValidationError(str(err).split('\n')[0]) 
    