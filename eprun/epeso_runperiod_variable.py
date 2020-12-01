# -*- coding: utf-8 -*-



class EPEsoRunPeriodVariable():
    """A class for a run period variable recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoRunPeriodVariable(sim_env="%s", report_code=%s)' % (self._epesose.environment_title,
                                                                       self._report_code)
