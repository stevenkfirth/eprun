# -*- coding: utf-8 -*-

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
        lines=[]
        warnings=[]
        
        with open(fp,'r') as f:
            for line in f:
                lines.append(line)
                
                # first line
                if line.startswith('Program Version'):
                    firstline=line
                
                # warning
                if line.startswith('   ** Warning ** '):
                    warnings.append(line[17:])
                    current_message=warnings
                    
                    
                # error message continuation
                if line.startswith('   **   ~~~   ** '):
                    current_message[-1]+=line[17:]
        
        self._firstline=firstline
        self._lastline=line[17:]
        self._lines=lines
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
        
        :rtype: list
        
        """
        return self._lines
        
    
    @property
    def warnings(self):
        """The warnings recorded in the .err file.
        
        :rtype: list
        
        """
        return self._warnings
        
        
        