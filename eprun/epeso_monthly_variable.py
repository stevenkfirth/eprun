# -*- coding: utf-8 -*-


from datetime import datetime


class EPEsoMonthlyVariable():
    """A class for a monthly variable recorded in a EPEsoSimulationEnviroment instance.
    """
        
    def __repr__(self):
        ""
        return 'EPEsoMonthlyVariable(sim_env="%s", report_code=%s)' % (self._epesose.environment_title,
                                                                       self._report_code)
    
    @property
    def _data(self):
        ""
        return self._epesose._data['monthly_data'][self._report_code]
        
        
    @property
    def _variable_dictionary(self):
        ""
        return self._epesose._epeso._variable_dictionary[self._report_code]
    
    
    @property
    def object_name(self):
        """The object name of the monthly variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['object_name']
    
    
    @property
    def quantity(self):
        """The quantity of the monthly variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['quantity']
    
    
    @property
    def unit(self):
        """The unit of the monthly variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['unit']
    
    
    @property
    def values(self):
        """The (mean) values of the monthly variable.
        
        :returns: A tuple of floats.
        :rtype: tuple
        
        """
        return tuple(float(x) for x in self._data[0])


    @property
    def min_values(self):
        """The minimum values of the monthly variable.
        
        :returns: A tuple of floats.
        :rtype: tuple
        
        """
        return tuple(float(x) for x in self._data[1])
    
    
    @property
    def min_days(self):
        """The day numbers for the minimum values of the monthly variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[2])
    
    
    @property
    def min_hours(self):
        """The hour numbers for the minimum values of the monthly variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[3])
    
    
    @property
    def min_minutes(self):
        """The minute numbers for the minimum values of the monthly variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[4])
    
    
    @property
    def max_values(self):
        """The maximum values of the monthly variable.
        
        :returns: A tuple of floats.
        :rtype: tuple
        
        """
        return tuple(float(x) for x in self._data[5])
    
    
    @property
    def max_days(self):
        """The day numbers for the maximum values of the monthly variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[6])
    
    
    @property
    def max_hours(self):
        """The hour numbers for the maximum values of the monthly variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[7])
    
    
    @property
    def max_minutes(self):
        """The minute numbers for the maximum values of the monthly variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[8])
    
    
    def get_min_times(self):
        """Returns the times when the minumum values occur.
        
        :returns: A tuple of datetime.datetime instances.
        :rtype: tuple
        
        """
        month_start_times=self._epesose.get_monthly_periods().get_start_times()
        result=[]
        for month_start_time,min_day,min_hour,min_minute in zip(month_start_times,
                                                                self.min_days,
                                                                self.min_hours,
                                                                self.min_minutes):
            t=datetime.datetime(month_start_time.year,
                                month_start_time.month,
                                min_day,
                                min_hour,
                                min_minute,
                                tzinfo=month_start_time.tzinfo
                                )
            result.append(t)
        return tuple(result)
    
    
    def get_max_times(self):
        """Returns the times when the maximum values occur.
        
        :returns: A tuple of datetime.datetime instances.
        :rtype: tuple
        
        """
        month_start_times=self._epesose.get_monthly_periods().get_start_times()
        result=[]
        for month_start_time,max_day,max_hour,max_minute in zip(month_start_times,
                                                                self.max_days,
                                                                self.max_hours,
                                                                self.max_minutes):
            t=datetime.datetime(month_start_time.year,
                                month_start_time.month,
                                max_day,
                                max_hour,
                                max_minute,
                                tzinfo=month_start_time.tzinfo
                                )
            result.append(t)
        return tuple(result)
