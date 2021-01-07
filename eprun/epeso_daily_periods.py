# -*- coding: utf-8 -*-

import datetime
import pandas as pd


class EPEsoDailyPeriods():
    """A class for the daily time periods recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoDailyPeriods instance is returned as the result of 
       the `get_daily_periods` method.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> env=eso.get_environment('RUN PERIOD 1')
       >>> dp=env.get_daily_periods()
       >>> print(type(dp))
       <class 'eprun.epeso_daily_periods.EPEsoDailyPeriods'>
       >>> print(dp.get_start_times()[:5])
       (datetime.datetime(2001, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 2, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 3, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 4, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 5, 0, 0, tzinfo=datetime.timezone.utc))
       
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
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[0])
    
        
    @property 
    def days_of_month(self):
        """The days in the month for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[2])
    

    @property 
    def day_types(self):
        """The day types for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(str(x) for x in self._data[7])


    @property 
    def dst_indicators(self):
        """The daylight saving time indicators for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[3])
    
    
    
    def get_end_times(self):
        """Returns the end times for the daily periods.
        
        :rtype: tuple (datetime.datetime)
        
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
        
        :rtype: list (pandas.Period)
        
        """
        start_times=self.get_start_times()
        period_frequency='%sS' % self.get_interval().total_seconds()
        return [pd.Period(start_time,period_frequency) for start_time in start_times]


    def get_start_times(self):
        """Returns the start times for the daily periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        x=zip(self.months,self.days_of_month)
        return tuple(datetime.datetime(2001,m,d,
                                  tzinfo=self._epesose.get_timezone())
                     for m,d in x)


    @property
    def months(self):
        """The months for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[1])


    def summary(self):
        """Returns a summary of the interval periods.
        
        :rtype: str
        
        """
        start_times=self.get_start_times()
        return 'Starts at %s, %s periods @ 1 day intervals' % (start_times[0].isoformat(),
                                                               len(start_times))
        
