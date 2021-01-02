# -*- coding: utf-8 -*-

from .epend import EPEnd
from .eperr import EPErr
from .epeso import EPEso


class EPResult():
    """A class representing the results of an EnergyPlus simulation.
    
    .. note::
        
       An EPResult instance is returned as the result of the `eprun` function.
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
    
    
    