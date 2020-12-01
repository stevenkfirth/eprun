# -*- coding: utf-8 -*-

class EPErr():
    """A class for an EnergyPlus .err file.
    
    :param fp: The filepath for the .err file.
    :type fp: str
    
    :Example:
        
    .. code-block:: python
           
       >>> from eprun import EPErr
       >>> e=EPErr(fp='eplusout.err')
       >>> print(len(e.warnings))
       3
       >>> print(e.warnings[0])
       Weather file location will be used rather than entered (IDF) Location object.
       ..Location object=DENVER CENTENNIAL  GOLDEN   N_CO_USA DESIGN_CONDITIONS
       ..Weather File Location=San Francisco Intl Ap CA USA TMY3 WMO#=724940
       ..due to location differences, Latitude difference=[2.12] degrees, Longitude difference=[17.22] degrees.
       ..Time Zone difference=[1.0] hour(s), Elevation difference=[99.89] percent, [1827.00] meters.
    
    .. seealso::
    
       Output Details and Examples, page 125.
       https://energyplus.net/quickstart
    
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
        
        
        