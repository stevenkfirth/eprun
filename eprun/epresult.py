# -*- coding: utf-8 -*-

from .epend import EPEnd
from .eperr import EPErr
from .epeso import EPEso


class EPResult():
    """A class representing the results of an EnergyPlus simulation.
    
    .. note::
        
       An EPResult instance is returned as the result of the :py:meth:`~eprun.eprun.eprun` function.
       It should not be instantiated directly.
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import eprun
       >>> result=eprun(idf_filepath='1ZoneUncontrolled.idf',
       >>>              epw_filepath='USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
       >>>              sim_dir='sim')
       >>> print(type(result))
       <class 'eprun.epresult.EPResult'>
       >>> print(result.returncode)
       1

    """
    
    @property
    def files(self):
        """A dictionary of the results files from a successful EnergyPlus simulation.
        The keys of the dictionary are the file extensions e.g. 'eso', 'err' etc.
        The values of the dictionary are the absolute filepaths of the files.
        
        :rtype: dict
        
        """
        return self._files
    
    
    def get_end(self):
        """Gets the .end output file.
        
        :rtype: eprun.eprun.EPEnd        
        
        """
        fp=self.files['end']
        return EPEnd(fp)
    
    
    def get_err(self):
        """Gets the .err output file.
        
        :rtype: eprun.eprun.EPErr        
        
        """
        fp=self.files['err']
        return EPErr(fp)
    
    
    def get_eso(self):
        """Gets the .eso output file.
        
        :rtype: eprun.eprun.EPEso       
        
        """
        fp=self.files['eso']
        return EPEso(fp)
    
    
    @property
    def returncode(self):
        """The returncode of the `subprocess.run <https://docs.python.org/3/library/subprocess.html>`_ call to the EnergyPlus exe file.
        This indicates if the call to EnergyPlus was successful.
        0 means success. 1 means failure.
        
        :rtype: int
        """
        return self._returncode
    
    
    @property
    def stdout(self):
        """The stdout of the `subprocess.run <https://docs.python.org/3/library/subprocess.html>`_ call to the EnergyPlus exe file.
        This is the text that would appear in the CommandPromt if the command was run there.
        
        :rtype: str
        """
        return self._stdout
    
    
    