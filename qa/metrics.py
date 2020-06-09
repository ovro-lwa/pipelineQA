import numpy as np
from scipy.ndimage import filters
import casatools
import os.path

tb = casatools.table()

def flagfrac(msfile):
    """ Get fraction of visibilities (crosscorr) that are flagged
    """

    if not os.path.exists(msfile):
        logger.warn('File {0} not found'.format(msfile))
        return None

    tb.open(msfile, nomodify=True)
    tcross  = tb.query('ANTENNA1!=ANTENNA2')
    flagcol = tcross.getcol('FLAG')
    flagarr = np.rollaxis(flagcol[0,:,:] | flagcol[1,:,:] | flagcol[2,:,:] | flagcol[3,:,:], 1)
    frac = np.count_nonzero(flagarr)/flagarr.size

    return frac


def flagfrac_chans(msfile):
    """ Get fraction of visibilities (crosscorr) that are flagged per channel
    """

    if not os.path.exists(msfile):
        logger.warn('File {0} not found'.format(msfile))
        return None

    tb.open(msfile, nomodify=True)
    tcross  = tb.query('ANTENNA1!=ANTENNA2')
    flagcol = tcross.getcol('FLAG')
    flagarr = np.rollaxis(flagcol[0,:,:] | flagcol[1,:,:] | flagcol[2,:,:] | flagcol[3,:,:], 1)
    frac = [np.count_nonzero(flagarr[:,i])/flagarr[:,i].size for i in range(len(flagarr[0]))]

    return frac
