# -*- coding: utf-8 -*-

import datetime


class EPEso():
    """A class for an EnergyPlus .ese file.
    
    :param fp: The filepath for the .eso file.
    :type fp: str
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPEso
       >>> e=EPEso(fp='eplusout.eso')
       >>> print()
       
    .. seealso::
    
       Output Details and Examples, page 126.
       https://energyplus.net/quickstart
    
    """        
        
    def __init__(self,fp):
        ""
        
        eodd_flag=False # End of Data Dictionary flag, if True has occurred
        eod_flag=False # End of Data flag, if True has occurred
        
        data_dictionary={} 
        data=[]
        environment_data={}
        
        with open(fp,'r') as f:
            
            programme_version_statement=f.readline()
            
            while not eod_flag:
                            
                line=f.readline()
                
                if eodd_flag: # data section
                    
                    if line.startswith('End of Data'): # end of the data section
                    
                        eod_flag=True
                
                    else: # not the end of the data section
                        
                        report_code,items=self._parse_data_line(line)
                        
                        if report_code==1: # new environment section
                            
                            environment_data={'environment':items,
                                              'frequency':{}
                                              }
                            data.append(environment_data)
                            
                            
                        else:
                            
                            if report_code>=2 and report_code<=6: # new interval section
                            
                                frequency_data=environment_data['frequency'].setdefault(report_code,{})
                                
                            interval_data=frequency_data.setdefault(report_code,[])
                            interval_data.append(items)
                    
                else: # data dictionary section
                    
                    if line.startswith('End of Data Dictionary'):
                        eodd_flag=True
                        
                    else:
                        report_code,items=self._parse_data_dictionary_line(line)
                        data_dictionary[report_code]=items
        
        
        self._programme_version_statement=programme_version_statement
        self._data_dictionary=data_dictionary
        
        # zip the interval data
        for env in data:
            for frequency_data in env['frequency'].values():
                for report_code,interval_data in frequency_data.items():
                    a=tuple(zip(*interval_data))
                    frequency_data[report_code]=a
        
        self._data=data
    
    
    @staticmethod
    def _parse_data_line(line):
        """Parses a data line in the .eso file.
        
        :param line: A line of text in the .eso file from the data section.
        :type line: str
        
        :returns: A tuple with (report_code,items) where the report code
            is the first item in the row, and items is a list of the remaining
            items in the row. Numeric items are converted to integers and floats.
        :rtype: tuple
        
        """
        a=line.split('\n')[0] # remove characters inc. and after an exclamation mark
        b=a.split(',') # split by commas
        
        report_code=int(b[0])
        items=b[1:]
        
        if report_code==1:
            items=[items[0]]+[float(x) for x in items[1:]]
        elif report_code==2:
            items=[int(x) for x in items[0:5]]+[float(x) for x in items[5:7]]+[items[7]]
        elif report_code==3:
            items=[int(x) for x in items[0:4]]+[items[4]]
        else:
            items=[float(x) for x in items]
            
        return report_code,items
    
    
    @staticmethod
    def _parse_data_dictionary_line(line):
        """Parses a data dictionary line in the .eso file.
        
        :param line: A line of text in the .eso file from the data dictionary.
        :type line: str
        
        :returns: A tuple with (report_code,items) where the report code
            is the first item in the row, and items is a list of the remaining
            items in the row. Numeric items are converted to integers and floats.
        :rtype: tuple
        
        """
        a=line.split('!')[0] # remove characters inc. and after an exclamation mark
        b=a.split(',') # split by commas
        
        report_code=int(b[0])
        number_of_items=int(b[1])
        remaining_items=b[2:]
        
        return report_code, [number_of_items]+remaining_items
            
    
    # @property
    # def _data(self):
    #     """A list of the data in the .eso file, structured by the environments and reporting intervals.
        
    #     :returns: A list where each item is a dictionary of the complete data for a simulation environment.
    #         A environment dictionary has keys 'environment' and 'data'.
    #         'environment' contains a list with the enviroment metadata.
    #         'data' contains a list of dictionaries where each dictionary 
    #         represents the data from a time interval, using the report codes as keys.
    #     :rtype: list
        
    #     """
    #     return self._data
    
        
    # @property
    # def _data_dictionary(self):
    #     """A dictionary of the data dictionary items in the .eso file.
        
    #     :returns: A dictionary with {report_code,items}
    #     :rtype: dict
    #     """
    #     return self._data_dictionary
        
    
    def get_environments(self):
        """Returns a list of the simulation environments in the .eso file.
        
        :returns: A list of EPEsoSimulationEnvironment instances
        :rtype: list
        
        """
        return [EPEsoSimulationEnviroment(self,i) for i,x in enumerate(self._data)]
            
    
      
class EPEsoSimulationEnviroment():
    """
    """
    
    def __init__(self,
                 epeso,
                 index):
        self._epeso=epeso
        self._index=index
        
    
    def __repr__(self):
        ""
        return 'EPEsoSimuationEnvironment("%s")' % self.title
    
    
    @property
    def _dict(self):
        ""
        return self._epeso._data[self._index]
    
    
    @property
    def title(self):
        ""
        return self._dict['environment'][0]
    
    
    @property
    def latitude(self):
        ""
        return self._dict['environment'][1]
    
    
    @property
    def longitude(self):
        ""
        return self._dict['environment'][2]
    
    
    @property
    def time_zone(self):
        ""
        return self._dict['environment'][3]
    
    
    @property
    def elevation(self):
        ""
        return self._dict['environment'][4]
    
    
    def get_interval_periods(self):
        ""
        return EPEsoIntervalPeriods(self,2)
    
    
    def get_interval_variables(self):
        ""
        frequency=2
        report_codes=self._dict['frequency'].get(frequency,{}).keys()
        return [EPEsoIntervalVariable(self,frequency,report_code) 
                for report_code in report_codes if not report_code==frequency]
    
    
    def get_daily_variables(self):
        ""
        frequency=3
        report_codes=self._dict['frequency'].get(frequency,{}).keys()
        return [EPEsoDailyVariable(self,frequency,report_code) 
                for report_code in report_codes if not report_code==frequency]
                
    
    def get_monthly_variables(self):
        ""
        frequency=4
        report_codes=self._dict['frequency'].get(frequency,{}).keys()
        return [EPEsoMonthlyVariable(self,frequency,report_code) 
                for report_code in report_codes if not report_code==frequency]
        
    
    def get_run_period_variables(self):
        ""
        frequency=5
        report_codes=self._dict['frequency'].get(frequency,{}).keys()
        return [EPEsoRunPeriodVariable(self,frequency,report_code) 
                for report_code in report_codes if not report_code==frequency]
        
    
    def get_annual_variables(self):
        ""
        frequency=6
        report_codes=self._dict['frequency'].get(frequency,{}).keys()
        return [EPEsoAnnualVariable(self,frequency,report_code) 
                for report_code in report_codes if not report_code==frequency]
    
    
    def get_timezone(self):
        """returns a datetime.timezone instance
        """
        return datetime.timezone(datetime.timedelta(hours=self.time_zone))
    
    
                                 
class _EPEsoPeriods():
    """
    """
    def __init__(self,
                 epesose,
                 frequency):
        ""
        self._epesose=epesose
        self._frequency=frequency
        
        
    @property
    def _data(self):
        ""
        return self._epesose._dict['frequency'][self._frequency][self._frequency]
    
    

class EPEsoIntervalPeriods(_EPEsoPeriods):
    """
    """
    
    @property
    def day_of_simulation(self):
        ""
        return self._data[0]
    
    
    @property
    def month(self):
        ""
        return self._data[1]
    
    
    @property 
    def day_of_month(self):
        ""
        return self._data[2]
    
    
    @property 
    def dst_indicator(self):
        ""
        return self._data[3]
    
    
    @property 
    def hour(self):
        ""
        return self._data[4]
    
    
    @property 
    def start_minute(self):
        ""
        return [int(x) for x in self._data[5]] # assumes whole minutes
    
    
    @property 
    def end_minute(self):
        ""
        return [int(x) for x in self._data[6]] # assumes whole minutes
    
    
    @property 
    def day_type(self):
        ""
        return self._data[7]
    
    
    def get_start_times(self):
        ""
        x=zip(self.month,self.day_of_simulation,self.hour,self.start_minute)
        return [datetime.datetime(2001,m,d,h-1,mi,
                                  tzinfo=self._epesose.get_timezone())
                for m,d,h,mi in x]
    
    
    def get_end_times(self):
        ""
        start_times=self.get_start_times()
        x=zip(start_times,self.start_minute,self.end_minute)
        return [start_time+datetime.timedelta(minutes=end_minute-start_minute) 
                for start_time,start_minute,end_minute in x]
    
    
    
class EPEsoVariable():
    """
    """
    
    def __init__(self,
                 epesose,
                 frequency,
                 report_code):
        ""
        self._epesose=epesose
        self._frequency=frequency
        self._report_code=report_code
        
        
    @property
    def _data(self):
        ""
        return self._epesose._dict['frequency'][self._frequency][self._report_code]
        
        
    @property
    def _datadict(self):
        ""
        return self._epesose._epeso._data_dictionary[self._report_code]
    
    
    @property
    def location(self):
        ""
        return self._datadict[1]
    
    
    @property
    def quantity(self):
        ""
        return self._datadict[2].split('[')[0].strip()
    
    
    @property
    def units(self):
        ""
        return self._datadict[2].split('[')[1].split(']')[0]
    
    
    @property
    def values(self):
        ""
        return self._data[0]



class EPEsoIntervalVariable(EPEsoVariable):
    """
    """
    
    def __repr__(self):
        ""
        return 'EPEsoIntervalVariable(report_code=%s)' % (self._report_code)
    
        
    
class EPEsoDailyVariable(EPEsoVariable):
    """
    """
    
    def __repr__(self):
        ""
        return 'EPEsoDailyVariable(report_code=%s)' % (self._report_code)
    
    
    @property
    def min_value(self):
        ""
        return self._data[1]
    
    
    @property
    def min_hour(self):
        ""
        return self._data[2]
    
    
    @property
    def min_minute(self):
        ""
        return self._data[3]
    
    
    @property
    def max_value(self):
        ""
        return self._data[4]
    
    
    @property
    def max_hour(self):
        ""
        return self._data[5]
    
    
    @property
    def max_minute(self):
        ""
        return self._data[6]
    
   
    
class EPEsoMonthlyVariable(EPEsoVariable):
    """
    """
    
    def __repr__(self):
        ""
        return 'EPEsoMonthlyVariable(report_code=%s)' % (self._report_code)
    
    
    @property
    def min_value(self):
        ""
        return self._data[1]
    
    
    @property
    def min_day(self):
        ""
        return self._data[2]
    
    
    @property
    def min_hour(self):
        ""
        return self._data[3]
    
    
    @property
    def min_minute(self):
        ""
        return self._data[4]
    
    
    @property
    def max_value(self):
        ""
        return self._data[5]
    
    
    @property
    def max_day(self):
        ""
        return self._data[6]
    
    
    @property
    def max_hour(self):
        ""
        return self._data[7]
    
    
    @property
    def max_minute(self):
        ""
        return self._data[8]
    
    
        
class EPEsoRunPeriodVariable(EPEsoVariable):
    """
    """
    
    def __repr__(self):
        ""
        return 'EPEsoRunPeriodVariable(report_code=%s)' % (self._report_code)
        
    
    
class EPEsoAnnualVariable(EPEsoVariable):
    """
    """
    
    def __repr__(self):
        ""
        return 'EPEsoAnnualVariable(report_code=%s)' % (self._report_code)
        
        
        
    