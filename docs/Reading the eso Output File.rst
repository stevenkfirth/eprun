Reading the eso Output File
===========================

1. Introduction
---------------

The .eso output file of an EnergyPlus simulation contains the main results of the simulation such as the hourly air temperatures or monthly energy consumption. 
The .eso file is a text file in a non-standard format.

Some, but not all, of the contents of a .eso file can be viewed as a .csv file by including the ``--readvars`` argument when running an EnergyPlus simulation.
This runs an additional programme after the main simulation which converts some contents in the .eso file to a .csv file. 

`eprun` provides the :py:class:`~eprun.epeso.EPEso` class to directly read the .eso file and avoid the need for the ``--readvars`` step.

2. Accessing an EPEso object instance
------------------------------------- 

In `eprun` the contents of the .eso file are viewed using the :py:class:`~eprun.epeso.EPEso` class. 
A :py:class:`~eprun.epeso.EPEso` object instance is created from the results of an EnergyPlus simulation run using the :py:meth:`~eprun.eprun.eprun` function.

This tutorial is based on the '1ZoneUncontrolled.idf' EnergyPlus input file which is provided in the 'ExampleFiles' directory of the EnergyPlus install directory.
The simulation is run using the 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw' EnergyPlus weather file.

.. code-block:: python

   >>> from eprun import eprun
   >>> result=eprun(ep_dir=r'C:\EnergyPlusV9-4-0',
   >>>              input_filepath='1ZoneUncontrolled.idf',
   >>>              epw_filepath='USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw',
   >>>              sim_dir='my_results')
   >>> eso=result.get_eso()
   >>> print(type(eso))
   <class 'eprun.epeso.EPEso'>
   
3. Understanding EPEso simulation environments
----------------------------------------------

An EnergyPlus input file can request that a simulation provide results for different 'simulation environments', 
such as a winter design day, a summer design day and a annual run period of hourly data.
The results of these simulation environments are stored in the same .eso file.

In our example, the '1ZoneUncontrolled.idf' contains the instructions for three simulation environments.
These are accessed using the :py:meth:`~eprun.epeso.EPEso.get_environments` method which returns a list of 
:py:class:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment` object instances.

.. code-block:: python

   >>> envs=eso.get_environments()
   >>> print(envs)
   [EPEsoSimuationEnvironment("DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB"),
    EPEsoSimuationEnvironment("DENVER CENTENNIAL  GOLDEN   N ANN CLG 1% CONDNS DB=>MWB"),
    EPEsoSimuationEnvironment("RUN PERIOD 1")]

Each :py:class:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment` object contains a number of properties 
(:py:attr:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.elevation`,
:py:attr:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.environment_title`,
:py:attr:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.latitude`,
:py:attr:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.longitude`,
:py:attr:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.time_zone`)
which hold the meta-data for the environment.

4. Accessing variables
----------------------

An :py:class:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment` object also contains the simulation results. 
These are accessed using different functions based on the reporting interval:

- :py:meth:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.get_interval_data` returns a list of :py:class:`~eprun.epeso_interval_variable.EPEsoIntervalVariable` objects. This often represents hourly data but other intervals are possible.
- :py:meth:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.get_daily_data` returns a list of :py:class:`~eprun.epeso_daily_variable.EPEsoDailyVariable` objects.
- :py:meth:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.get_monthly_data` returns a list of :py:class:`~eprun.epeso_monthly_variable.EPEsoMonthlyVariable` objects.
- :py:meth:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.get_run_period_data` returns a list of :py:class:`~eprun.epeso_runperiod_variable.EPEsoRunPeriodVariable` objects.
- :py:meth:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.get_annual_data` returns a list of :py:class:`~eprun.epeso_annual_variable.EPEsoAnnualVariable` objects.

Continuing our example, we can use the :py:meth:`~eprun.epeso_simulation_environment.EPEsoSimulationEnviroment.get_interval_data` method 
to access the six interval variables for the 'RUN PERIOD 1' simulation environment:

.. code-block:: python

   >>> rp1=envs[2]
   >>> interval_variables=rp1.get_interval_variables()
   >>> print(interval_variables)
   (EPEsoIntervalVariable(sim_env="RUN PERIOD 1", report_code=7),
    EPEsoIntervalVariable(sim_env="RUN PERIOD 1", report_code=47),
    EPEsoIntervalVariable(sim_env="RUN PERIOD 1", report_code=74),
    EPEsoIntervalVariable(sim_env="RUN PERIOD 1", report_code=75),
    EPEsoIntervalVariable(sim_env="RUN PERIOD 1", report_code=76),
    EPEsoIntervalVariable(sim_env="RUN PERIOD 1", report_code=77))

The different variable classes contain different properties and methods to access the data of the different reporting intervals. 
For example, a :py:class:`~eprun.epeso_interval_variable.EPEsoIntervalVariable` object has four properties to enable access to its data:

.. code-block:: python

   >>> iv7=interval_variables[7]
   >>> print(iv7.object_name)
   Environment
   >>> print(iv7.quantity)
   Site Outdoor Air Drybulb Temperature
   >>> print(iv7.unit)
   C
   >>> print(iv7.values[0:20])   # Prints the first 20 values
   (7.0125, 7.2, 6.8875, 6.324999999999999, 5.0375, 4.4, 5.4624999999999995, 5.4125, 6.750000000000001, 
    8.487499999999999, 9.2125, 9.775, 10.375, 10.9125, 12.85, 13.9, 12.15, 11.1, 10.7875, 10.6)   
   


5. Accessing time stamps
------------------------


6. Plotting the data
--------------------



7. Creating a Pandas dataframe
------------------------------











Further resources
-----------------


