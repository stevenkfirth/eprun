# -*- coding: utf-8 -*-


class EPEsoAnnualVariable():
    """A class for an annual variable recorded in a EPEsoSimulationEnviroment instance.
    """
    
    def __repr__(self):
        ""
        return 'EPEsoAnnualVariable(sim_env="%s", report_code=%s)' % (self._epesose.environment_title,
                                                                       self._report_code)
