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
import pandas as pd


class EPEsoSimulationEnvironment():
    """A class representing the results from a simulation environment section 
    of an `EPEso` instance.
    
    .. note::
        
       An EPEsoSimulationEnvironment instance is returned as the result of 
       the `get_environment` or `get_environments` methods.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(fp=r'files\eplusout.eso')
       >>> envs=eso.get_environments()
       [EPEsoSimuationEnvironment(environment_title="DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB"),
        EPEsoSimuationEnvironment(environment_title="DENVER CENTENNIAL  GOLDEN   N ANN CLG 1% CONDNS DB=>MWB"),
        EPEsoSimuationEnvironment(environment_title="RUN PERIOD 1")]
       >>> print(envs[0].environment_title)
       DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB
       
    """
    
    def __repr__(self):
        ""
        return 'EPEsoSimuationEnvironment(environment_title="%s")' % self.environment_title
    
    
    @property
    def _data(self):
        """The simulation environment dictionary holding the data.
        
        :rtype: dict   
        
        """
        return self._epeso._data[self._index]
    
        
    @property
    def elevation(self):
        """The elevation of the simulation environment section.
        
        :returns: The elevation in metres.
        :rtype: float
        
        """
        return float(self._data['elevation'])
    
        
    @property
    def environment_title(self):
        """The environment title of the simulation environment section.
        
        :rtype: str
        
        """
        return self._data['environment_title']


    def get_annual_dataframe(self):
        """Returns a pandas DataFrame from the annual data.
        
        :rtype: pandas.DataFrame
        
        """
        
    
    def get_annual_periods(self):
        """Returns the annual time periods.
        
        :rtype: EPEsoAnnualPeriods
        
        """
        p=EPEsoAnnualPeriods()
        p._epesose=self
        return p
    
    
    def get_annual_summary(self):
        """Returns a summary of the annual periods and variables.
        
        :rtype: str
        
        """
        return ''
        #return '--- TO DO ---'
    

    def get_annual_variables(self):
        """Return the annual variables.
        
        :rtype: tuple (EPEsoAnnualVariable)
        
        """
        result=[]
        for report_code in self._data['annual_data']:
            if not report_code==6:
                mv=EPEsoAnnualVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_annual_variable(self,report_code):
        """
        """
    
    
    def get_daily_dataframe(self):
        """Returns a pandas DataFrame from the daily data.
        
        :rtype: pandas.DataFrame
        
        """
    
        index=pd.Index(data=self.get_daily_periods().get_periods(),
                       name='time_periods')
        column_level_names=('object_name','quantity','unit','value_type')
        
        data=[]
        columns=[[],[],[],[]]
        
        for dv in self.get_daily_variables():
            
            columns[0]+=[dv.object_name]*5
            columns[1]+=[dv.quantity]*5
            columns[2]+=[dv.unit or '-']*5
            columns[3]+=['value','min_value','min_time','max_value','max_time']
        
            data+=[dv.values,
                   dv.min_values,
                   dv.get_min_times(),
                   dv.max_values,
                   dv.get_max_times()]
        
        columns=tuple(zip(*columns))
        data=tuple(zip(*data))
        
        df=pd.DataFrame(index=index,
                        data=data,
                        columns=pd.MultiIndex.from_tuples(columns,
                                                          names=column_level_names))
        return df


    def get_daily_periods(self):
        """Returns the daily time periods.
        
        :rtype: EPEsoDailyPeriods
        
        """
        p=EPEsoDailyPeriods()
        p._epesose=self
        return p


    def get_daily_summary(self):
        """Returns a summary of the daily periods and variables.
        
        :rtype: str
        
        """
        result=[]
        result.append(self.get_daily_periods().summary())
        
        for v in self.get_daily_variables():
            result.append(v.summary())
                    
        return '\n'.join(result)
    
    
    def get_daily_variables(self):
        """Return the daily variables.
        
        :rtype: tuple (EPEsoDailyVariable)
        
        """
        result=[]
        for report_code in self._data['daily_data']:
            if not report_code==3:
                mv=EPEsoDailyVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_daily_variable(self,report_code):
        """Return a daily variable.
        
        :param report_code: The report code of the variable.
        :type report_code: int
        
        :raises KeyError: If a daily variable with the report code does not exist.
        
        :rtype: EPEsoDailyVariable

        """ 
        if report_code in self._data['daily_data']:
        
            v=EPEsoDailyVariable()
            v._epesose=self
            v._report_code=report_code
            return v        
        
        else:
            
            raise KeyError('Report code %s does not match any interval variables.' % (report_code))
        

    def get_interval_dataframe(self):
        """Returns a pandas DataFrame from the interval data.
        
        :rtype: pandas.DataFrame
        
        """
        index=pd.Index(data=self.get_interval_periods().get_periods(),
                       name='time_periods')
        column_level_names=('object_name','quantity','unit','value_type')
        
        data=[]
        columns=[[],[],[],[]]
        
        for dv in self.get_interval_variables():
            
            columns[0]+=[dv.object_name]
            columns[1]+=[dv.quantity]
            columns[2]+=[dv.unit or '-']
            columns[3]+=['value']
        
            data+=[dv.values]
        
        columns=tuple(zip(*columns))
        data=tuple(zip(*data))
        
        df=pd.DataFrame(index=index,
                        data=data,
                        columns=pd.MultiIndex.from_tuples(columns,
                                                          names=column_level_names))
        return df

    
    def get_interval_periods(self):
        """Returns the interval time periods.
        
        :rtype: EPEsoIntervalPeriods
        
        """
        p=EPEsoIntervalPeriods()
        p._epesose=self
        return p
    
    
    def get_interval_summary(self):
        """Returns a summary of the interval periods and variables.
        
        :rtype: str
        
        """
        result=[]
        result.append(self.get_interval_periods().summary())
        
        for v in self.get_interval_variables():
            result.append(v.summary())
                    
        return '\n'.join(result)


    def get_interval_variable(self,
                              report_code):
        """Return an interval variable.
        
        :param report_code: The report code of the variable.
        :type report_code: int
        
        :raises KeyError: If an interval variable with the report code does not exist.
        
        :rtype: EPEsoIntervalVariable

        """ 
        if report_code in self._data['interval_data']:
        
            v=EPEsoIntervalVariable()
            v._epesose=self
            v._report_code=report_code
            return v        
        
        else:
            
            raise KeyError('Report code %s does not match any interval variables.' % (report_code))
        
    
    def get_interval_variables(self):
        """Return the interval variables.
        
        :rtype: tuple (EPEsoIntervalVariable)
        
        """
        result=[]
        for report_code in self._data['interval_data']:
            if not report_code==2:
                v=EPEsoIntervalVariable()
                v._epesose=self
                v._report_code=report_code
                result.append(v)
        return result
    
    
    def get_monthly_dataframe(self):
        """Returns a pandas DataFrame from the monthly data.
        
        :rtype: pandas.DataFrame
        
        """
        index=pd.Index(data=self.get_monthly_periods().get_periods(),
                       name='time_periods')
        column_level_names=('object_name','quantity','unit','value_type')
        
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
        
        df=pd.DataFrame(index=index,
                        data=data,
                        columns=pd.MultiIndex.from_tuples(columns,
                                                          names=column_level_names))
        
        return df
    
    
    def get_monthly_periods(self):
        """Returns the monthly time periods.
        
        :rtype: EPEsoMonthlyPeriods
        
        """
        p=EPEsoMonthlyPeriods()
        p._epesose=self
        return p
    
    
    def get_monthly_summary(self):
        """Returns a summary of the monthly periods and variables.
        
        :rtype: str
        
        """
        result=[]
        result.append(self.get_monthly_periods().summary())
        
        for v in self.get_monthly_variables():
            result.append(v.summary())
                    
        return '\n'.join(result)

    
    def get_monthly_variables(self):
        """Return the monthly variables.
        
        :rtype: tuple (EPEsoMonthlyVariable)
        
        """
        result=[]
        for report_code in self._data['monthly_data']:
            if not report_code==4:
                mv=EPEsoMonthlyVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_monthly_variable(self,report_code):
        """Return a monthly variable.
        
        :param report_code: The report code of the variable.
        :type report_code: int
        
        :raises KeyError: If a monthly variable with the report code does not exist.
        
        :rtype: EPEsoMonthlyVariable

        """ 
        if report_code in self._data['monthly_data']:
        
            v=EPEsoMonthlyVariable()
            v._epesose=self
            v._report_code=report_code
            return v        
        
        else:
            
            raise KeyError('Report code %s does not match any monthly variables.' % (report_code))
        
    
    def get_number_of_variables(self):
        """Returns all the number of variables in the simulation environment.
        
        :returns: A dictionary with keys as the different variable intervals
            and values as the number of variables.
        :rtype: dict (str,int)
        
        """
        return {'interval':len(self.get_interval_variables()),
                'daily':len(self.get_daily_variables()),
                'monthly':len(self.get_monthly_variables()),
                'runperiod':len(self.get_run_period_variables()),
                'annual':len(self.get_annual_variables())}

        
    def get_run_period_dataframe(self):
        """
        
        """
    
    
    def get_run_period_periods(self):
        """Returns the run period time periods.
        
        :rtype: EPEsoRunPeriodPeriods
        
        """
        p=EPEsoRunPeriodPeriods()
        p._epesose=self
        return p
    
    
    def get_run_period_summary(self):
        """
        
        """
        return ''
        #return '--- TO DO ---'
    
    
    def get_run_period_variables(self):
        """Return the run period variables.
        
        :rtype: tuple (EPEsorunPeriodVariable)
        
        """
        result=[]
        for report_code in self._data['run_period_data']:
            if not report_code==5:
                mv=EPEsoRunPeriodVariable()
                mv._epesose=self
                mv._report_code=report_code
                result.append(mv)
        return tuple(result)
    
    
    def get_run_period_variable(self):
        """
        
        """
    
    
    def get_timezone(self):
        """Returns the time zone as a datetime.timezone instance.
        
        :rtype: datetime.timezone
        
        """
        return datetime.timezone(datetime.timedelta(hours=float(self.time_zone)))
    

    def get_variables(self):
        """Returns all the variables in the simulation environment.
        
        :returns: A dictionary with keys as the different variable intervals
            and values as the interval objects.
        :rtype: dict(str,list)
        
        """
        return {'interval':self.get_interval_variables(),
                'daily':self.get_daily_variables(),
                'monthly':self.get_monthly_variables(),
                'runperiod':self.get_run_period_variables(),
                'annual':self.get_annual_variables()}

        
    
    
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
    
    
    
    def summary(self):
        """Returns a summary of the all periods and variables in the simulation environment.
        
        :rtype: str
        
        """
        return '\n'.join(['INTERVAL DATA',
                          self.get_interval_summary(),
                          'DAILY DATA',
                          self.get_daily_summary(),
                          'MONTHLY DATA',
                          self.get_monthly_summary(),
                          'RUN PERIOD DATA',
                          self.get_run_period_summary(),
                          'ANNUAL DATA',
                          self.get_annual_summary()
                          ])
        
        
    
    
    @property
    def time_zone(self):
        """The time zone of the simulation environment section.
        
        :rtype: str
        
        """
        return self._data['time_zone'][3]
    
    
    
    
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
