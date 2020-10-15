import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from scipy.ndimage import filters
import casatools
import os.path

tb = casatools.table()
ms = casatools.ms()


nall2nant = lambda nall: max(np.round(np.roots([1/2., 1/2., -nall]), 0).astype(int)) # nant calc from cross+auto

def corr_flagfrac(msfile, showplot=False, saveplot=False):
    """ Make matrix plot of flagging fraction of cross corrlations
    """

    ms.open(msfile)
    nspw = len(ms.getspectralwindowinfo())
    ms.close()

    tb.open(msfile, nomodify=True)

    flagcol = tb.getcol('FLAG')
    npol, nchan, nblnspw = flagcol.shape
    nall = nblnspw//nspw
    nant = nall2nant(nall)
    print('Data shape: {0} bls, {1} ants, {2} chans/spw, {3} spw, {4} pol'
          .format(nall, nant, nchan, nspw, npol))

    flagmat = np.zeros((nant, nant, nchan, npol), dtype=bool)
    ant1, ant2 = np.triu_indices(nant)
    flagcol = flagcol.transpose()
    for ind in range(len(ant1)):
        flagmat[ant1[ind], ant2[ind]] = flagcol[ind]
    corrmat = flagmat.reshape(nant, nant, -1)
    corrmat_frac = np.sum(corrmat, axis=2)/corrmat.shape[2]

    # plot
    if showplot or saveplot:
        im = plt.matshow(corrmat_frac, norm=LogNorm(vmin=1.e-4, vmax=1))
        plt.colorbar(im)
        if showplot:
            plt.show()
        elif saveplot:
            plt.savefig('corrmat.png')

    tb.close()

    return corrmat_frac
