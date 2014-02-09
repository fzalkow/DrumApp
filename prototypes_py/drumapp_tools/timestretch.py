import numpy
import utils
from scipy.interpolate import interp1d

def simple_stretcher(array, factor):
    """ time stretch by simply interpolating the audio signal linear """
    l = len(array)
    x = numpy.linspace(0.0, 1.0, l)
    f = interp1d(x, array, bounds_error=False, fill_value=0)#, bounds_error=False, fill_value=0)#, kind="cubic")
    newx = numpy.linspace(0.0, 1.0, int(round(factor*l)))
    return utils.numpy_to_chunks(numpy.int16(f(newx)))
