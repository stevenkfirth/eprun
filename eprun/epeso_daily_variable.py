# -*- coding: utf-8 -*-

import datetime
import matplotlib.pyplot as plt
import pandas as pd


class EPEsoDailyVariable():
    """A class for a daily variable recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoDailyVariable(report_code=%s)' % (self._report_code)
    
    
    @property
    def _data(self):
        """A dictionary with the variable data.
        
        :rtype: dict
        
        """
        return self._epesose._data['daily_data'][self._report_code]
        
    
    @property
    def _daily_periods(self):
        """The time periods object relating to the variable
        
        :rtype: EPEsoDailyPeriods
        
        """
        return self._epesose.get_daily_periods()
    
        
    @property
    def _variable_dictionary(self):
        """A dictionary with the variable data dicionary data
        
        :rtype: dict
        
        """
        return self._epesose._epeso._variable_dictionary[self._report_code]
    
    
    def get_dataframe(self):
        """Returns a pandas dataframe of the interval variable.
        
        :rtype: pandas.DataFrame
        
        """
        index=pd.Index(data=self._daily_periods.get_periods(),
                       name='time_periods')
        column_level_names=('object_name','quantity','unit','value_type')
        
        data=[self.values,
              self.min_values,
              self.get_min_times(),
              self.max_values,
              self.get_max_times()]
        columns=[[self.object_name]*5,
                 [self.quantity]*5,
                 [self.unit or '-']*5,
                 ['value','min_value','min_time','max_value','max_time']]
        
        columns=tuple(zip(*columns))
        data=tuple(zip(*data))
        
        df=pd.DataFrame(index=index,
                        data=data,
                        columns=pd.MultiIndex.from_tuples(columns,
                                                          names=column_level_names))
        return df


    def get_max_times(self):
        """Returns the times when the maximum values occur.
        
        :returns: A tuple of datetime.datetime instances.
        :rtype: tuple
        
        """
        day_start_times=self._epesose.get_daily_periods().get_start_times()
        result=[]
        for day_start_time,max_hour,max_minute in zip(day_start_times,
                                                      self.max_hours,
                                                      self.max_minutes):
            t=datetime.datetime(day_start_time.year,
                                day_start_time.month,
                                day_start_time.day,
                                max_hour-1,
                                max_minute-1,
                                tzinfo=day_start_time.tzinfo
                                )
            result.append(t)
        return tuple(result)
    
    
    def get_min_times(self):
        """Returns the times when the minumum values occur.
        
        :returns: A tuple of datetime.datetime instances.
        :rtype: tuple
        
        """
        day_start_times=self._epesose.get_daily_periods().get_start_times()
        result=[]
        for day_start_time,min_hour,min_minute in zip(day_start_times,
                                                      self.min_hours,
                                                      self.min_minutes):
            t=datetime.datetime(day_start_time.year,
                                day_start_time.month,
                                day_start_time.day,
                                min_hour-1,
                                min_minute-1,
                                tzinfo=day_start_time.tzinfo
                                )
            result.append(t)
        return tuple(result)
    
    
    @property
    def max_hours(self):
        """The hour numbers for the maximum values of the daily variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[5])
    
    
    @property
    def max_minutes(self):
        """The minute numbers for the maximum values of the daily variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[6])
    
    
    @property
    def max_values(self):
        """The maximum values of the monthly variable.
        
        :returns: A tuple of floats.
        :rtype: tuple
        
        """
        return tuple(float(x) for x in self._data[4])
    
    
    @property
    def min_hours(self):
        """The hour numbers for the minimum values of the daily variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[2])


    @property
    def min_minutes(self):
        """The minute numbers for the minimum values of the daily variable.
        
        :returns: A tuple of ints.
        :rtype: tuple
        
        """
        return tuple(int(x) for x in self._data[3])
    
        
    @property
    def min_values(self):
        """The minimum values of the daily variable.
        
        :returns: A tuple of floats.
        :rtype: tuple
        
        """
        return tuple(float(x) for x in self._data[1])
    
        
    @property
    def object_name(self):
        """The object name of the daily variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['object_name']
    
    
    def plot(self,
             ax=None,
             **kwargs):
        """Plots the daily variable values on the supplied axes.
        
        :param ax: An Axes instance.
        :type ax: matplotlib.axes.Axes
        :param kwargs: Keyword arguments to be supplied to the matplotlib plot call.
        
        """
        if not ax:
            fig, ax = plt.subplots(figsize=(16,4))
        
        ax.plot(self.values)
        ax.set_title('%s' % (self.summary()))
        ax.set_ylabel('%s' % (self.unit))
        
        return ax
    
        
    @property
    def quantity(self):
        """The quantity of the daily variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['quantity']


    @property
    def report_code(self):
        """The report code of the daily variable.
        
        :rtype: str
        
        """
        return self._report_code
    
    
    def summary(self):
        """Returns a summary of the daily variable.
        
        :rtype: str
        
        """
        return '%s - %s - %s (%s)' % (self.report_code,
                                      self.object_name, 
                                      self.quantity, 
                                      self.unit or '-')
    
    
    @property
    def unit(self):
        """The unit of the daily variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['unit']
    
    
    @property
    def values(self):
        """The (mean) values of the daily variable.
        
        :returns: A tuple of floats.
        :rtype: tuple
        
        """
        return tuple(float(x) for x in self._data[0])
    
    
    
    
    
    
    
    
    