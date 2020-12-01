# -*- coding: utf-8 -*-

import datetime


class EPEsoDailyPeriods():
    """A class for the daily time periods recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoDailyPeriods(sim_env="%s")' % self._epesose.environment_title
    
    
    @property
    def _data(self):
        """The daily period data.
        
        :rtype: tuple
        
        """
        return self._epesose._data['daily_data'][3]
    
    @property
    def cumulative_days_of_simulation(self):
        """The 'cumulative days of simulation' for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[0])
    
    
    @property
    def months(self):
        """The months for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[1])
    
    
    @property 
    def days_of_month(self):
        """The days in the month for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[2])
    
    
    @property 
    def dst_indicators(self):
        """The daylight saving time indicators for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[3])
    

    @property 
    def day_types(self):
        """The day types for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(str(x) for x in self._data[7])
    
    
    def get_start_times(self):
        """Returns the start times for the daily periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        x=zip(self.months,self.days_of_month)
        return tuple(datetime.datetime(2001,m,d,
                                  tzinfo=self._epesose.get_timezone())
                     for m,d in x)
    
    
    def get_end_times(self):
        """Returns the end times for the daily periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        return tuple(start_time+datetime.timedelta(days=1) 
                     for start_time in self.get_start_times())
