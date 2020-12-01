# -*- coding: utf-8 -*-


class EPSchemaName():
    """A class representing a name property of a EPSchemaObject.
    """
    
    def __repr__(self):
        ""
        return 'EPSchemaName(object_name="%s")' % (self._epso.name)
    
    @property
    def _dict(self):
        """
        """
        return self._epso._dict['name']
    
    @property
    def data_type(self):
        """
        """
        return
    
    @property
    def default(self):
        """
        """
        return
    
    @property
    def is_required(self):
        """
        """
        return
    
    @property
    def note(self):
        """
        """
        return
    
    @property
    def object_list(self):
        """
        """
        return
    
    @property
    def reference(self):
        """
        """
        return
    
    @property
    def reference_class_name(self):
        """
        """
        return
    
    @property
    def retaincase(self):
        """
        """
        return
