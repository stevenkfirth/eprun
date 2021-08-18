Working with Errors
===================

1. Introduction
---------------

Running an EnergyPlus simulation using the `runsim` function has the potential to raise a number of errors. 
These can arise from a variety of sources including user input error for the `runsim` function arguments 
and incorrectly specified EnergyPlus input files.

The sections below demonstrate the different errors which can be encountered. 
This should help in identifying and solving the error. 

A summary of the errors listed below is:

* The `runsim` function will raise a `FileNotFoundError` if the EnergyPlus install directory is specified incorrectly.

* EnergyPlus will run but fail with a `returncode` of '1' and generate no output files if:

   * The input file name is specified incorrectly.
   * The weather file name is specified incorrectly.
   
* EnergyPlus will run but fail with a `returncode` of '1' and generate some output files if:

   * The simulation terminates due to a Fatal Error - such as objects missing from the input file.
   
* EnergyPlus will run successfuly with a `returncode` of '0' and generate all output files if:

   * There are no errors.
   * There are no Fatal Errors but only minor errors such as warnings.




2. Simulation with no errors
----------------------------

This demonstrates a simulation which runs successfully with no errors. 

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
  
Here the 'ep_dir' argument is specified incorrectly, leading to a `FileNotFoundError`.
  
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

Here the 'input_filepath' argument is specified incorrectly, leading to a `returncode` of '1' (fail) and no output files created.
The details of the error are given in the `stdout` property.

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

Here the 'input_filepath' argument is specified incorrectly, leading to a `returncode` of '1' (fail) and no output files created.
The details of the error are given in the `stdout` property.

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

Here the 'sim_dir' argument is specified incorrectly. 
However this leads to a successful EnergyPlus run with a `returncode` of '0' (success).
A new directory named 'simulation_files_ERROR' is created and the simulation output files are placed in this new directory.

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

Here the '1ZoneUncontrolled - EMPTY.idf' file is an empty text file. 
The simulation runs but terminates due to a 'Fatal Error Detected'.
A `returncode` of '1' (fail) is given and some of the output files are created. 
The reason for the error is given by the `EPErr.severes` property.

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

Here the '1ZoneUncontrolled - MINIMUM REQUIRED OBJECTS.idf' file contains the minimum input objects required, a Building object and a GlobalGeometryRules object.
The simulation runs but terminates due to a 'Fatal Error Detected'.
A `returncode` of '1' (fail) is given and some of the output files are created. 
The reason for the error is given by the `EPErr.severes` property.

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

Here a simulation is run with a weather file that doesn't match the location specified in the input .idf file.
The simulation runs successfully with a `returncode` of '0' (success) and all the the output files created.
Although the simulation does work a number of warning errors are reported. These can be seen in the `EPErr.warnings` property.

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




























