# -*- coding: utf-8 -*-

import os
import subprocess
import time

        
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
    :rtype: eprun.eprun.EPResult
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import eprun
       >>> result=eprun(idf_filepath='1ZoneUncontrolled.idf',
       >>>              epw_filepath='USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
       >>>              sim_dir='sim')
       >>> print(type(result))
       <class 'eprun.eprun.EPResult'>
       >>> print(result.files)
       {'audit': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.audit', 
        'bnd': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.bnd', 
        'dxf': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.dxf', 
        'eio': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.eio', 
        'end': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.end', 
        'err': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.err', 
        'eso': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.eso', 
        'mdd': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.mdd', 
        'mtd': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.mtd', 
        'mtr': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.mtr', 
        'rdd': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.rdd', 
        'shd': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplusout.shd', 
        'csv': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplustbl.csv', 
        'htm': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplustbl.htm', 
        'tab': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplustbl.tab', 
        'txt': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplustbl.txt', 
        'xml': 'C:\\Users\\cvskf\\OneDrive - Loughborough University\\_Git\\stevenkfirth\\eprun\\tests\\sim\\eplustbl.xml'}
               
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
    
    
class EPResult():
    """A class representing the results of an EnergyPlus simulation.
    
    An EPResult instance is returned as the result of the :py:meth:`~eprun.eprun.eprun` function.
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import eprun
       >>> result=eprun(idf_filepath='1ZoneUncontrolled.idf',
       >>>              epw_filepath='USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
       >>>              sim_dir='sim')
       >>> print(type(result))
       <class 'eprun.eprun.EPResult'>
       >>> print(result.returncode)
       1

    """
    
    @property
    def returncode(self):
        """The returncode of the subprocess.run call to the EnergyPlus exe file.
        This indicates if the call to EnergyPlus was successful.
        0 means success. 1 means failure.
        
        :rtype: int
        """
        return self._returncode
    
    
    @property
    def stdout(self):
        """The stdout of the subprocess.run call to the EnergyPlus exe file.
        This is the text that would appear in the CommandPromt if the command was run there.
        
        :rtype: str
        """
        return self._stdout
    
    
    @property
    def files(self):
        """A dictionary of the results files from a successful EnergyPlus simulation.
        The keys of the dictionary are the file extensions e.g. 'eso', 'err' etc.
        The values of the dictionary are the absolute filepaths of the files.
        
        :rtype: dict
        """
        return self._files
        
        
        
        
        
        
        
        
        
        
        
        