# -*- coding: utf-8 -*-

import datetime
import calendar
import pandas as pd


class EPEsoMonthlyPeriods():
    """A class for the monthly time periods recorded in a EPEsoSimulationEnviroment instance.
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
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[0])
    
    
    def get_end_times(self):
        """Returns the end times for the monthly periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        result=[]
        for start_time in self.get_start_times():
            days_in_month=calendar.monthrange(start_time.year,start_time.month)[1]
            result.append(start_time+datetime.timedelta(days=days_in_month))
        return tuple(result)
    
    
    def get_periods(self):
        """Returns the interval periods as a list of Pandas periods.
        
        :rtype: list
        
        """
        start_times=self.get_start_times()
        period_frequency='1M' 
        return [pd.Period(start_time,period_frequency) for start_time in start_times]   
    
    
    def get_start_times(self):
        """Returns the start times for the monthly periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        x=self.months
        return tuple(datetime.datetime(2001,m,1,tzinfo=self._epesose.get_timezone())
                for m in x)
        

    @property
    def months(self):
        """The months for the monthly periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[1])


    def summary(self):
        """Returns a summary of the interval periods.
        
        :rtype: dict
        
        """
        start_times=self.get_start_times()
        return 'Starts at %s, %s periods @ 1 month intervals' % (start_times[0].isoformat(),
                                                                 len(start_times))
