import numpy as np
from scipy.ndimage import filters
import casatools
import os.path

tb = casatools.table()

def corr_mat_plot(msfile):
    """ Make matrix plot of flagging fraction of cross corrlations
    NEEDS TESTING
    """

    with tb.table(msfile, readonly=True) as t:
        flagcol = t.getcol('FLAG')

    flagmat = np.zeros((256,256,554,109,4), dtype=bool)
    tiuinds = np.triu_indices(256)
    flagmat[tiuinds] = flagcol.reshape(554, 32896, 109, 4).transpose(1,0,2,3)
    corrmat = flagmat.reshape(256,256,-1)
    corrmat_frac = np.sum(corrmat, axis=2)/corrmat.shape[2]
    # plot
    im = p.matshow(corrmat_frac, norm=LogNorm(vmin=1.e-4, vmax=1))
    p.colorbar(im)
    p.show()

    return corrmat_frac
