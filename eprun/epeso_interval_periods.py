# -*- coding: utf-8 -*-


import datetime
import pandas as pd


class EPEsoIntervalPeriods():
    """A class for the interval time periods recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoIntervalPeriods instance is returned as the result of 
       the `get_interval_periods` method.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> env=eso.get_environment('RUN PERIOD 1')
       >>> ip=env.get_interval_periods()
       >>> print(type(ip))
       <class 'eprun.epeso_interval_periods.EPEsoIntervalPeriods'>
       >>> print(ip.get_start_times()[:5])
       (datetime.datetime(2001, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 1, 1, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 1, 2, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 1, 3, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 1, 4, 0, tzinfo=datetime.timezone.utc))
       
    """
    
    def __repr__(self):
        ""
        return 'EPEsoIntervalPeriods()' 
    
    
    @property
    def _data(self):
        """The interval period data.
        
        :rtype: tuple
        
        """
        return self._epesose._data['interval_data'][2]

    
    @property 
    def day_types(self):
        """The day types for the interval periods.
        
        :rtype: tuple (str)
        
        """
        return tuple(str(x) for x in self._data[7])


    @property 
    def days_of_month(self):
        """The days in the month for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[2])
    

    @property
    def days_of_simulation(self):
        """The 'day of simulation' values for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[0])
    
    
    @property 
    def dst_indicators(self):
        """The daylight saving time indicators for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[3])
    
    
    @property 
    def end_minutes(self):
        """The end minutes for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(float(x)) for x in self._data[6]) 
    
    
    def get_end_times(self):
        """Returns the end times for the interval periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        start_times=self.get_start_times()
        x=zip(start_times,self.start_minutes,self.end_minutes)
        return tuple(start_time+datetime.timedelta(minutes=end_minute-start_minute) 
                     for start_time,start_minute,end_minute in x)
 
    
    def get_interval(self):
        """Returns the time interval between periods.
        
        :rtype: datetime.timedelta
        
        """
        return datetime.timedelta(minutes=self.end_minutes[0]-self.start_minutes[0])
        
    
    def get_periods(self):
        """Returns the interval periods as a list of Pandas periods.
        
        :rtype: list (pandas.Period)
        
        """
        start_times=self.get_start_times()
        period_frequency='%sS' % self.get_interval().total_seconds()
        return [pd.Period(start_time,period_frequency) for start_time in start_times]
    
    
    def get_start_times(self):
        """Returns the start times for the interval periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        x=zip(self.months,self.days_of_month,self.hours,self.start_minutes)
        return tuple(datetime.datetime(2001,m,d,h-1,mi,
                                  tzinfo=self._epesose.get_timezone())
                     for m,d,h,mi in x)
    
    
    @property 
    def hours(self):
        """The hours for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[4])
    
    
    @property
    def months(self):
        """The months for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[1])
    
    
    @property 
    def start_minutes(self):
        """The start minutes for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(float(x)) for x in self._data[5]) 
    
    
    def summary(self):
        """Returns a summary of the interval periods.
        
        :rtype: str
        
        """
        start_times=self.get_start_times()
        return 'Starts at %s, %s periods @ %s minute intervals' % (start_times[0].isoformat(),
                                                                  len(start_times),
                                                                  int(self.get_interval().total_seconds()/60))
        
    
    