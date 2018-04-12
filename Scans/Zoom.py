"""Default class and utilities for Zoom

All the scanning code specific to the Zoom instrument is
contained in this module

"""
from __future__ import print_function
try:
    # pylint: disable=import-error
    from genie_python import genie as g
except ImportError:
    g = None
from .Defaults import Defaults
from .Motion import populate
from .Monoid import Sum
from .Util import make_scan, make_estimator


def zoom_monitor(spectrum):
    """A generating function for detectors for monitor spectra"""
    def monitor(**kwargs):
        """A simple detector for monitor number {}""".format(spectrum)
        g.begin()
        g.waitfor(**kwargs)
        spec = g.get_spectrum(spectrum)
        while not spec:
            spec = g.get_spectrum(spectrum)
        temp = sum(spec["signal"])
        g.abort()
        return Sum(temp)
    return monitor


class Zoom(Defaults):
    """
    This class represents the default functions for the Zoom instrument.
    """

    @staticmethod
    def measure(title, position, **kwargs):
        g.change_title(title.format(**position))
        g.begin()
        g.waitfor(**kwargs)
        g.end()

    detector = zoom_monitor(4)

    @staticmethod
    def time_estimator(**kwargs):
        # Double check this value
        monitor_count_rate = 1e6
        return make_estimator(monitor_count_rate)(**kwargs)

    @staticmethod
    def log_file():
        from datetime import datetime
        now = datetime.now()
        return "U:/zoom_scan_{}_{}_{}_{}_{}_{}.dat".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

    def __repr__(self):
        return "Zoom()"


scan = make_scan(Zoom())
populate()
monitor1 = zoom_monitor(1)
monitor2 = zoom_monitor(2)
monitor3 = zoom_monitor(3)
monitor4 = zoom_monitor(4)
