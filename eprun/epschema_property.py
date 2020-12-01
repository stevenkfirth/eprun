# -*- coding: utf-8 -*-


class EPSchemaProperty():
    """A class representing a property of a EPSchemaObject.
    """
    
    def __repr__(self):
        ""
        return 'EPSchemaProperty(name="%s")' % (self._name)
    
    @property
    def _dict(self):
        """
        """
        return self._epso._dict['patternProperties'][self._pattern_property_regex][self._name]


    @property
    def name(self):
        """The name of the schema property.
        
        :rtype: str
        
        """
        return self._name