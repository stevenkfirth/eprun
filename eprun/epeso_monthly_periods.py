# -*- coding: utf-8 -*-

import datetime
import calendar
import pandas as pd


class EPEsoMonthlyPeriods():
    """A class for the monthly time periods recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoMonthlyPeriods instance is returned as the result of 
       the `get_monthly_periods` function.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> env=eso.get_environment('RUN PERIOD 1')
       >>> mp=env.get_monthly_periods()
       >>> print(type(mp))
       <class 'eprun.epeso_monthly_periods.EPEsoMonthlyPeriods'>
       >>> print(mp.get_start_times()[:5])
       (datetime.datetime(2001, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 2, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 3, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 4, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 5, 1, 0, 0, tzinfo=datetime.timezone.utc))
       
    """
    
    def __repr__(self):
        ""
        return 'EPEsoMonthlyPeriods(sim_env="%s")' % self._epesose.environment_title
    
    
    @property
    def _data(self):
        """The monthly period data.
        
        :rtype: tuple
        
        """
        return self._epesose._data['monthly_data'][4]
    
    @property
    def cumulative_days_of_simulation(self):
        """The 'cumulative days of simulation' for the monthly periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[0])
    
    
    def get_end_times(self):
        """Returns the end times for the monthly periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        result=[]
        for start_time in self.get_start_times():
            days_in_month=calendar.monthrange(start_time.year,start_time.month)[1]
            result.append(start_time+datetime.timedelta(days=days_in_month))
        return tuple(result)
    
    
    def get_periods(self):
        """Returns the monthly periods as a list of Pandas periods.
        
        :rtype: list (pandas.Period)
        
        """
        start_times=self.get_start_times()
        period_frequency='1M' 
        return [pd.Period(start_time,period_frequency) for start_time in start_times]   
    
    
    def get_start_times(self):
        """Returns the start times for the monthly periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        x=self.months
        return tuple(datetime.datetime(2001,m,1,tzinfo=self._epesose.get_timezone())
                for m in x)
        

    @property
    def months(self):
        """The months for the monthly periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[1])


    def summary(self):
        """Returns a summary of the monthly periods.
        
        :rtype: str
        
        """
        start_times=self.get_start_times()
        return 'Starts at %s, %s periods @ 1 month intervals' % (start_times[0].isoformat(),
                                                                 len(start_times))
