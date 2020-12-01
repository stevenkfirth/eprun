# -*- coding: utf-8 -*-

from .epeso_simulation_environment import EPEsoSimulationEnviroment


class EPEso():
    """A class for an EnergyPlus .eso file.
    
    :param fp: The filepath for the .eso file.
    :type fp: str
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPEso
       >>> e=EPEso(fp='eplusout.eso')
       >>> print(e.programme_version_statement)
       {'programme': 'EnergyPlus',
        'timestamp': 'YMD=2020.11.13 06:25',
        'version': 'Version 9.4.0-998c4b761e'}
       >>> print(e.standard_items_dictionary[1])
       {'comment': None,
        'items': [{'name': 'Environment Title', 'unit': None},
                  {'name': 'Latitude', 'unit': 'deg'},
                  {'name': 'Longitude', 'unit': 'deg'},
                  {'name': 'Time Zone', 'unit': None},
                  {'name': 'Elevation', 'unit': 'm'}],
        'number_of_values': 5}
       >>> print(e.variable_dictionary[7])
       {'comment': 'Hourly',
        'number_of_values': 1,
        'object_name': 'Environment',
        'quantity': 'Site Outdoor Air Drybulb Temperature',
        'unit': 'C'}
       >>> print(e.get_environments())
       [EPEsoSimuationEnvironment("DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB"),
        EPEsoSimuationEnvironment("DENVER CENTENNIAL  GOLDEN   N ANN CLG 1% CONDNS DB=>MWB"),
        EPEsoSimuationEnvironment("RUN PERIOD 1")]

    .. seealso::
    
       Output Details and Examples, page 126.
       https://energyplus.net/quickstart

    """

    def __init__(self,fp):
        ""
        
        programme_version_statement_flag=True # True if in his section
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



    @property
    def data(self):
        """A list of the simulation environment data dictionaries.
        
        :returns: A list of dictionaries where each dictionary holds the
            data from a simulation environment such as a winter design day,
            a summer design day or a full annual simulation. The dictionary
            has keys 'environment_title', 'latitude', 'longitude',
            'time_zone', 'elevation', 'interval_data' ,'daily_data',
            'monthly_data', 'run_period_data' and 'annual_data'.
        :rtype: list
        """
        return self._data


    @property
    def programme_version_statement(self):
        """A dictionary of the programme version statement.
        
        :returns: A dictionary with keys 'programme', 'version' and 'timestamp'.
        :rtype: dict
        """
        return self._programme_version_statement
    

    @property
    def standard_items_dictionary(self):
        """A dictionary of the standard items in the data dictionary.
        
        :returns: A dictionary with the keys based on the report codes and the values given 
            by a dictionary with keys 'number_of_values', 'items' and 'comment'.
        :rtype: dict
        """
        return self._standard_items_dictionary


    @property
    def variable_dictionary(self):
        """A dictionary of the variables in the data dictionary.
        
        :returns: A dictionary with the keys based on the report codes and the values given 
            by a dictionary with keys 'number_of_values', 'object_name', 'quantity', 
            'unit' and 'comment'.
        :rtype: dict
        """
        return self._variable_dictionary


    def get_environments(self):
        """Returns a list of the simulation environments in the .eso file.
        
        :returns: A list of `EPEsoSimulationEnvironment` instances.
        :rtype: list
        
        """
        result=[]
        for i in range(len(self._data)):
            epesose=EPEsoSimulationEnviroment()
            epesose._epeso=self
            epesose._index=i
            result.append(epesose) 
        return result
    
    
      
    
    
    
   


    
    
    

    



       
    
    
   
   
    
      
    
        
        
    
    
        
        
        
    