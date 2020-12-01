# -*- coding: utf-8 -*-

import os
import subprocess
import time

from .epresult import EPResult

        
def eprun(idf_filepath,
          epw_filepath,
          sim_dir='.',
          ep_dir='C:\EnergyPlusV9-4-0',
          expand_objects=False,
          convert=False,
          readvars=False):
    """Runs an EnergyPlus simulation and returns the results.
    
    :param idf_filepath: The filepath of the input .idf file.
        This can be relative or absolute.
    :type idf_filepath: str
    :param epw_filepath: The filepath of the climate .epw file.
        This can be relative or absolute.
    :type epw_filepath: str
    :param sim_dir: The directory to hold the simulation files.
        This can be relative or absolute.
        Default is '.' which is the current directory.
    :type sim_dir: str
    :param ep_dir: The EnergyPlus directory where 'energyplus.exe' is installed.
        Default is 'C:\EnergyPlusV9-4-0'.
    :type ep_folder: str
    :param expand_objects: If True, the '--expandobjects' argument is included
        in the call to EnergyPlus.
        This is the argument for 'Run ExpandObjects prior to simulation'.
        Default is False.
    :type expand_objects: bool
    :param convert: If True, the '--convert' argument is included in the call
        to EnergyPlus. 
        This is the argument for 'Output IDF->epJSON or epJSON->IDF, dependent on
        input file type'.
        Default is False.
    :type convert: bool
    :param readvars: If True, the '--readvars' argument is included in the 
        call to EnergyPlus.
        This is the argument for 'Run ReadVarsESO after simulation'.
        Default is False.
    :type readvars: bool
        
    :returns: A EPResult object which contains the returncode, stdout and a 
        dictionary of the results files.
    :rtype: eprun.epresult.EPResult
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import eprun
       >>> result=eprun(idf_filepath='1ZoneUncontrolled.idf',
       >>>              epw_filepath='USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
       >>>              sim_dir='sim')
       >>> print(type(result))
       <class 'eprun.eprun.EPResult'>
       >>> print(list(result.files.keys()))
       ['audit', 'bnd', 'dxf', 'eio', 'end', 'err', 'eso', 'mdd', 'mtd', 
        'mtr', 'rdd', 'shd', 'csv', 'htm', 'tab', 'txt', 'xml']
               
    .. seealso::
    
       EnergyPlus Essentials, pages 15 and 16.
       https://energyplus.net/quickstart
    
    """
    
    # check if the directory for the simulation exists
    if not sim_dir=='':
        if not os.path.isdir(sim_dir):
            raise Exception('The sim_dir directory does not exist: %s' % sim_dir)
    
    # get absolute filepaths
    idf_absolute_filepath=os.path.abspath(idf_filepath)
    epw_absolute_filepath=os.path.abspath(epw_filepath)
    sim_absolute_dir=os.path.abspath(sim_dir)
    
    # get EnergyPlus exe filepath
    ep_exe=r'%s\EnergyPlus' % ep_dir
    
    # create the Command Prompt string to run EnergyPlus
    st='"%s" %s %s %s -d "%s" -w "%s" "%s"' % (ep_exe,
                                            '-x' if expand_objects else '',
                                            '-c' if convert else '',
                                            '-r' if readvars else '',
                                            sim_absolute_dir,
                                            epw_absolute_filepath,
                                            idf_absolute_filepath
                                            )
    
    # get simulation start time in seconds since the epoch
    simulation_start_time=time.time()
        
    # run EnergyPlus simulation using subprocess.run
    result=subprocess.run(st,capture_output=True)
    
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
    
    

        

                    
        

        
        