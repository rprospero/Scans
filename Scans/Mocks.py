"""This module exists to make mock version of the beamline

This module creates mocks to handle classes that may not be available
on development or testing machines.
"""

from time import sleep
from mock import Mock
import numpy as np
from .Instrument import THETA

g = Mock()
g.period = 0
g.frames = 0
g.get_period = lambda: g.period
g.get_frames = lambda: g.frames


def fake_spectrum(channel, period):
    """Create a fake intensity spectrum."""
    if channel == 1:
        return {"signal": np.zeros(1000)+1}
    x = np.arange(1000)
    base = np.cos(0.01*(THETA()+1.05)*x)+1
    if period % 2 == 0:
        base = 2 - base
    base *= 100000
    base += np.sqrt(base) * (2 * np.random.rand(1000) - 1)
    base /= x
    sleep(0.1)
    return {"signal": base}


g.get_spectrum = fake_spectrum

lm = Mock()
