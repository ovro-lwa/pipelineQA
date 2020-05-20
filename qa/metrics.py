import numpy as np
from scipy.ndimage import filters
import casatools

tb = casatools.table()

def flagfrac(msfile):
    """ Get fraction of visibilities (crosscorr) that are flagged
    """

    tb.open(msfile, nomodify=False)
    tcross  = tb.query('ANTENNA1!=ANTENNA2')
    flagcol = tcross.getcol('FLAG')
    flagarr = np.rollaxis(flagcol[0,:,:] | flagcol[1,:,:] | flagcol[2,:,:] | flagcol[3,:,:], 1)
    frac = np.count_nonzero(flagarr)/flagarr.size

    return frac
