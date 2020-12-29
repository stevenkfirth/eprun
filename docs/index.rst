.. eprun documentation master file, created by
   sphinx-quickstart on Thu Nov 12 05:35:52 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to eprun's documentation!
=================================

`eprun` is a Python package for running EnergyPlus simulations.

Quick Demo
----------

`eprun` uses the :py:meth:`~eprun.eprun.eprun` function to run an EnergyPlus simulation. 
The code below runs an EnergyPlus simulation on an '.idf' input file and an '.epw' weather file.

.. code-block:: python

   >>> from eprun import eprun
   >>> epresult=eprun(ep_dir='C:\EnergyPlusV9-4-0',
   >>>                input_filepath='1ZoneUncontrolled.idf',
   >>>                epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
   >>>                sim_dir='my_results')
   >>> print(type(epresult))
   eprun.epresult.EPResult

We can see that the simulation was successful by looking at the single line '.end' file, 
one of the output files produced by the simulation run.

.. code-block:: python

   >>> print(epresult.get_end().line)
   EnergyPlus Completed Successfully-- 0 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.39sec

The simulation outputs are located in the '.eso' file, another of the simulation output files. 
We can see a summary of the interval (hourly) results in the 'RUN PERIOD 1' section of the '.eso' file by using the
:py:meth:`~eprun.epeso_simulation_environment.EPEsoSimulationEnvironment.get_interval_summary` method:

.. code-block:: python

   >>> print(epresult.get_eso().get_environment('RUN PERIOD 1').get_interval_summary())
   Starts at 2001-01-01T00:00:00+00:00, 8760 periods @ 60 minute intervals
   7 - Environment - Site Outdoor Air Drybulb Temperature (C)
   47 - ZONE ONE - Zone Total Internal Latent Gain Energy (J)
   74 - ZONE ONE - Zone Mean Radiant Temperature (C)
   75 - ZONE ONE - Zone Mean Air Temperature (C)
   76 - ZONE ONE - Zone Air Heat Balance Surface Convection Rate (W)
   77 - ZONE ONE - Zone Air Heat Balance Air Energy Storage Rate (W)

The :py:meth:`~eprun.epeso_interval_variable.EPEsoIntervalVariable.plot` method can be used to create a quick time series plot of the hourly data.
Here the hourly values for the 'ZONE ONE - Zone Mean Air Temperature' variable are shown.

.. code-block:: python

   >>> epresult.get_eso().get_environment('RUN PERIOD 1').get_interval_variable(75).plot()

.. image:: _static/quick_demo.png

The next section gives more details and examples of how to use the `eprun` methods and classes.


.. toctree::
   :maxdepth: 1
   :caption: Start here:
   :hidden:

   Introduction
   Demo - Running an EnergyPlus Simulation
   Demo - Results of a Simulation Run
   Demo - Reading the Output Files
   
.. toctree::
   :maxdepth: 1
   :caption: Tutorials:
   :hidden:
   
   Reading the eso Output File
   
   
.. toctree::
   :maxdepth: 1
   :caption: Reference - Simulation Run:
   :hidden:
   
   eprun
   EPResult

   
.. toctree::
   :maxdepth: 1
   :caption: Reference - Input files:
   :hidden:
   
   EPSchema   
   EPEpJSON

   
.. toctree::
   :maxdepth: 1
   :caption: Reference - Output files:
   :hidden:
   
   EPEnd
   EPErr
   EPEso
   
   
   
..
  Indices and tables
  ==================

  * :ref:`genindex`
  * :ref:`modindex`
  * :ref:`search`
