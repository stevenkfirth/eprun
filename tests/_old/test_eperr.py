# -*- coding: utf-8 -*-

import unittest
from eprun import EPErr


class Test_EPErr(unittest.TestCase):
   
        
    def test_EPErr(self):
        ""
        err=EPErr(fp=r'files\eplusout.err')
        self.assertEqual(str(type(err)),
                         "<class 'eprun.eperr.EPErr'>")
        
        
    def test_firstline(self):
        ""
        err=EPErr(fp=r'files\eplusout.err')
        self.assertEqual(err.firstline.strip(),
                         'Program Version,EnergyPlus, Version 9.4.0-998c4b761e, YMD=2020.11.13 06:25,')
        
        
    def test_lastline(self):
        ""
        err=EPErr(fp=r'files\eplusout.err')
        self.assertEqual(err.lastline.strip(),
                         'EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.33sec')
        
        
    def test_lines(self):
        ""
        err=EPErr(fp=r'files\eplusout.err')
        self.assertEqual(err.lines.encode(),
                         b'Program Version,EnergyPlus, Version 9.4.0-998c4b761e, YMD=2020.11.13 06:25,\n   ** Warning ** Weather file location will be used rather than entered (IDF) Location object.\n   **   ~~~   ** ..Location object=DENVER CENTENNIAL  GOLDEN   N_CO_USA DESIGN_CONDITIONS\n   **   ~~~   ** ..Weather File Location=San Francisco Intl Ap CA USA TMY3 WMO#=724940\n   **   ~~~   ** ..due to location differences, Latitude difference=[2.12] degrees, Longitude difference=[17.22] degrees.\n   **   ~~~   ** ..Time Zone difference=[1.0] hour(s), Elevation difference=[99.89] percent, [1827.00] meters.\n   ** Warning ** SetUpDesignDay: Entered DesignDay Barometric Pressure=81198 differs by more than 10% from Standard Barometric Pressure=101301.\n   **   ~~~   ** ...occurs in DesignDay=DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB, Standard Pressure (based on elevation) will be used.\n   ** Warning ** SetUpDesignDay: Entered DesignDay Barometric Pressure=81198 differs by more than 10% from Standard Barometric Pressure=101301.\n   **   ~~~   ** ...occurs in DesignDay=DENVER CENTENNIAL  GOLDEN   N ANN CLG 1% CONDNS DB=>MWB, Standard Pressure (based on elevation) will be used.\n   ************* Testing Individual Branch Integrity\n   ************* All Branches passed integrity testing\n   ************* Testing Individual Supply Air Path Integrity\n   ************* All Supply Air Paths passed integrity testing\n   ************* Testing Individual Return Air Path Integrity\n   ************* All Return Air Paths passed integrity testing\n   ************* No node connection errors were found.\n   ************* Beginning Simulation\n   ************* Simulation Error Summary *************\n   ************* EnergyPlus Warmup Error Summary. During Warmup: 0 Warning; 0 Severe Errors.\n   ************* EnergyPlus Sizing Error Summary. During Sizing: 0 Warning; 0 Severe Errors.\n   ************* EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.33sec\n')
        
        
    def test_severes(self):
        ""
        err=EPErr(fp=r'files\eplusout-SEVERE.err')
        self.assertEqual(err.severes,
                         ["<root> - Object required to validate 'required' properties."])
        
        
    def test_warnings(self):
        ""
        err=EPErr(fp=r'files\eplusout.err')
        self.assertEqual(err.warnings[0].encode(),
                         b'Weather file location will be used rather than entered (IDF) Location object. ..Location object=DENVER CENTENNIAL  GOLDEN   N_CO_USA DESIGN_CONDITIONS ..Weather File Location=San Francisco Intl Ap CA USA TMY3 WMO#=724940 ..due to location differences, Latitude difference=[2.12] degrees, Longitude difference=[17.22] degrees. ..Time Zone difference=[1.0] hour(s), Elevation difference=[99.89] percent, [1827.00] meters.')
    
    
if __name__=='__main__':
    
    unittest.main(Test_EPErr())

