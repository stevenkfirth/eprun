# -*- coding: utf-8 -*-

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