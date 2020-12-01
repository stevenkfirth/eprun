# -*- coding: utf-8 -*-

import datetime


class EPEsoRunPeriodPeriods():
    """A class for the run period time periods recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoRunPeriodPeriods(sim_env="%s")' % self._epesose.environment_title
    
    
    @property
    def _data(self):
        """The run period period data.
        
        :rtype: tuple
        
        """
        return self._epesose._data['run_period_data'][5]
    
    @property
    def cumulative_days_of_simulation(self):
        """The 'cumulative days of simulation' for the run period periods.
        
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[0])
    
    
    def get_start_times(self):
        """Returns the start times for the run period periods.
        
        :returns: A tuple of datetime.datetime instances
        :rtype: tuple
        
        """
        return tuple(datetime.datetime(2001,1,1,tzinfo=self._epesose.get_timezone())+
                     datetime.timedelta(days=d-1)
                     for d in self.cumulative_days_of_simulation)
    