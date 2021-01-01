# --- UNDER DEVELOPMENT --- #

# eprun

*eprun* is a Python package for running EnergyPlus simulations.



## Documentation (recommended)

Please see the *eprun* package documentation here: https://eprun.readthedocs.io/en/latest/index.html



## Quick Demo

*eprun* uses the [`eprun`] function to run an EnergyPlus simulation. 
The code below runs an EnergyPlus simulation on an '.idf' input file and an '.epw' weather file.

```python
>>> from eprun import eprun
>>> epresult=eprun(ep_dir='C:\EnergyPlusV9-4-0',
>>>          input_filepath='1ZoneUncontrolled.idf',
>>>          epw_filepath='USA_CO_Golden-NREL.724666_TMY3.epw',
>>>          sim_dir='simulation_results')
>>> print(type(epresult))
```

```
<class 'eprun.epresult.EPResult'>
```



We can see that the simulation was successful by looking at the single line '.end' file, 
one of the output files produced by the simulation run.

```python
>>> print(epresult.get_end().line)
```

```
EnergyPlus Completed Successfully-- 0 Warning; 0 Severe Errors; Elapsed Time=00hr 00min  2.39sec
```



The simulation outputs are located in the '.eso' file, another of the simulation output files. 
We can see a summary of the interval (hourly) results in the 'RUN PERIOD 1' section of the '.eso' file by using the `get_interval_summary` method:

```python
>>> print(epresult.get_eso().get_environment('RUN PERIOD 1').get_interval_summary())
```

```
Starts at 2001-01-01T00:00:00+00:00, 8760 periods @ 60 minute intervals
7 - Environment - Site Outdoor Air Drybulb Temperature (C)
47 - ZONE ONE - Zone Total Internal Latent Gain Energy (J)
74 - ZONE ONE - Zone Mean Radiant Temperature (C)
75 - ZONE ONE - Zone Mean Air Temperature (C)
76 - ZONE ONE - Zone Air Heat Balance Surface Convection Rate (W)
77 - ZONE ONE - Zone Air Heat Balance Air Energy Storage Rate (W)
```



The `plot` method can be used to create a quick time series plot of the hourly data.
Here the hourly values for the 'ZONE ONE - Zone Mean Air Temperature' variable are shown.

```python
>>> epresult.get_eso().get_environment('RUN PERIOD 1').get_interval_variable(75).plot()
```

![alt text](docs/_static/quick_demo.png)


## Further resources

* The [Running an EnergyPlus simulation on the 1ZoneUncontrolled file]  Jupyter Notebook shows the `eprun` function in action.
* The [Examples] folder with further examples using Jupyter Notebooks.

[`eprun`]: https://eprun.readthedocs.io/en/latest/eprun_function.html

[Running an EnergyPlus simulation on the 1ZoneUncontrolled file]: https://nbviewer.jupyter.org/github/stevenkfirth/eprun/blob/main/examples/Running%20an%20EnergyPlus%20simulation%20on%20the%201ZoneUncontrolled%20file/Running%20an%20EnergyPlus%20simulation%20on%20the%201ZoneUncontrolled%20file.ipynb

[Examples]: https://nbviewer.jupyter.org/github/stevenkfirth/eprun/tree/main/examples/

