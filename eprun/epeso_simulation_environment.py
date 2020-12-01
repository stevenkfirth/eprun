# -*- coding: utf-8 -*-

from .epeso_annual_periods import EPEsoAnnualPeriods
from .epeso_annual_variable import EPEsoAnnualVariable
from .epeso_daily_periods import EPEsoDailyPeriods
from .epeso_daily_variable import EPEsoDailyVariable
from .epeso_interval_periods import EPEsoIntervalPeriods
from .epeso_interval_variable import EPEsoIntervalVariable
from .epeso_monthly_periods import EPEsoMonthlyPeriods
from .epeso_monthly_variable import EPEsoMonthlyVariable
from .epeso_runperiod_periods import EPEsoRunPeriodPeriods
from .epeso_runperiod_variable import EPEsoRunPeriodVariable

import datetime


class EPEsoSimulationEnviroment():
    """A class representing the results from a simulation environment section of an EnergyPlus .eso file.
    
    
    :Example:
        
    .. code-block:: python
    
       >>> epeso=EPEso(fp=r'files\eplusout.eso')
       >>> se=epeso.get_environments()[0]
       >>> print(se.environment_title)
       DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB
       
      
    """
    
    def __repr__(self):
        ""
        return 'EPEsoSimuationEnvironment("%s")' % self.environment_title
    
    
    @property
    def _data(self):
        """The simulation environment dictionary holding the data.
        
        :rtype: dict   
        
        """
        return self._epeso._data[self._index]
    
    
    @property
    def environment_title(self):
        """The environment title of the simulation environment section.
        
        :rtype: str
        
        """
        return self._data['environment_title']
    
    
    @property
    def latitude(self):
        """The latitude of the simulation environment section.
        
        :returns: The latitude in degrees.
        :rtype: float
        
        """
        return float(self._data['latitude'])
    
    
    @property
    def longitude(self):
        """The longitude of the simulation environment section.
        
        :returns: The longitude in degrees.
        :rtype: float
        
        """
        return float(self._data['longitude'][2])
    
    
    @property
    def time_zone(self):
        """The time zone of the simulation environment section.
        
        :rtype: str
        
        """
        return self._data['time_zone'][3]
    
    
    def get_timezone(self):
        """Returns the time zone as a datetime.timezone instance.
        
        See https://docs.python.org/3/library/datetime.html#timezone-objects
        
        :rtype: datetime.timezone
        """
        return datetime.timezone(datetime.timedelta(hours=float(self.time_zone)))
    
    
    @property
    def elevation(self):
        """The elevation of the simulation environment section.
        
        :returns: The elevation in metres.
        :rtype: float
        
        """
        return float(self._data['elevation'][4])
    
    
    def get_interval_periods(self):
        """Returns the interval time periods.
        
        :rtype: EPEsoIntervalPeriods
        """
        p=EPEsoIntervalPeriods()
        p._epesose=self
        return p
    
    
    def get_daily_periods(self):
        """Returns the daily time periods.
        
        :rtype: EPEsoDailyPeriods
        """
        p=EPEsoDailyPeriods()
        p._epesose=self
        return p
        
    
    def get_monthly_periods(self):
        """Returns the monthly time periods.
        
        :rtype: EPEsoMonthlyPeriods
        """
        p=EPEsoMonthlyPeriods()
        p._epesose=self
        return p
    
    
    def get_run_period_periods(self):
        """Returns the run period time periods.
        
        :rtype: EPEsoRunPeriodPeriods
        """
        p=EPEsoRunPeriodPeriods()
        p._epesose=self
        return p
    
    
    def get_annual_periods(self):
        """Returns the annual time periods.
        
        :rtype: EPEsoAnnualPeriods
        """
        p=EPEsoAnnualPeriods()
        p._epesose=self
        return p
    
    
    def get_interval_variables(self):
        """Return the interval variables.
        
        :rtype: tuple
        
        """
        result=[]
        for report_code in self._data['interval_data']:
            if not report_code==2:
                mv=EPEsoIntervalVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_daily_variables(self):
        """Return the daily variables.
        
        :rtype: tuple
        
        """
        result=[]
        for report_code in self._data['daily_data']:
            if not report_code==3:
                mv=EPEsoDailyVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_monthly_variables(self):
        """Return the monthly variables.
        
        :rtype: tuple
        
        """
        result=[]
        for report_code in self._data['monthly_data']:
            if not report_code==4:
                mv=EPEsoMonthlyVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_run_period_variables(self):
        """Return the run period variables.
        
        :rtype: tuple
        
        """
        result=[]
        for report_code in self._data['run_period_data']:
            if not report_code==5:
                mv=EPEsoRunPeriodVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_annual_variables(self):
        """Return the annual variables.
        
        :rtype: tuple
        
        """
        result=[]
        for report_code in self._data['annual_data']:
            if not report_code==6:
                mv=EPEsoAnnualVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_interval_dataframe_inputs(self):
        """Returns the inputs to create a pandas DataFrame from the interval data.
        
        Use the following code to create a pandas DataFrame:
            
        .. code-block:: python
           
           import pandas as pd
           df=pd.DataFrame(index=[pd.Period(dt,period_frequency) for dt in index],
                           data=data,
                           columns=pd.MultiIndex.from_tuples(columns, 
                                                             names=column_level_names))
        
        :returns: index, period_frequency, data, columns ,column_level_names
        :rtype: tuple
        
        """
    
        index=self.get_interval_periods().get_start_times()
        period_frequency='H'
        column_level_names=('object_name','quantity','unit','value')
        
        data=[]
        columns=[[],[],[],[]]
        
        for dv in self.get_interval_variables():
            
            columns[0]+=[dv.object_name]
            columns[1]+=[dv.quantity]
            columns[2]+=[dv.unit]
            columns[3]+=['value']
        
            data+=[dv.values]
        
        columns=tuple(zip(*columns))
        data=tuple(zip(*data))
        
        return index,period_frequency,data,columns,column_level_names
    
    
    def get_daily_dataframe_inputs(self):
        """Returns the inputs to create a pandas DataFrame from the daily data.
        
        Use the following code to create a pandas DataFrame:
            
        .. code-block:: python
           
           import pandas as pd
           df=pd.DataFrame(index=[pd.Period(dt,period_frequency) for dt in index],
                           data=data,
                           columns=pd.MultiIndex.from_tuples(columns, 
                                                             names=column_level_names))
        
        :returns: index, period_frequency, data, columns ,column_level_names
        :rtype: tuple
        
        """
    
        index=self.get_daily_periods().get_start_times()
        period_frequency='D'
        column_level_names=('object_name','quantity','unit','value')
        
        data=[]
        columns=[[],[],[],[]]
        
        for dv in self.get_daily_variables():
            
            columns[0]+=[dv.object_name]*5
            columns[1]+=[dv.quantity]*5
            columns[2]+=[dv.unit]*5
            columns[3]+=['value','min_value','min_time','max_value','max_time']
        
            data+=[dv.values,
                   dv.min_values,
                   dv.get_min_times(),
                   dv.max_values,
                   dv.get_max_times()]
        
        columns=tuple(zip(*columns))
        data=tuple(zip(*data))
        
        return index,period_frequency,data,columns,column_level_names
    
    
    def get_monthly_dataframe_inputs(self):
        """Returns the inputs to create a pandas DataFrame from the monthly data.
        
        Use the following code to create a pandas DataFrame:
            
        .. code-block:: python
           
           import pandas as pd
           df=pd.DataFrame(index=[pd.Period(dt,period_frequency) for dt in index],
                           data=data,
                           columns=pd.MultiIndex.from_tuples(columns, 
                                                             names=column_level_names))
        
        :returns: index, period_frequency, data, columns ,column_level_names
        :rtype: tuple
        
        """
    
        index=self.get_monthly_periods().get_start_times()
        period_frequency='M'
        column_level_names=('object_name','quantity','unit','value')
        
        data=[]
        columns=[[],[],[],[]]
        
        for mv in self.get_monthly_variables():
            
            columns[0]+=[mv.object_name]*5
            columns[1]+=[mv.quantity]*5
            columns[2]+=[mv.unit]*5
            columns[3]+=['value','min_value','min_time','max_value','max_time']
        
            data+=[mv.values,
                   mv.min_values,
                   mv.get_min_times(),
                   mv.max_values,
                   mv.get_max_times()]
        
        columns=tuple(zip(*columns))
        data=tuple(zip(*data))
        
        return index,period_frequency,data,columns,column_level_names
    
 
