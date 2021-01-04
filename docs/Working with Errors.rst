Working with Errors
===================

1. Introduction
---------------



In summary:

* The `eprun` function will raise a `FileNotFoundError` if the EnergyPlus install directory is specified incorrectly.

* EnergyPlus will run but fail with a `returncode` of '1' if:

   * The input file name is specified incorrectly.
   * The weather file name is specified incorrectly.
   * The simulation terminates due to a Fatal Error - such as objects missing from the input file.
   
* EnergyPlus will run successfuly with a `returncode` of '0' if:

   * There are no errors.
   * There are no Fatal Errors but only minor errors such as warnings.




2. Simulation with no errors
----------------------------

.. code-block:: python

   >>> from eprun import eprun
   >>> epresult=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>                input_filepath='1ZoneUncontrolled.idf',
   >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
   >>>                sim_dir='simulation_files')
   >>> print('returncode:', epresult.returncode)
   returncode: 0
   >>> print('end.line:', epresult.get_end().line)
   end.line: EnergyPlus Completed Successfully-- 0 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  3.61sec



3. Simulation with the EnergyPlus install directory not specified correctly
---------------------------------------------------------------------------
   
.. code-block:: python

   >>> from eprun import eprun
   >>> try:
   >>>    epresult=eprun(ep_dir=r'C:\EnergyPlusV9-4-0_ERROR',
   >>>                   input_filepath='1ZoneUncontrolled.idf',
   >>>                   epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
   >>>                   sim_dir='simulation_files')
   >>> except FileNotFoundError:
   >>>    print('FileNotFoundError error raised')
   FileNotFoundError error raised
   


4. Simulation with the input file name not specified correctly
--------------------------------------------------------------

.. code-block:: python

   >>> from eprun import eprun
   >>> epresult=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>                input_filepath='1ZoneUncontrolled_ERROR.idf',
   >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
   >>>                sim_dir='simulation_files')
   >>> print('returncode:', epresult.returncode)
   returncode: 1
   >>> print('stdout:',epresult.stdout[:39])      #  full string truncated to avoid printing local file path on the author's PC
   stdout: ERROR: Could not find input data file: 
   >>> try:
   >>>     print('end.line:', epresult.get_end().line)
   >>> except KeyError:
   >>>     print('KeyError raised')      # occurs if the '.end' file was not created by the simulation
   KeyError raised



5. Simulation with the weather file name not specified correctly
----------------------------------------------------------------

.. code-block:: python

   >>> from eprun import eprun
   >>> epresult=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>                input_filepath='1ZoneUncontrolled.idf',
   >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3_ERROR.epw',
   >>>                sim_dir='simulation_files')
   >>> print('returncode:', epresult.returncode)
   returncode: 1
   >>> print('stdout:',epresult.stdout[:36])      #  full string truncated to avoid printing local file path on the author's PC
   stdout: ERROR: Could not find weather file: 
   >>> try:
   >>>     print('end.line:', epresult.get_end().line)
   >>> except KeyError:
   >>>     print('KeyError raised')      # occurs if the '.end' file was not created by the simulation
   KeyError raised



5. Simulation with the simulation directory name not specified correctly
------------------------------------------------------------------------

.. code-block:: python

   >>> from eprun import eprun
   >>> epresult=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>                input_filepath='1ZoneUncontrolled.idf',
   >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
   >>>                sim_dir='simulation_files_ERROR')
   >>> print('returncode:', epresult.returncode)
   returncode: 0
   >>> print('end.line:', epresult.get_end().line)
   end.line: EnergyPlus Completed Successfully-- 0 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  3.29sec



6. Simulation with an empty input file
--------------------------------------

.. code-block:: python

   >>> from eprun import eprun
   >>> epresult=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>                input_filepath='1ZoneUncontrolled - EMPTY.idf',
   >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
   >>>                sim_dir='simulation_files')
   >>> print('returncode:', epresult.returncode)
   returncode: 1
   >>> print('end.line:', epresult.get_end().line)
   end.line: EnergyPlus Terminated--Fatal Error Detected. 0 Warning; 1 Severe Errors; Elapsed Time=00hr 00min  0.39sec
   >>> print('err.severes:', epresult.get_err().severes)
   err.severes: ["<root> - Object required to validate 'required' properties."]



7. Simulation with input file with required objects only
--------------------------------------------------------

.. code-block:: python

   >>> from eprun import eprun
   >>> epresult=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>                input_filepath='1ZoneUncontrolled - MINIMUM REQUIRED OBJECTS.idf',
   >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
   >>>                sim_dir='simulation_files')
   >>> print('returncode:', epresult.returncode)
   returncode: 1
   >>> print('end.line:', epresult.get_end().line)
   end.line: EnergyPlus Terminated--Fatal Error Detected. 1 Warning; 1 Severe Errors; Elapsed Time=00hr 00min  0.52sec
   >>> print('err.severes:', epresult.get_err().severes)
   err.severes: ['GetNextEnvironment: No Design Days or Run Period(s) specified, program will terminate.']



8. Simulation with warning errors only
--------------------------------------

.. code-block:: python

   >>> from eprun import eprun
   >>> epresult=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>                input_filepath='1ZoneUncontrolled.idf',
   >>>                epw_filepath='USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
   >>>                sim_dir='simulation_files')
   >>> print('returncode:', epresult.returncode)
   returncode: 0
   >>> print('end.line:', epresult.get_end().line)
   end.line: EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  3.45sec
   >>> for w in epresult.get_err().warnings: print('err.warning:', w)
   err.warning: Weather file location will be used rather than entered (IDF) Location object. ..Location object=DENVER CENTENNIAL  GOLDEN   N_CO_USA DESIGN_CONDITIONS ..Weather File Location=San Francisco Intl Ap CA USA TMY3 WMO#=724940 ..due to location differences, Latitude difference=[2.12] degrees, Longitude difference=[17.22] degrees. ..Time Zone difference=[1.0] hour(s), Elevation difference=[99.89] percent, [1827.00] meters.
   err.warning: SetUpDesignDay: Entered DesignDay Barometric Pressure=81198 differs by more than 10% from Standard Barometric Pressure=101301. ...occurs in DesignDay=DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB, Standard Pressure (based on elevation) will be used.
   err.warning: SetUpDesignDay: Entered DesignDay Barometric Pressure=81198 differs by more than 10% from Standard Barometric Pressure=101301. ...occurs in DesignDay=DENVER CENTENNIAL  GOLDEN   N ANN CLG 1% CONDNS DB=>MWB, Standard Pressure (based on elevation) will be used.




























