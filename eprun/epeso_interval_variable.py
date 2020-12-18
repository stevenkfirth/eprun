# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd


class EPEsoIntervalVariable():
    """A class for a interval variable recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoIntervalVariable(report_code=%s)' % (self._report_code)

    
    @property
    def _data(self):
        """A dictionary with the variable data.
        
        :rtype: dict
        
        """
        return self._epesose._data['interval_data'][self._report_code]
        
    
    @property
    def _interval_periods(self):
        """The time periods object relating to the variable
        
        :rtype: EPEsoIntervalPeriods
        
        """
        return self._epesose.get_interval_periods()
        
        
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
        index=pd.Index(data=self._interval_periods.get_periods(),
                       name='time_periods')
        column_level_names=('object_name','quantity','unit','value_type')
        
        column=(self.object_name,
                self.quantity,
                self.unit or '-',
                'value')
        
        df=pd.DataFrame(index=index,
                        data=self.values,
                        columns=pd.MultiIndex.from_tuples((column,),
                                                          names=column_level_names))
        return df


    def get_series(self):
        """Returns a pandas series of the interval variable
        
        :rtype: pandas.Series
        
        """
        s=pd.Series(data=self.values,
                    index=self._interval_periods.get_periods(),
                    name=self.summary())
        return s
        
    
    @property
    def object_name(self):
        """The object name of the interval variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['object_name']
    
    
    def plot(self,
             ax=None,
             **kwargs):
        """Plots the interval variable on the supplied axes.
        
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
        """The quantity of the interval variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['quantity']

    
    @property
    def report_code(self):
        """The report code of the interval variable.
        
        :rtype: str
        
        """
        return self._report_code
    
    
    def summary(self):
        """Returns a summary of the interval variable.
        
        :rtype: str
        
        """
        return '%s - %s - %s (%s)' % (self.report_code,
                                      self.object_name, 
                                      self.quantity, 
                                      self.unit or '-')
        
    @property
    def unit(self):
        """The unit of the interval variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['unit']
    
    
    @property
    def values(self):
        """The (mean) values of the interval variable.
        
        :returns: A tuple of floats.
        :rtype: tuple
        
        """
        return tuple(float(x) for x in self._data[0])
 
    
 