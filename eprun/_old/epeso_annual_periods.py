# -*- coding: utf-8 -*-

import datetime


class EPEsoAnnualPeriods():
    """A class for the annual time periods recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoAnnualPeriods(sim_env="%s")' % self._epesose.environment_title
    
    
    @property
    def _data(self):
        """The annual period data.
        
        :rtype: tuple
        
        """
        return self._epesose._data['annual_data'][6]
    
    @property
    def calendar_years_of_simulation(self):
        """The 'calendar year of simulation' for the annual periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[0])
    
    
    def get_start_times(self):
        """Returns the start times for the annual periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        return tuple(datetime.datetime(y,1,1,tzinfo=self._epesose.get_timezone())
                     for y in self.calendar_years_of_simulation)
    
    
    def get_end_times(self):
        """Returns the end times for the annual periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        return tuple(datetime.datetime(y+1,1,1,tzinfo=self._epesose.get_timezone())
                     for y in self.calendar_years_of_simulation)
