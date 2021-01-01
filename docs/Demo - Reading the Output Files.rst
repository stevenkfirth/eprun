Demo - Reading the Output Files
===============================

A successful EnergyPlus simulation run will generate a series of EnergyPlus output files. 

.. code-block:: python
   :lineno-start: 1

   >>> from eprun import eprun
   >>> result=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>              input_filepath='1ZoneUncontrolled.idf',
   >>>              epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
   >>>              sim_dir='simulation_results')
   >>> print(type(epresult))
   <class 'eprun.epresult.EPResult'>
   >>> print(list(epresult.files.keys()))      # This prints the output file extensions
   ['audit', 'bnd', 'dxf', 'eio', 'end', 'err', 'eso', 'mdd', 'mtd', 'mtr', 
    'rdd', 'shd', 'csv', 'htm', 'tab', 'txt', 'xml']
   
The EnergyPlus output files are text files and can be read with the Python built-in `open` method.
However the format of the text files is non-standard so additional processing is almost always required.

*eprun* contains the following classes for reading EnergyPlus output files:

* `EPEnd` for reading '.end' files.
* `EPErr` for reading '.err' files.
* `EPEso` for reading '.eso' files.

These classes can be created directly or by using the ``get_[output_file_extension]`` methods of the `EPResult` object.

The simplest output file is the '.end' file which contains a single line of information. 
This is accessed using the `get_end` method which returns a `EPEnd` object instance.

.. code-block:: python
   :lineno-start: 11

   >>> end=epresult.get_end()
   >>> print(type(end))
   <class 'eprun.epend.EPEnd'>
   >>> print(end.line)   # The single line of the file
   EnergyPlus Completed Successfully-- 0 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.21sec

A slightly more complex output file is the '.err' file which records an errors encountered during the simulation run.
This is accessed using the `get_err` method which returns a `EPErr` object instance.

.. code-block:: python
   :lineno-start: 16

   >>> err=epresult.get_err()
   >>> print(type(err))
   <class 'eprun.eperr.EPErr'>
   >>> for line in err.lines: print(line, end='')      # Prints all lines in the file 
   Program Version,EnergyPlus, Version 9.4.0-998c4b761e, YMD=2020.12.31 08:53,
      ************* Testing Individual Branch Integrity
      ************* All Branches passed integrity testing
      ************* Testing Individual Supply Air Path Integrity
      ************* All Supply Air Paths passed integrity testing
      ************* Testing Individual Return Air Path Integrity
      ************* All Return Air Paths passed integrity testing
      ************* No node connection errors were found.
      ************* Beginning Simulation
      ************* Simulation Error Summary *************
      ************* EnergyPlus Warmup Error Summary. During Warmup: 0 Warning; 0 Severe Errors.
      ************* EnergyPlus Sizing Error Summary. During Sizing: 0 Warning; 0 Severe Errors.
      ************* EnergyPlus Completed Successfully-- 0 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.21sec

Another output file is the '.eso' file which contains the results of the simulation calculations. 
Instructions on how to view these results is described in the tutorial `Reading the eso Output File`.

Congratulations! You now know how to run an EnergyPlus simulation using the `eprun` function
and how to access the simulation results and output files using the `EPResult` class.

.. The next section looks further at these topics with in-depth tutorials on working with Energy Plus simulations, input files and output files.

Further resources
-----------------

* The documentation for:

   * the `EPResult class <EPResult_class>`
   * the `EPEnd class <EPEnd_class>`
   * the `EPErr class <EPErr_class>`
   * the `EPEso class <EPEso_class>`
  
* The '`Viewing the results of the 1ZoneUncontrolled simulation run`_' Jupyter Notebook shows the EPResult class in action.
* The EnergyPlus QuickStart guide: https://energyplus.net/quickstart
* Section '3.8 What Are All These Output Files?' in the `EnergyPlus Essentials`_ documentation.

.. _Viewing the results of the 1ZoneUncontrolled simulation run: https://nbviewer.jupyter.org/github/stevenkfirth/eprun/blob/main/examples/Viewing%20the%20results%20of%20the%201ZoneUncontrolled%20simulation%20run/Viewing%20the%20results%20of%20the%201ZoneUncontrolled%20simulation%20run.ipynb
.. _EnergyPlus Essentials: https://energyplus.net/quickstart#reading

