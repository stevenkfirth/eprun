# -*- coding: utf-8 -*-

import datetime
import pandas as pd


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
    def days_of_month(self):
        """The days in the month for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[2])
    

    @property 
    def day_types(self):
        """The day types for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(str(x) for x in self._data[7])


    @property 
    def dst_indicators(self):
        """The daylight saving time indicators for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[3])
    
    
    
    def get_end_times(self):
        """Returns the end times for the daily periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        return tuple(start_time+datetime.timedelta(days=1) 
                     for start_time in self.get_start_times())


    def get_interval(self):
        """Returns the time interval between periods.
        
        :rtype: datetime.timedelta
        
        """
        return datetime.timedelta(days=1)
        


    def get_periods(self):
        """Returns the interval periods as a list of Pandas periods.
        
        :rtype: list
        
        """
        start_times=self.get_start_times()
        period_frequency='%sS' % self.get_interval().total_seconds()
        return [pd.Period(start_time,period_frequency) for start_time in start_times]


    def get_start_times(self):
        """Returns the start times for the daily periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        x=zip(self.months,self.days_of_month)
        return tuple(datetime.datetime(2001,m,d,
                                  tzinfo=self._epesose.get_timezone())
                     for m,d in x)
    

    @property
    def months(self):
        """The months for the daily periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[1])


    def summary(self):
        """Returns a summary of the interval periods.
        
        :rtype: dict
        
        """
        start_times=self.get_start_times()
        return 'Starts at %s, %s periods @ 1 day intervals' % (start_times[0].isoformat(),
                                                               len(start_times))
        
