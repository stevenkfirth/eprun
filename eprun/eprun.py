# -*- coding: utf-8 -*-

import os
import subprocess
import time
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import calendar


        
def runsim(input_filepath,
          epw_filepath,
          sim_dir='.',
          ep_dir='C:\EnergyPlusV9-4-0',
          annual=False,
          convert=False,
          design_day=False,
          epmacro=False,
          expand_objects=False,
          output_prefix='eplus',
          output_suffix='L',
          readvars=False,
          print_call=False,
          **kwargs):
    """Runs an EnergyPlus simulation and returns the results.
    
    :param input_filepath: The filepath of the input file.
        This can be either an .idf file or an .epJSON file.
        This can be relative or absolute.
    :type input_filepath: str
    
    :param epw_filepath: The filepath of the climate .epw file.
        This can be relative or absolute.
    :type epw_filepath: str
    
    :param sim_dir: The directory to hold the simulation files.
        This can be relative or absolute.
        Default is '.' which is the current directory.
    :type sim_dir: str
    
    :param ep_dir: The EnergyPlus directory where 'energyplus.exe' is installed.
        Default is 'C:\EnergyPlusV9-4-0'.
    :type ep_dir: str
    
    :param annual: If True, the '--annual' argument is included in the call
        to EnergyPlus. 
        This is the argument for 'Forces annual simulation'.
        Default is False.
    :type annual: bool
    
    :param convert: If True, the '--convert' argument is included in the call
        to EnergyPlus. 
        This is the argument for 'Output IDF->epJSON or epJSON->IDF, dependent on
        input file type'.
        Default is False.
    :type convert: bool
    
    :param design_day: If True, the '--design-day' argument is included in the call
        to EnergyPlus. 
        This is the argument for 'Forces design-day-only simulation'.
        Default is False.
    :type design_day: bool
    
    :param epmacro: If True, the '--epmacro' argument is included in the call
        to EnergyPlus. 
        This is the argument for 'Run EPMacro prior to simulation'.
        Default is False.
    :type epmacro: bool
    
    :param expand_objects: If True, the '--expandobjects' argument is included
        in the call to EnergyPlus.
        This is the argument for 'Run ExpandObjects prior to simulation'.
        Default is False.
    :type expand_objects: bool
    
    :param output_prefix: Prefic for output file names.
        Default is 'eplus'.
    :type output_prefix: str
    
    :param output_suffix: Suffix style for output names.
        Should be one of 'L' (legacy), 'C' (capital) or 'D' (dash).
        Default is 'L'
    :type output_suffix: str
    
    :param readvars: If True, the '--readvars' argument is included in the 
        call to EnergyPlus.
        This is the argument for 'Run ReadVarsESO after simulation'.
        Default is False.
    :type readvars: bool
        
    :param print_call: If True then the call string is printed.
        Default is False.
    :type print_call: bool
    
    :returns: A EPResult object which contains the returncode, stdout and a 
        dictionary of the results files.
    :rtype: EPResult
    
    .. rubric:: Code Example
    
    .. code-block:: python
           
       >>> from eprun import eprun
       >>> epresult=eprun(ep_dir='C:\EnergyPlusV9-4-0',
       >>>                input_filepath='1ZoneUncontrolled.idf',
       >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
       >>>                sim_dir='simulation_files')
       >>> print(type(epresult))
       <class 'eprun.epresult.EPResult'>
       >>> print(list(epresult.files.keys()))
       ['audit', 'bnd', 'dxf', 'eio', 'end', 'err', 'eso', 'mdd', 'mtd', 
        'mtr', 'rdd', 'shd', 'csv', 'htm', 'tab', 'txt', 'xml']
               
    .. seealso::
    
       EnergyPlus Essentials, pages 15 and 16.
       https://energyplus.net/quickstart#reading
    
    """
    
    # get absolute filepaths
    input_absolute_filepath=os.path.abspath(input_filepath)
    epw_absolute_filepath=os.path.abspath(epw_filepath)
    sim_absolute_dir=os.path.abspath(sim_dir)
    
    # get EnergyPlus exe filepath
    ep_exe=r'%s\EnergyPlus' % ep_dir
    
    # create the Command Prompt string to run EnergyPlus
    st='"%s" %s%s%s%s%s%s--output-prefix %s --output-suffix %s --output-directory "%s" --weather "%s" "%s"' % (ep_exe,
                                            '--annual ' if annual else '',
                                            '--convert ' if convert else '',
                                            '--design-day ' if design_day else '',
                                            '--epmacro ' if epmacro else '',
                                            '--expandobjects ' if expand_objects else '',
                                            '--readvars ' if readvars else '',
                                            output_prefix,
                                            output_suffix,
                                            sim_absolute_dir,
                                            epw_absolute_filepath,
                                            input_absolute_filepath
                                            )
    
    # print_call
    if print_call: print(st)
    
    # get simulation start time in seconds since the epoch
    simulation_start_time=time.time()
        
    # run EnergyPlus simulation using subprocess.run
    result=subprocess.run(st,capture_output=True,**kwargs)
    
    # get outputs
    returncode=result.returncode
    stdout=result.stdout.decode()
    
    # get files in sim_dir which were modified (or created) after the simulation start time
    files={}
    for fp in os.listdir(sim_absolute_dir):
        afp=os.path.join(sim_absolute_dir,fp)
        extension=os.path.splitext(fp)[1][1:]
        modified_time=os.path.getmtime(afp)
        if modified_time>simulation_start_time:
            files[extension]=afp
    
    # set up the return object
    result=EPResult()
    result._returncode=returncode
    result._stdout=stdout
    result._files=files
    
    return result
    
    
class EPResult():
    """A class representing the results of an EnergyPlus simulation.
    
    .. note::
        
       An EPResult instance is returned as the result of the `runsim` function.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
           
       >>> from eprun import eprun
       >>> epresult=eprun(ep_dir='C:\EnergyPlusV9-4-0',
       >>>                input_filepath='1ZoneUncontrolled.idf',
       >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
       >>>                sim_dir='simulation_files')
       >>> print(type(epresult))
       <class 'eprun.epresult.EPResult'>
       >>> print(epresult.returncode)
       0

    """
    
    @property
    def files(self):
        """A dictionary of the results files from a successful EnergyPlus simulation.
        The keys of the dictionary are the file extensions e.g. 'eso', 'err' etc.
        The values of the dictionary are the absolute filepaths of the files.
        
        :rtype: dict (str,str)
        
        """
        return self._files
    
    
    def get_end(self):
        """Gets the .end output file.
        
        :rtype: EPEnd        
        
        """
        fp=self.files['end']
        return EPEnd(fp)
    
    
    def get_err(self):
        """Gets the .err output file.
        
        :rtype: EPErr        
        
        """
        fp=self.files['err']
        return EPErr(fp)
    
    
    def get_eso(self):
        """Gets the .eso output file.
        
        :rtype: EPEso       
        
        """
        fp=self.files['eso']
        return EPEso(fp)
    
    
    @property
    def returncode(self):
        """The returncode of the `subprocess.run` call to the EnergyPlus exe file.
        This indicates if the call to EnergyPlus was successful.
        0 means success. 1 means failure.
        
        :rtype: int
        
        """
        return self._returncode
    
    
    @property
    def stdout(self):
        """The stdout of the `subprocess.run` call to the EnergyPlus exe file.
        This is the text that would appear in the CommandPromt if the command was run there.
        
        :rtype: str
        
        """
        return self._stdout
    

class EPEnd():
    """A class for an EnergyPlus .end file.
    
    :param fp: The filepath for the .end file.
    :type fp: str
    
    .. rubric:: Code Example
        
    .. code-block:: python
           
       >>> from eprun import EPEnd
       >>> end=EPEnd(r'simulation_files\eplusout.end')
       >>> print(type(end))
       <class 'eprun.epend.EPEnd'>
       >>> print(end.line)
       EnergyPlus Completed Successfully-- 0 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.21sec
    
    .. seealso::
    
       Output Details and Examples, page 125.
       https://energyplus.net/quickstart#reading
    
    """        
    
    def __init__(self,fp):
        ""
        with open(fp,'r') as f:
            self._line=f.readline().strip()
            
            
    @property
    def line(self):
        """The single line recorded in the .end file.
        
        :rtype: str
        """
        return self._line
        

                    
class EPErr():
    """A class for an EnergyPlus .err file.
    
    :param fp: The filepath for the .err file.
    :type fp: str
    
    .. rubric:: Code Example
        
    .. code-block:: python
           
       >>> from eprun import EPErr
       >>> err=EPErr(r'simulation_files\eplusout.err')
       >>> print(type(err))
       <class 'eprun.eperr.EPErr'>
       >>> print(err.firstline)
       Program Version,EnergyPlus, Version 9.4.0-998c4b761e, YMD=2020.12.31 08:53,
       >>> print(err.lastline)
       EnergyPlus Completed Successfully-- 0 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.21sec
       >>> print(err.warnings)
       []
       
    .. seealso::
    
       Output Details and Examples, page 125.
       https://energyplus.net/quickstart#reading
    
    """        
        
    def __init__(self,fp):
        ""
        lines=''
        warnings=[]
        severes=[]
        
        with open(fp,'r') as f:
            for line in f:
                lines+=line
                
                # first line
                if line.startswith('Program Version'):
                    firstline=line
                
                # warning
                if line.startswith('   ** Warning ** '):
                    warnings.append(line[17:].strip())
                    current_message=warnings
                    
                # severe
                if line.startswith('   ** Severe  ** '):
                    severes.append(line[17:].strip())
                    current_message=severes
                    
                # error message continuation
                if line.startswith('   **   ~~~   ** '):
                    current_message[-1]+=' ' + line[17:].strip()
        
        self._firstline=firstline
        self._lastline=line[17:]
        self._lines=lines
        self._severes=severes
        self._warnings=warnings
        
        
        
    @property
    def firstline(self):
        """The first line recorded in the .err file.
        
        :rtype: str
        
        """
        return self._firstline
    
    
    @property
    def lastline(self):
        """The last line recorded in the .err file.
        
        :rtype: str
        
        """
        return self._lastline
    
        
    @property
    def lines(self):
        """The lines recorded in the .err file.
        
        :rtype: str
        
        """
        return self._lines
        
    
    @property
    def severes(self):
        """The severe errors recorded in the .err file.
        
        :rtype: list (str)
        
        """
        return self._severes
    
    
    @property
    def warnings(self):
        """The warning errors recorded in the .err file.
        
        :rtype: list (str)
        
        """
        return self._warnings
        
        
class EPEso():
    """A class for an EnergyPlus .eso file.
    
    :param fp: The filepath for the .eso file.
    :type fp: str
    
    .. rubric:: Code Example
        
    .. code-block:: python
           
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> print(type(eso))
       <class 'eprun.epeso.EPEso'>
       >>> print(eso.programme_version_statement)
       {'programme': 'EnergyPlus', 
        'version': 'Version 9.4.0-998c4b761e', 
        'timestamp': 'YMD=2020.12.31 08:53'}
       >>> print(eso.standard_items_dictionary[1])
       {'comment': None,
        'items': [{'name': 'Environment Title', 'unit': None},
                  {'name': 'Latitude', 'unit': 'deg'},
                  {'name': 'Longitude', 'unit': 'deg'},
                  {'name': 'Time Zone', 'unit': None},
                  {'name': 'Elevation', 'unit': 'm'}],
        'number_of_values': 5}
       >>> print(eso.variable_dictionary[7])
       {'comment': 'Hourly',
        'number_of_values': 1,
        'object_name': 'Environment',
        'quantity': 'Site Outdoor Air Drybulb Temperature',
        'unit': 'C'}
       >>> print(eso.get_environments())
       [EPEsoSimuationEnvironment("DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB"),
        EPEsoSimuationEnvironment("DENVER CENTENNIAL  GOLDEN   N ANN CLG 1% CONDNS DB=>MWB"),
        EPEsoSimuationEnvironment("RUN PERIOD 1")]

    .. seealso::
    
       Output Details and Examples, page 126.
       https://energyplus.net/quickstart

    """

    def __init__(self,fp):
        ""
        programme_version_statement_flag=True # True if in this section
        data_dictionary_flag=False # True if in this section
        data_flag=False # True if in this section
                
        standard_items_dictionary={}
        variable_dictionary={}
        data=[]
                
        with open(fp,'r') as f:
            
            for line in f: # loop through lines in file
                
                if programme_version_statement_flag: # programme version statement (first row)
                    
                    row=line.strip().split(',')
                    programme_version_statement={'programme':row[1].strip(),
                                                 'version':row[2].strip(),
                                                 'timestamp':row[3].strip()}
                    programme_version_statement_flag=False
                    data_dictionary_flag=True
                    
                    
                elif data_dictionary_flag: # data dictionary section
                    
                    if line.startswith('End of Data Dictionary'): # end of section line
                        
                        data_dictionary_flag=False
                        data_flag=True
                        
                    else: # a data dictionary line
                    
                        line_and_comment=line.split('!')
                        row=line_and_comment[0].split(',')
                        try:
                            comment=line_and_comment[1].strip()
                        except IndexError:
                            comment=None
                    
                        report_code=int(row[0])
                        number_of_values=int(row[1])
                        
                        if report_code<=6: # a 'standard item'
                        
                            items=[]
                            for item in row[2:]:
                                a=item.split('[')
                                name=a[0].strip()
                                try:
                                    unit=a[1].split(']')[0].strip() or None
                                except IndexError:
                                    unit=None
                                items.append({'name':name,
                                              'unit':unit})
                            
                            standard_items_dictionary[report_code]={'number_of_values':number_of_values,
                                                                    'items':items,
                                                                    'comment':comment}
                        
                        else: # a 'variable item'
                            
                            object_name=row[2]
                            a=row[3].split('[')
                            quantity=a[0].strip()
                            try:
                                unit=a[1].split(']')[0].strip() or None
                            except IndexError:
                                unit=None
                        
                            variable_dictionary[report_code]={'number_of_values':number_of_values,
                                                              'object_name':object_name,
                                                              'quantity':quantity,
                                                              'unit':unit,
                                                              'comment':comment}
                        
    
                elif data_flag: # data section
                
                    if line.startswith('End of Data'):
                        
                        data_flag=False
                    
                    else:
                        
                        row=[x.strip() for x in line.split(',')]
                        report_code=int(row[0])
                        
                        if report_code==1: # start of a new simulation environment
                            
                            simulation_environment={'environment_title':row[1].strip(),
                                                    'latitude':row[2].strip(),
                                                    'longitude':row[3].strip(),
                                                    'time_zone':row[4].strip(),
                                                    'elevation':row[5].strip(),
                                                    'interval_data':{2:[]},
                                                    'daily_data':{3:[]},
                                                    'monthly_data':{4:[]},
                                                    'run_period_data':{5:[]},
                                                    'annual_data':{6:[]}}
                            
                            data.append(simulation_environment)
                            
                            
                        elif report_code==2:
                            
                            d=simulation_environment['interval_data']
                            d[report_code].append(row[1:])
                            
                        elif report_code==3:
                            
                            d=simulation_environment['daily_data']
                            d[report_code].append(row[1:])
                            
                        elif report_code==4:
                            
                            d=simulation_environment['monthly_data']
                            d[report_code].append(row[1:])
                            
                            
                        elif report_code==5:
                            
                            d=simulation_environment['run_period_data']
                            d[report_code].append(row[1:])
                            
                        elif report_code==6:
                            
                            d=simulation_environment['annual_data']
                            d[report_code].append(row[1:])
                            
                        else:
                            
                            x=d.setdefault(report_code,[])
                            x.append(row[1:])
                            
                else: # beyond the data section
                    
                    pass

        # zip the interval data
        for env in data:
            for k in env['interval_data'].keys():
                env['interval_data'][k]=tuple(zip(*env['interval_data'][k]))
            for k in env['daily_data'].keys():
                env['daily_data'][k]=tuple(zip(*env['daily_data'][k]))
            for k in env['monthly_data'].keys():
                env['monthly_data'][k]=tuple(zip(*env['monthly_data'][k]))
            for k in env['run_period_data'].keys():
                env['run_period_data'][k]=tuple(zip(*env['run_period_data'][k]))
            for k in env['annual_data'].keys():
                env['annual_data'][k]=tuple(zip(*env['annual_data'][k]))
            
        # set attributes
        self._programme_version_statement=programme_version_statement
        self._standard_items_dictionary=standard_items_dictionary
        self._variable_dictionary=variable_dictionary
        self._data=data


    def get_environment(self,environment_title):
        """Returns a simulation environment in the .eso file.
        
        :param environment_title: The name of the simulation environment.
        :type environment_title: str
        
        :raises IndexError: If `environment_title` does not match any of the simulation environments.
        
        :rtype: EPEsoSimulationEnvironment
        
        """
        for se in self.get_environments():
            if environment_title == se.environment_title:
                return se
        raise IndexError('Simulation environment "%s" does not exist in the .eso file')


    def get_environments(self):
        """Returns a list of the simulation environments in the .eso file.
        
        :returns: A list of `EPEsoSimulationEnvironment` instances.
        :rtype: list (EPEsoSimulationEnvironment)
        
        """
        result=[]
        for i in range(len(self._data)):
            epesose=EPEsoSimulationEnvironment()
            epesose._epeso=self
            epesose._index=i
            result.append(epesose) 
        return result


    @property
    def programme_version_statement(self):
        """A dictionary of the programme version statement.
        
        :returns: A dictionary with keys 'programme', 'version' and 'timestamp'.
        :rtype: dict (str, str)
        
        """
        return self._programme_version_statement
    

    @property
    def standard_items_dictionary(self):
        """A dictionary of the standard items in the data dictionary.
        
        :returns: A dictionary with the keys based on the report codes and the values given 
            by a dictionary with keys 'number_of_values', 'items' and 'comment'.
        :rtype: dict (int,dict)
        """
        return self._standard_items_dictionary


    @property
    def variable_dictionary(self):
        """A dictionary of the variables in the data dictionary.
        
        :returns: A dictionary with the keys based on the report codes and the values given 
            by a dictionary with keys 'number_of_values', 'object_name', 'quantity', 
            'unit' and 'comment'.
        :rtype: dict (int,dict)
        """
        return self._variable_dictionary




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

    
    
class EPEsoAnnualVariable():
    """A class for an annual variable recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoAnnualVariable(report_code=%s)' % (self._report_code)



class EPEsoDailyPeriods():
    """A class for the daily time periods recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoDailyPeriods instance is returned as the result of 
       the `get_daily_periods` method.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> env=eso.get_environment('RUN PERIOD 1')
       >>> dp=env.get_daily_periods()
       >>> print(type(dp))
       <class 'eprun.epeso_daily_periods.EPEsoDailyPeriods'>
       >>> print(dp.get_start_times()[:5])
       (datetime.datetime(2001, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 2, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 3, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 4, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 5, 0, 0, tzinfo=datetime.timezone.utc))
       
    """
    
    def __repr__(self):
        ""
        return 'EPEsoDailyPeriods(sim_env="%s")' % self._epesose.environment_title
    
    
    @property
    def _data(self):
        """The daily period data.
        
        :rtype: tuple
        
        """
        return self._epesose._data['daily_data'][3]
    
    @property
    def cumulative_days_of_simulation(self):
        """The 'cumulative days of simulation' for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[0])
    
        
    @property 
    def days_of_month(self):
        """The days in the month for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[2])
    

    @property 
    def day_types(self):
        """The day types for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(str(x) for x in self._data[7])


    @property 
    def dst_indicators(self):
        """The daylight saving time indicators for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[3])
    
    
    
    def get_end_times(self):
        """Returns the end times for the daily periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        return tuple(start_time+datetime.timedelta(days=1) 
                     for start_time in self.get_start_times())


    def get_interval(self):
        """Returns the time interval between periods.
        
        :rtype: datetime.timedelta
        
        """
        return datetime.timedelta(days=1)
        


    def get_periods(self):
        """Returns the interval periods as a list of Pandas periods.
        
        :rtype: list (pandas.Period)
        
        """
        start_times=self.get_start_times()
        period_frequency='%sS' % self.get_interval().total_seconds()
        return [pd.Period(start_time,period_frequency) for start_time in start_times]


    def get_start_times(self):
        """Returns the start times for the daily periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        x=zip(self.months,self.days_of_month)
        return tuple(datetime.datetime(2001,m,d,
                                  tzinfo=self._epesose.get_timezone())
                     for m,d in x)


    @property
    def months(self):
        """The months for the daily periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[1])


    def summary(self):
        """Returns a summary of the interval periods.
        
        :rtype: str
        
        """
        start_times=self.get_start_times()
        return 'Starts at %s, %s periods @ 1 day intervals' % (start_times[0].isoformat(),
                                                               len(start_times))
    
    
        
class EPEsoDailyVariable():
    """A class for a daily variable recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoDailyVariable instance is returned as the result of 
       the `get_daily_variable` or `get_daily_variables` methods.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> env=eso.get_environment('RUN PERIOD 1')
       >>> dv=env.get_daily_variables()[0]
       >>> print(type(dv))
       <class 'eprun.epeso_daily_variable.EPEsoDailyVariable'>
       >>> print(dv.summary())
       51 - ZN001:WALL001 - Surface Inside Face Temperature (C)
       >>> print(dv.values[:5])
       (0.2586823729828891, -2.1861342037263127, -3.1313024424355285, -2.9489865949136895, 0.3701320282261298)
    
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
        index=pd.Index(data=self._daily_periods.get_start_times(),
                       name='start_times')
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
        
        :rtype: tuple (datetime.datetime)
        
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
        
        :rtype: tuple (datetime.datetime)
        
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
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[5])
    
    
    @property
    def max_minutes(self):
        """The minute numbers for the maximum values of the daily variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[6])
    
    
    @property
    def max_values(self):
        """The maximum values of the monthly variable.
        
        :rtype: tuple (float)
        
        """
        return tuple(float(x) for x in self._data[4])
    
    
    @property
    def min_hours(self):
        """The hour numbers for the minimum values of the daily variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[2])


    @property
    def min_minutes(self):
        """The minute numbers for the minimum values of the daily variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[3])
    
        
    @property
    def min_values(self):
        """The minimum values of the daily variable.
        
        :rtype: tuple (float)
        
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
        """Plots the daily variable on the supplied axes.
        
        :param ax: An Axes instance. 
            Optional, if not supplied then automatically created.
        :type ax: matplotlib.axes.Axes
        :param kwargs: Keyword arguments to be supplied to the matplotlib plot call.
        
        :returns: The Axes instance.
        :rtype: matplotlib.axes.Axes
        
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
        
        :rtype: tuple (float)
        
        """
        return tuple(float(x) for x in self._data[0])
    
    
    
class EPEsoIntervalPeriods():
    """A class for the interval time periods recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoIntervalPeriods instance is returned as the result of 
       the `get_interval_periods` method.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> env=eso.get_environment('RUN PERIOD 1')
       >>> ip=env.get_interval_periods()
       >>> print(type(ip))
       <class 'eprun.epeso_interval_periods.EPEsoIntervalPeriods'>
       >>> print(ip.get_start_times()[:5])
       (datetime.datetime(2001, 1, 1, 0, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 1, 1, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 1, 2, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 1, 3, 0, tzinfo=datetime.timezone.utc), 
        datetime.datetime(2001, 1, 1, 4, 0, tzinfo=datetime.timezone.utc))
       
    """
    
    def __repr__(self):
        ""
        return 'EPEsoIntervalPeriods()' 
    
    
    @property
    def _data(self):
        """The interval period data.
        
        :rtype: tuple
        
        """
        return self._epesose._data['interval_data'][2]

    
    @property 
    def day_types(self):
        """The day types for the interval periods.
        
        :rtype: tuple (str)
        
        """
        return tuple(str(x) for x in self._data[7])


    @property 
    def days_of_month(self):
        """The days in the month for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[2])
    

    @property
    def days_of_simulation(self):
        """The 'day of simulation' values for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[0])
    
    
    @property 
    def dst_indicators(self):
        """The daylight saving time indicators for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[3])
    
    
    @property 
    def end_minutes(self):
        """The end minutes for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(float(x)) for x in self._data[6]) 
    
    
    def get_end_times(self):
        """Returns the end times for the interval periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        start_times=self.get_start_times()
        x=zip(start_times,self.start_minutes,self.end_minutes)
        return tuple(start_time+datetime.timedelta(minutes=end_minute-start_minute) 
                     for start_time,start_minute,end_minute in x)
 
    
    def get_interval(self):
        """Returns the time interval between periods.
        
        :rtype: datetime.timedelta
        
        """
        return datetime.timedelta(minutes=self.end_minutes[0]-self.start_minutes[0])
        
    
    def get_periods(self):
        """Returns the interval periods as a list of Pandas periods.
        
        :rtype: list (pandas.Period)
        
        """
        start_times=self.get_start_times()
        period_frequency='%sS' % self.get_interval().total_seconds()
        return [pd.Period(start_time,period_frequency) for start_time in start_times]
    
    
    def get_start_times(self):
        """Returns the start times for the interval periods.
        
        :rtype: tuple (datetime.datetime)
        
        """
        x=zip(self.months,self.days_of_month,self.hours,self.start_minutes)
        return tuple(datetime.datetime(2001,m,d,h-1,mi,
                                  tzinfo=self._epesose.get_timezone())
                     for m,d,h,mi in x)
    
    
    @property 
    def hours(self):
        """The hours for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[4])
    
    
    @property
    def months(self):
        """The months for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[1])
    
    
    @property 
    def start_minutes(self):
        """The start minutes for the interval periods.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(float(x)) for x in self._data[5]) 
    
    
    def summary(self):
        """Returns a summary of the interval periods.
        
        :rtype: str
        
        """
        start_times=self.get_start_times()
        return 'Starts at %s, %s periods @ %s minute intervals' % (start_times[0].isoformat(),
                                                                  len(start_times),
                                                                  int(self.get_interval().total_seconds()/60))
        
    
    
class EPEsoIntervalVariable():
    """A class for an interval variable recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoIntervalVariable instance is returned as the result of 
       the `get_interval_variable` or `get_interval_variables` methods.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> env=eso.get_environment('RUN PERIOD 1')
       >>> iv=env.get_interval_variables()[0]
       >>> print(type(iv))
       <class 'eprun.epeso_interval_variable.EPEsoIntervalVariable'>
       >>> print(iv.summary())
       7 - Environment - Site Outdoor Air Drybulb Temperature (C)
       >>> print(iv.values[:5])
       (-4.5, -3.0, -3.625, -2.75, -2.0)
    
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
        index=pd.Index(data=self._interval_periods.get_start_times(),
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
            Optional, if not supplied then automatically created.
        :type ax: matplotlib.axes.Axes
        :param kwargs: Keyword arguments to be supplied to the matplotlib plot call.
        
        :returns: The Axes instance.
        :rtype: matplotlib.axes.Axes
        
        """
        if not ax:
            fig, ax = plt.subplots(figsize=(16,4))
        
        
        ax.plot(self.values)
        ax.set_title('%s' % (self.summary()))
        ax.set_xlabel('Period number')
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
        
        :rtype: tuple (float)
        
        """
        return tuple(float(x) for x in self._data[0])
 
    
    
class EPEsoMonthlyPeriods():
    """A class for the monthly time periods recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoMonthlyPeriods instance is returned as the result of 
       the `get_monthly_periods` method.
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

    
    

class EPEsoMonthlyVariable():
    """A class for a monthly variable recorded in an `EPEsoSimulationEnvironment` instance.
    
    .. note::
        
       An EPEsoMonthlyVariable instance is returned as the result of 
       the `get_monthly_variable` or `get_monthly_variables` methods.
       It should not be instantiated directly.
    
    .. rubric:: Code Example
        
    .. code-block:: python
    
       >>> from eprun import EPEso
       >>> eso=EPEso(r'simulation_files\eplusout.eso')
       >>> env=eso.get_environment('RUN PERIOD 1')
       >>> mv=env.get_monthly_variables()[0]
       >>> print(type(mv))
       <class 'eprun.epeso_monthly_variable.EPEsoMonthlyVariable'>
       >>> print(mv.summary())
       48 - TEST 352A - Other Equipment Total Heating Energy (J)
       >>> print(mv.values[:5])
       (942796800.0, 851558400.0, 942796800.0, 912384000.0, 942796800.0)
    
    """
        
    def __repr__(self):
        ""
        return 'EPEsoMonthlyVariable(report_code=%s)' % (self._report_code)
    
    @property
    def _data(self):
        """A dictionary with the variable data.
        
        :rtype: dict
        
        """
        return self._epesose._data['monthly_data'][self._report_code]
    
    
    @property
    def _monthly_periods(self):
        """The time periods object relating to the variable.
        
        :rtype: EPEsoDailyPeriods
        
        """
        return self._epesose.get_monthly_periods()
    
    
    @property
    def _variable_dictionary(self):
        """A dictionary with the variable data dicionary data
        
        :rtype: dict
        
        """
        return self._epesose._epeso._variable_dictionary[self._report_code]
    
    
    def get_dataframe(self):
        """Returns a pandas dataframe of the monthly variable.
        
        :rtype: pandas.DataFrame
        
        """
        index=pd.Index(data=self._monthly_periods.get_periods(),
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
        
        :rtype: tuple (datetime.datetime)
        
        """
        month_start_times=self._monthly_periods.get_start_times()
        result=[]
        for month_start_time,max_day,max_hour,max_minute in zip(month_start_times,
                                                                self.max_days,
                                                                self.max_hours,
                                                                self.max_minutes):
            t=datetime.datetime(month_start_time.year,
                                month_start_time.month,
                                max_day,
                                max_hour,
                                max_minute,
                                tzinfo=month_start_time.tzinfo
                                )
            result.append(t)
        return tuple(result)

    
    
    def get_min_times(self):
        """Returns the times when the minumum values occur.
        
        :rtype: tuple (datetime.datetime)
        
        """
        month_start_times=self._monthly_periods.get_start_times()
        result=[]
        for month_start_time,min_day,min_hour,min_minute in zip(month_start_times,
                                                                self.min_days,
                                                                self.min_hours,
                                                                self.min_minutes):
            t=datetime.datetime(month_start_time.year,
                                month_start_time.month,
                                min_day,
                                min_hour,
                                min_minute,
                                tzinfo=month_start_time.tzinfo
                                )
            result.append(t)
        return tuple(result)


    @property
    def max_days(self):
        """The day numbers for the maximum values of the monthly variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[6])
    
    
    @property
    def max_hours(self):
        """The hour numbers for the maximum values of the monthly variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[7])
    
    
    @property
    def max_minutes(self):
        """The minute numbers for the maximum values of the monthly variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[8])
    
        
    @property
    def max_values(self):
        """The maximum values of the monthly variable.
        
        :rtype: tuple (float)
        
        """
        return tuple(float(x) for x in self._data[5])
    
    
    @property
    def min_days(self):
        """The day numbers for the minimum values of the monthly variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[2])
    
    
    @property
    def min_hours(self):
        """The hour numbers for the minimum values of the monthly variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[3])
    
    
    @property
    def min_minutes(self):
        """The minute numbers for the minimum values of the monthly variable.
        
        :rtype: tuple (int)
        
        """
        return tuple(int(x) for x in self._data[4])


    @property
    def min_values(self):
        """The minimum values of the monthly variable.
        
        :rtype: tuple (float)
        
        """
        return tuple(float(x) for x in self._data[1])
    
            
    @property
    def object_name(self):
        """The object name of the monthly variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['object_name']


    def plot(self,
             ax=None,
             **kwargs):
        """Plots the monthly variable on the supplied axes.
        
        :param ax: An Axes instance. 
            Optional, if not supplied then automatically created.
        :type ax: matplotlib.axes.Axes
        :param kwargs: Keyword arguments to be supplied to the matplotlib plot call.
        
        :returns: The Axes instance.
        :rtype: matplotlib.axes.Axes
        
        """
        if not ax:
            fig, ax = plt.subplots(figsize=(16,4))
        
        ax.plot(self.values)
        ax.set_title('%s' % (self.summary()))
        ax.set_ylabel('%s' % (self.unit))
        
        return ax
        
    
    @property
    def quantity(self):
        """The quantity of the monthly variable.
        
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
        """The unit of the monthly variable.
        
        :rtype: str
        
        """
        return self._variable_dictionary['unit']
    
    
    @property
    def values(self):
        """The (mean) values of the monthly variable.
        
        :rtype: tuple (float)
        
        """
        return tuple(float(x) for x in self._data[0])


    
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
    
    
    
class EPEsoRunPeriodVariable():
    """A class for a run period variable recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoRunPeriodVariable(report_code=%s)' % (self._report_code)

    
    
    
    
    
    
    

        
