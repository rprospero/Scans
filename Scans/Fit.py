"""The Fit module holds the Fit class, which defines common parameters
for fitting routines.  It also contains implementations of some common
fits (i.e. Linear and Gaussian).

"""
from abc import ABCMeta, abstractmethod
import numpy as np
from scipy.optimize import curve_fit


class Fit():
    """The Fit class combines the common requirements needed for fitting.
    We need to be able to turn a set of data points into a set of
    parameters, get the simulated curve from a set of parameters, and
    extract usable information from those parameters.
    """

    __metaclass__ = ABCMeta

    def __init__(self, degree, title):
        self.degree = degree
        self.title = title

    @abstractmethod
    def fit(self, x, y):
        """The fit function takes arrays of independent and depedentend
        variables.  It returns a set of parameters in a format that is
        convenient for this specific object.

        """
        return lambda i, j: None

    @abstractmethod
    def get_y(self, x, fit):
        """get_y takes an array of independent variables and a set of model
        parameters and returns the expected dependent variables for
        those parameters

        """
        return lambda i, j: None

    @abstractmethod
    def readable(self, fit):
        """Readable turns the implementation specific set of fit parameters
        into a human readable dictionary.

        """
        return lambda i: {}

    def fit_plot_action(self):
        """
        Create a function to be called in a plotting loop
        to live fit the data

        Returns
        -------
        A function to call in the plotting loop
        """
        def action(x, y, fig, remainder):
            """Fit and plot the data within the plotting loop

            Parameters
            ----------
            x : Array of Float
              The x positions measured thus far
            y : Array of Float
              The y positions measured thus fat
            fig : matplotlib.figure.Figure
              The figure on which to plot
            line : None or maplotlib plot
              If None, the fit hasn't begun plotting yet.  Otherwise, it
              will be an object representing the last line fit.

            Returns
            -------
            line : None or matplotlib plot
              If nothing has been plotted, simply returns None.  Otherwise,
              the plotted line is returned

            """
            if len(x) < self.degree:
                return None
            params = self.fit(x, y)
            fity = self.get_y(x, params)
            if not remainder:
                line = fig.gca().plot(x, fity, "m-",
                                      label="{} fit".format(self.title))[0]
                fig.gca().legend()
            else:
                line, _ = remainder
                line.set_data(x, fity)
            return (line, params)
        return action


class PolyFit(Fit):
    """
    A fitting class for polynomials
    """
    def __init__(self, degree,
                 title=None):
        if title is None:
            title = "Polynomial fit of degree {}".format(degree)
        Fit.__init__(self, degree+1, title)

    def fit(self, x, y):
        return np.polyfit(x, y, self.degree-1)

    def get_y(self, x, fit):
        return np.polyval(fit, x)

    def readable(self, fit):
        if self.degree == 2:
            return {"slope": fit[0], "intercept": fit[1]}
        orders = np.arange(self.degree, 0, -1)
        results = {}
        for key, value in zip(orders, fit):
            results["^{}".format(key)] = value
        return results


class GaussianFit(Fit):
    """
    A fitting class for handling gaussian peaks
    """
    def __init__(self):
        Fit.__init__(self, 4, "Gaussian Fit")

    @staticmethod
    def _gaussian_model(xs, cen, sigma, amplitude, background):
        """
        This is the model for a gaussian with the mean at center, a
        standard deviation of sigma, and a peak of amplitude over a base of
        background.

        """
        return background + amplitude * np.exp(-((xs-cen)/sigma/np.sqrt(2))**2)

    def fit(self, x, y):
        return curve_fit(self._gaussian_model, x, y,
                         [np.mean(x), np.max(x)-np.min(x),
                          np.max(y)-np.min(y), np.min(y)])[0]

    def get_y(self, x, fit):
        return self._gaussian_model(x, *fit)

    def readable(self, fit):
        return {"center": fit[0], "sigma": fit[1],
                "amplitude": fit[2], "background": fit[3]}


#: A linear regression
Linear = PolyFit(1, title="Linear")

#: A gaussian fit
Gaussian = GaussianFit()
