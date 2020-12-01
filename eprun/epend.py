# -*- coding: utf-8 -*-

class EPEnd():
    """A class for an EnergyPlus .end file.
    
    :param fp: The filepath for the .end file.
    :type fp: str
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPRun
       >>> e=EPEnd(fp='eplusout.end')
       >>> print(e.line)
       EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.33sec
    
    .. seealso::
    
       Output Details and Examples, page 125.
       https://energyplus.net/quickstart
    
    """        
    
    def __init__(self,fp):
        ""
        with open(fp,'r') as f:
            self._line=f.readline()
            
    @property
    def line(self):
        """The single line recorded in the .end file.
        
        :rtype: str
        """
        return self._line