if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from Scans.Instrument import scan, THETA, pol_measure
from Scans.Fit import DampedOscillator


currents = scan(THETA, start=-3, stop=2, stride=0.1).and_back.forever
result = currents.fit(DampedOscillator, frames=100,
                detector=pol_measure)
THETA(result["center"])
print(THETA)