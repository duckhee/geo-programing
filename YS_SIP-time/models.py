import numpy as np
import pygimli as pg

from scipy.special import gamma


def modelColeColeTD(t, eta0, tau, c):
    sigma = 0
    for n in range(0, 300):
        t1 = (-1)**n * (t / tau) ** (n * c)
        t2 = gamma(1 + n * c)
        sigma += t1 / t2

    return eta0 * sigma


class ColeColeTD(pg.core.ModellingBase):
    def __init__(self, t, verbose=False):
        super(ColeColeTD, self).__init__(verbose)
        self.t_ = t  # save times
        self.setMesh(pg.meshtools.createMesh1D(1, 3))  # 3 single parameters

    def response(self, par):
        """phase angle of the model"""
        return modelColeColeTD(self.t_, par[0], par[1], par[2])


def fitCCTD(times, data, error=0.01, lam=10., tau_param=(100, 1e-1, 100), c_param=(0.5, 0, 1)):

    # tLog = pg.trans.TransLog()

    fCC = ColeColeTD(times)
    fCC.region(0).setStartValue(max(data))
    fCC.region(1).setParameters(*tau_param)
    fCC.region(2).setParameters(*c_param)

    ICC = pg.core.Inversion(data, fCC, False)  # set up inversion class
    # ICC.setTransModel(tLog)
    ICC.setAbsoluteError(data*error+max(data)*0.0001)  # perr + ePhi/data)
    ICC.setLambda(lam)  # start with large damping and cool later
    ICC.setMarquardtScheme(0.8)  # lower lambda by 20%/it., no stop chi=1

    model = np.asarray(ICC.run())  # run inversion
    ICC.echoStatus()
    response = np.asarray(ICC.response())

    return model, response
