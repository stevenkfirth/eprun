# -*- coding: utf-8 -*-

import datetime
import calendar


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
    
    @property
    def months(self):
        """The months for the monthly periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[1])
    
    
    def get_start_times(self):
        """Returns the start times for the monthly periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        x=self.months
        return tuple(datetime.datetime(2001,m,1,tzinfo=self._epesose.get_timezone())
                for m in x)
    
    
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
