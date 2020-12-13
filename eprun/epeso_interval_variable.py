# -*- coding: utf-8 -*-



class EPEsoIntervalVariable():
    """A class for a interval variable recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoIntervalVariable(sim_env="%s", report_code=%s)' % (self._epesose.environment_title,
                                                                       self._report_code)
    
    @property
    def _data(self):
        ""
        return self._epesose._data['interval_data'][self._report_code]
        
        
    @property
    def _variable_dictionary(self):
        ""
        return self._epesose._epeso._variable_dictionary[self._report_code]
    
    
    @property
    def object_name(self):
        """The object name of the interval variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['object_name']
    
    
    @property
    def quantity(self):
        """The quantity of the interval variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['quantity']
    
    @property
    def report_code(self):
        """The report code of the interval variable.
        
        :rtype: str
        
        """
        return self._report_code
    
    
    @property
    def unit(self):
        """The unit of the interval variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['unit']
    
    
    @property
    def values(self):
        """The (mean) values of the interval variable.
        
        :returns: A tuple of floats.
        :rtype: tuple
        
        """
        return tuple(float(x) for x in self._data[0])
 