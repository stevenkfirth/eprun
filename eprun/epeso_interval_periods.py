# -*- coding: utf-8 -*-


import datetime


class EPEsoIntervalPeriods():
    """A class for the interval time periods recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoIntervalPeriods(sim_env="%s")' % self._epesose.environment_title
    
    
    @property
    def _data(self):
        """The interval period data.
        
        :rtype: tuple
        
        """
        return self._epesose._data['interval_data'][2]
    
    @property
    def days_of_simulation(self):
        """The 'day of simulation' values for the interval periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[0])
    
    
    @property
    def months(self):
        """The months for the interval periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[1])
    
    
    @property 
    def days_of_month(self):
        """The days in the month for the interval periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[2])
    
    
    @property 
    def dst_indicators(self):
        """The daylight saving time indicators for the interval periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[3])
    
    
    @property 
    def hours(self):
        """The hours for the interval periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[4])
    
    
    @property 
    def start_minutes(self):
        """The start minutes for the interval periods.
        
        :rtype: tuple
        
        """
        return tuple(int(float(x)) for x in self._data[5]) 
    
    
    @property 
    def end_minutes(self):
        """The end minutes for the interval periods.
        
        :rtype: tuple
        
        """
        return tuple(int(float(x)) for x in self._data[6]) 
    
    
    @property 
    def day_types(self):
        """The day types for the interval periods.
        
        :rtype: tuple
        
        """
        return tuple(str(x) for x in self._data[7])
    
    
    def get_start_times(self):
        """Returns the start times for the interval periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        x=zip(self.months,self.days_of_month,self.hours,self.start_minutes)
        return tuple(datetime.datetime(2001,m,d,h-1,mi,
                                  tzinfo=self._epesose.get_timezone())
                     for m,d,h,mi in x)
    
    
    def get_end_times(self):
        """Returns the end times for the interval periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        start_times=self.get_start_times()
        x=zip(start_times,self.start_minutes,self.end_minutes)
        return tuple(start_time+datetime.timedelta(minutes=end_minute-start_minute) 
                     for start_time,start_minute,end_minute in x)
 