Demo - Reading the Output Files
===============================

A successful EnergyPlus simulation run will generate a series of EnergyPlus output files. 

.. code-block:: python

   >>> from eprun import eprun
   >>> result=eprun(ep_dir='C:\EnergyPlusV9-4-0',
   >>>              input_filepath='1ZoneUncontrolled.idf',
   >>>              epw_filepath='USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
   >>>              sim_dir='my_results')
   >>> print(type(result))
   eprun.epresult.EPResult
   >>> print(list(result.files.keys()))   # This prints the output file extensions
   ['audit', 'bnd', 'dxf', 'eio', 'end', 'err', 'eso', 'mdd', 'mtd', 'mtr', 
    'rdd', 'shd', 'csv', 'htm', 'tab', 'txt', 'xml']
   
The EnergyPlus output files are text files and can be read with the Python built-in *open* method.
However the format of the text files is non-standard so additional processing is almost always required.

`eprun` provides a series of classes for viewing the contents of the EnergyPlus output files.
These classes are accessed using the ``get_`` methods of the :py:class:`~eprun.epresult.EPResult` object.

The simplest output file is the '.end' file which contains a single line of information. 
This is accessed using the :py:meth:`~eprun.epresult.EPResult.get_end` method which
returns a :py:class:`~eprun.epend.EPEnd` object instance.

.. code-block:: python

   >>> e=result.get_end()
   >>> print(type(e))
   eprun.epend.EPEnd
   >>> print(e.line)   # The single line of the file
   EnergyPlus Completed Successfully-- 3 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.28sec

A slightly more complex output file is the '.err' file which records an errors encountered during the simulation run.
This is accessed using the :py:meth:`~eprun.epresult.EPResult.get_err` method which
returns a :py:class:`~eprun.eperr.EPErr` object instance.

.. code-block:: python

   >>> e=result.get_err()
   >>> print(type(e))
   eprun.eprr.EPErr
   >>> print(len(e.warnings))  # The number of warnings in the .err file. 
   3
   >>> print(e.warnings[0])   # Prints the first warning in the .err file.
   Weather file location will be used rather than entered (IDF) Location object.
   ..Location object=DENVER CENTENNIAL  GOLDEN   N_CO_USA DESIGN_CONDITIONS
   ..Weather File Location=San Francisco Intl Ap CA USA TMY3 WMO#=724940
   ..due to location differences, Latitude difference=[2.12] degrees, Longitude difference=[17.22] degrees.
   ..Time Zone difference=[1.0] hour(s), Elevation difference=[99.89] percent, [1827.00] meters.
    
`eprun` contains the following classes for reading EnergyPlus output files:

- :py:class:`~eprun.epend.EPEnd` for reading '.end' files.
- :py:class:`~eprun.eperr.EPErr` for reading '.err' files.
- :py:class:`~eprun.epeso.EPEso` for reading '.eso' files.

Congratulations! You now know how to run an EnergyPlus simulation using the :py:meth:`~eprun.eprun.eprun` function
and how to access the simulation results and output files using the :py:class:`~eprun.epresult.EPResult` class.
The next section looks further at these topics with in-depth tutorials on working with Energy Plus simulations, input files and output files.

Further resources
-----------------

- The documentation for the :py:class:`~eprun.epresult.EPResult` class.
- This Jupyter Notebook shows the `EPResult` class in action.
- A video tutorial of the `EPResult` class: #### TO DO ###

