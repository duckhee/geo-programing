# -*- coding: utf-8 -*-
import sys
import codecs
import pylab as P

from math import pi, log10, exp
import numpy as np
import pygimli as pg
from scipy.special import gamma
from pygimli.utils import isComplex, squeezeComplex, toComplex, KramersKronig, rndig

from pygimli.frameworks import MethodManager
from pygimli.frameworks import ParameterModelling


def ColeColeRho(f, rho, m, tau, c, a=1):
    pg.deprecated("Please use modelColeColeRho instead of ColeColeRho.")
    return modelColeColeRho(f, rho, m, tau, c, a)


def modelColeColeRho(f, rho, m, tau, c, a=1):
    r"""Frequency-domain Cole-Cole impedance model after Pelton et al. (1978)
    Frequency-domain Cole-Cole impedance model after Pelton et al. (1978)
    :cite:`PeltonWarHal1978`
    .. math::
        Z(\omega) & = \rho_0\left[1 - m \left(1 -
        \frac{1}{1+(\text{i}\omega\tau)^c}\right)\right] \\
        \quad \text{with}\quad m & = \frac{1}{1+\frac{\rho_0}{\rho_1}} \quad
        \text{and}\quad \omega =2\pi f
    * :math:`Z(\omega)` - Complex impedance per 1A current injection
    * :math:`f` - Frequency
    * :math:`\rho_0` -- Background resistivity states the unblocked pore path
    * :math:`\rho_1` -- Resistance of the solution in the blocked pore passages
    * :math:`m` -- Chargeability after Seigel (1959) :cite:`Seigel1959` as
      being the ratio of voltage immediately after, to the voltage immediately
      before cessation of an infinitely long charging current.
    * :math:`\tau` --
      'Time constant' relaxation time [s] for 1/e decay
    * :math:`c` - Rate of charge accumulation.
      Cole-Cole exponent typically [0.1 .. 0.6]
    Examples
    --------
    
    >>> import numpy as np
    >>> import pygimli as pg
    >>> from pygimli.physics.SIP import modelColeColeRho
    >>> f = np.logspace(-2, 5, 100)
    >>> m = np.linspace(0.1, 0.9, 5)
    >>> tau = 0.01
    >>> fImMin = 1/(tau*2*np.pi)
    >>> fig, axs = pg.plt.subplots(1, 2)
    >>> ax1 = axs[0]
    >>> ax2 = axs[0].twinx()
    >>> ax3 = axs[1]
    >>> ax4 = axs[1].twinx()
    >>> for i in range(len(m)):
    ...     Z = ColeColeRho(f, rho=1, m=m[i], tau=tau, c=0.5)
    ...     _= ax1.loglog(f, np.abs(Z), color='black')
    ...     _= ax2.loglog(f, -np.angle(Z)*1000, color='b')
    ...     _= ax3.loglog(f, Z.real, color='g')
    ...     _= ax4.semilogx(f, Z.imag, color='r')
    ...     _= ax4.plot([fImMin, fImMin], [-0.2, 0.], color='r')
    >>> _= ax4.text(fImMin, -0.1, r"$f($min($Z''$))=$\frac{1}{2*\pi\tau}$", color='r')
    >>> _= ax4.text(0.1, -0.17, r"$f($min[$Z''$])=$\frac{1}{2\pi\tau}$", color='r')
    >>> _= ax1.set_ylabel('Amplitude $|Z(f)|$', color='black')
    >>> _= ax1.set_xlabel('Frequency $f$ [Hz]')
    >>> _= ax1.set_ylim(1e-2, 1)
    >>> _= ax2.set_ylabel(r'- Phase $\varphi$ [mrad]', color='b')
    >>> _= ax2.set_ylim(1, 1e3)
    >>> _= ax3.set_ylabel('re $Z(f)$', color='g')
    >>> _= ax4.set_ylabel('im $Z(f)$', color='r')
    >>> _= ax3.set_xlabel('Frequency $f$ [Hz]')
    >>> _= ax3.set_ylim(1e-2, 1)
    >>> _= ax4.set_ylim(-0.2, 0)
    >>> pg.plt.show()
    """
    z = (1. - m * (1. - relaxationTerm(f, tau, c, a))) * rho
    if np.isnan(z).any():
        print(f, 'rho', rho, 'm', m, 'tau', tau, 'c', c)
        pg.critical(z)
    return z


def ColeColeRhoDouble(f, rho, m1, t1, c1, m2, t2, c2):
    pg.deprecated("Please use modelColeColeRhoDouble instead of ColeColeRhoDouble.")
    return modelColeColeRhoDouble(f, rho, m1, t1, c1, m2, t2, c2)


def modelColeColeRhoDouble(f, rho, m1, t1, c1, m2, t2, c2, a=1):
    """Frequency-domain Double Cole-Cole impedance model
    Frequency-domain Double Cole-Cole impedance model returns the sum of
    two Cole-Cole Models with a common amplitude.
    Z = rho * (Z1(Cole-Cole) + Z2(Cole-Cole))
    """
    Z1 = modelColeColeRho(f, rho=1, m=m1, tau=t1, c=c1, a=a)
    Z2 = modelColeColeRho(f, rho=1, m=m2, tau=t2, c=c2, a=a)
    return rho * (Z1 + Z2)


def ColeColeSigma(f, sigma, m, tau, c, a=1):
    pg.deprecated("Please use modelColeColeSigma instead of ColeColeSigma.")
    return modelColeColeSigma(f, sigma, m, tau, c, a)


def modelColeColeSigma(f, sigma, m, tau, c, a=1):
    """Complex-valued conductivity Cole-Cole model"""
    return (1. + m / (1-m) * (1. - relaxationTerm(f, tau, c, a))) * sigma


def tauRhoToTauSigma(tRho, m, c):
    r"""Convert :math:`\tau_{\rho}` to :math:`\tau_{\sigma}` for Cole-Cole-Model.
    .. math::
        \tau_{\sigma} = \tau_{\rho}/(1-m)^{\frac{1}{c}}
    Examples
    --------
    >>> import numpy as np
    >>> import pygimli as pg
    >>> from pygimli.physics.SIP import modelColeColeRho, modelColeColeSigma, tauRhoToTauSigma
    >>> tr = 1.
    >>> Z = modelColeColeRho(1e5, rho=10.0, m=0.5, tau=tr, c=0.5)
    >>> ts = tauRhoToTauSigma(tr, m=0.5, c=0.5)
    >>> S = modelColeColeSigma(1e5, sigma=0.1, m=0.5, tau=ts, c=0.5)
    >>> abs(1.0/S - Z) < 1e-12
    True
    >>> np.angle(1.0/S / Z) < 1e-12
    True
    """
    return tRho * (1-m) ** (1/c)


def relaxationTerm(f, tau, c=1., a=1.):
    """Auxiliary function for Debye type relaxation term."""
    return 1. / ((f * 2. * pi * tau * 1j)**c + 1.)**a


def DebyeRelaxation(f, tau, m):
    pg.deprecated("Please use relaxationDebye instead of DebyeRelaxation.")
    return relaxationDebye(f, tau, m)


def relaxationDebye(f, tau, m):
    """Complex-valued single Debye relaxation term with chargeability."""
    return 1. - (1. - relaxationTerm(f, tau)) * m


def WarbugRelaxation(f, tau, m):
    pg.deprecated("Please use relaxationWarbug instead of WarbugRelaxation.")
    return relaxationWarbug(f, tau, m)


def relaxationWarbug(f, tau, m):
    """Complex-valued single Debye relaxation term with chargeability."""
    return 1. - (1. - relaxationTerm(f, tau, c=0.5)) * m


def ColeColeEpsilon(f, e0, eInf, tau, alpha):
    pg.deprecated("Please use modelColeColeEpsilon instead of ColeColeEpsilon.")
    return modelColeColeEpsilon(f, e0, eInf, tau, alpha)


def modelColeColeEpsilon(f, e0, eInf, tau, alpha):
    """Original complex-valued permittivity formulation (Cole&Cole, 1941)."""
    return (e0 - eInf) * relaxationTerm(f, tau, c=1./alpha) + eInf


def ColeCole(f, R, m, tau, c, a=1):
    pg.deprecated("Please use modelColeColeRho instead of ColeCole.")
    return modelColeColeRho(f, R, m, tau, c, a)


def ColeDavidson(f, R, m, tau, a=1):
    pg.deprecated("Please use modelColeDavidson instead of ColeDavidson.")
    return modelColeDavidson(f, R, m, tau, a)


def modelColeDavidson(f, R, m, tau, a=1):
    """For backward compatibility."""
    return ColeCole(f, R, m, tau, c=1, a=a)


class ColeColePhi(pg.core.ModellingBase):
    r"""Cole-Cole model with EM term after Pelton et al. (1978)
    Modelling operator for the Frequency Domain
    :py:mod:`Cole-Cole <pygimli.physics.SIP.ColeColeRho>` impedance model using
    :py:mod:`pygimli.physics.SIP.ColeColeRho` after Pelton et al. (1978)
    :cite:`PeltonWarHal1978`
    * :math:`\textbf{m} =\{ m, \tau, c\}`
        Modelling parameter for the Cole-Cole model with :math:`\rho_0 = 1`
    * :math:`\textbf{d} =\{\varphi_i(f_i)\}`
        Modelling eesponse for all given frequencies as negative phase angles
        :math:`\varphi(f) = -tan^{-1}\frac{\text{Im}\,Z(f)}{\text{Re}\,Z(f)}`
        and :math:`Z(f, \rho_0=1, m, \tau, c) =` Cole-Cole impedance.
    """

    def __init__(self, f, verbose=False):
        """Setup class by specifying the frequency."""
        super(ColeColePhi, self).__init__(self, verbose)
        self.f_ = f
        self.setMesh(pg.meshtools.createMesh1D(1, 3))

    def response(self, par):
        """Phase angle of the model."""
        spec = modelColeColeRho(self.f_, 1.0, par[0], par[1], par[2])
        return -np.angle(spec)


class DoubleColeColePhi(pg.core.ModellingBase):
    r"""Double Cole-Cole model with EM term after Pelton et al. (1978)
    Modelling operator for the Frequency Domain
    :py:mod:`Cole-Cole <pygimli.physics.SIP.ColeColeRho>` impedance model
    using :py:mod:`pygimli.physics.SIP.ColeColeRho` after Pelton et al. (1978)
    :cite:`PeltonWarHal1978`
    * :math:`\textbf{m} =\{ m_1, \tau_1, c_1, m_2, \tau_2, c_2\}`
        Modelling parameter for the Cole-Cole model with :math:`\rho_0 = 1`
    * :math:`\textbf{d} =\{\varphi_i(f_i)\}`
        Modelling Response for all given frequencies as negative phase angles
        :math:`\varphi(f) = \varphi_1(Z_1(f))+\varphi_2(Z_2(f)) =
        -tan^{-1}\frac{\text{Im}\,(Z_1Z_2)}{\text{Re}\,(Z_1Z_2)}`
        and :math:`Z_1(f, \rho_0=1, m_1, \tau_1, c_1)` and
        :math:`Z_2(f, \rho_0=1, m_2, \tau_2, c_2)` ColeCole impedances.
    """

    def __init__(self, f, verbose=False):
        """Setup class by specifying the frequency."""
        super(DoubleColeColePhi, self).__init__(verbose)
        self.f_ = f  # save frequencies
        self.setMesh(pg.meshtools.createMesh1D(1, 6))  # 4 single parameters

    def response(self, par):
        """phase angle of the model"""
        spec1 = modelColeColeRho(self.f_, 1.0, par[0], par[1], par[2])
        spec2 = modelColeColeRho(self.f_, 1.0, par[3], par[4], par[5])
        #return -np.angle(spec1 * spec2)

        return -np.angle(spec1) - np.angle(spec2)


class ColeColeAbs(pg.core.ModellingBase):
    """Cole-Cole model with EM term after Pelton et al. (1978)"""

    def __init__(self, f, verbose=False):
        super().__init__(verbose)
        self.f_ = f  # save frequencies
        self.setMesh(pg.meshtools.createMesh1D(1, 4))  # 3 single parameters

    def response(self, par):
        """phase angle of the model"""
        spec = modelColeColeRho(self.f_, par[0], par[1], par[2], par[3])
        return np.abs(spec)


class ColeColeComplex(pg.core.ModellingBase):
    """Cole-Cole model with EM term after Pelton et al. (1978)"""

    def __init__(self, f, verbose=False):
        super(ColeColeComplex, self).__init__(verbose)
        self.f_ = f  # save frequencies
        self.setMesh(pg.meshtools.createMesh1D(1, 4))  # 4 single parameters

    def response(self, par):
        """phase angle of the model"""
        spec = modelColeColeRho(self.f_, *par)
        return pg.cat(np.abs(spec), -np.angle(spec))


class ColeColeComplexSigma(pg.core.ModellingBase):
    """Cole-Cole model with EM term after Pelton et al. (1978)"""

    def __init__(self, f, verbose=False):
        super(ColeColeComplexSigma, self).__init__(verbose)
        self.f_ = f  # save frequencies
        self.setMesh(pg.meshtools.createMesh1D(1, 4))  # 4 single parameters

    def response(self, par):
        """phase angle of the model"""
        spec = modelColeColeSigma(self.f_, *par)
        return pg.cat(np.real(spec), np.imag(spec))


class PeltonPhiEM(pg.core.ModellingBase):
    """Cole-Cole model with EM term after Pelton et al. (1978)"""

    def __init__(self, f, verbose=False):
        super(PeltonPhiEM, self).__init__(verbose)
        self.f_ = f  # save frequencies
        self.setMesh(pg.meshtools.createMesh1D(1, 4))  # 4 single parameters

    def response(self, par):
        """phase angle of the model"""
        spec = modelColeColeRho(self.f_, 1.0, par[0], par[1], par[2]) * \
            relaxationTerm(self.f_, par[3])  # pure EM has c=1
        return -np.angle(spec)


class DebyePhi(pg.core.ModellingBase):
    """Debye decomposition (smooth Debye relaxations) phase only"""

    def __init__(self, fvec, tvec, verbose=False):  # save reference in class
        """constructor with frequecy and tau vector"""
        super(DebyePhi, self).__init__(verbose)
        self.f_ = fvec
        self.nf_ = len(fvec)
        self.t_ = tvec
        self.mesh = pg.meshtools.createMesh1D(len(tvec))  # standard 1d discretization
        self.setMesh(self.mesh)

    def response(self, par):
        """amplitude/phase spectra as function of spectral chargeabilities"""
        y = np.ones(self.nf_, dtype=np.complex)  # 1 -
        for (tau, mk) in zip(self.t_, par):
            y -= (1. - relaxationTerm(self.f_, tau)) * mk

        return -np.angle(y)


class DebyeComplex(pg.core.ModellingBase):
    """Debye decomposition (smooth Debye relaxations) of complex data"""

    def __init__(self, fvec, tvec, verbose=False):  # save reference in class
        """constructor with frequecy and tau vector"""
        self.f = fvec
        self.nf = len(fvec)
        self.t = tvec
        self.nt = len(tvec)
        mesh = pg.meshtools.createMesh1D(len(tvec))  # standard 1d discretization
        super(DebyeComplex, self).__init__(mesh, verbose)
        T, W = np.meshgrid(tvec, fvec * 2. * pi)
        WT = W*T
        self.A = WT**2 / (WT**2 + 1)
        self.B = WT / (WT**2+1)
        self.J = pg.Matrix()
        self.J.resize(len(fvec)*2, len(tvec))
        for i in range(self.nf):
            wt = fvec[i] * 2.0 * pi * tvec
            wt2 = wt**2
            self.J[i] = wt2 / (wt2 + 1.0)
            self.J[i+self.nf] = wt / (wt2 + 1.0)

        self.setJacobian(self.J)

    def response(self, par):
        """amplitude/phase spectra as function of spectral chargeabilities"""
        return self.J * par

    def createJacobian(self, par):
        """linear jacobian after Nordsiek&Weller (2008)"""
        pass




class DebyeModelling(pg.core.ModellingBase):

    """forward operator for Debye decomposition."""

    def __init__(self, fvec, tvec=None, zero=False, verbose=False):

        if tvec is None:
            tvec = N.logspace(-4, 0, 5)

        mesh = pg.meshtools.createMesh1D(len(tvec))

        if zero:
            mesh.cell(0).setMarker(-1)
            mesh.cell(len(tvec) - 1).setMarker(1)

        pg.core.ModellingBase.__init__(self, mesh, verbose)
        self.f_ = pg.asvector(fvec)
        self.t_ = tvec
        self.zero_ = zero

    def response(self, par):
        """phase spectrum as function of spectral chargeabilities."""
        y = pg.Vector(len(self.f_), 0.0)
        for (t, p) in zip(self.t_, par):
            wt = self.f_ * 2.0 * P.pi * t
            y = y + wt / (wt * wt + 1.) * p

        return y


class DoubleColeColeModelling(pg.core.ModellingBase):

    """
        Modelling using two Cole-Cole terms
    """

    def __init__(self, mesh, fvec, si=1.0, verbose=False):
        pg.core.ModellingBase.__init__(self, mesh, verbose)
        self.f_ = fvec
        self.si_ = si

    def response(self, par):
        """yields phase response response of double Cole Cole model."""
        y = pg.Vector(self.f_.size(), 0.0)
        wti = self.f_ * par[1] * 2.0 * P.pi
        wte = self.f_ * par[4] * 2.0 * P.pi
        for i in range(0, y.size()):
            cpI = 1. / (N.power(wti[i] * 1j, par[2]) + 1.)
            cpE = 1. / (N.power(wte[i] * 1j, par[5]) + 1.)
            y[i] = - N.imag(cpI) * par[0] - N.imag(cpE) * par[3] * self.si_
#            y[i] = - par[0] - N.imag(cpE) * par[3] * self.si_

        return y


class DoubleColeColeModelling(pg.core.ModellingBase):

    """
        Modelling using two Cole-Cole terms
    """

    def __init__(self, mesh, fvec, si=1.0, verbose=False):
        pg.core.ModellingBase.__init__(self, mesh, verbose)
        self.f_ = fvec
        self.si_ = si

    def response(self, par):
        """yields phase response response of double Cole Cole model."""
        y = pg.Vector(self.f_.size(), 0.0)
        wti = self.f_ * par[1] * 2.0 * P.pi
        wte = self.f_ * par[4] * 2.0 * P.pi
        for i in range(0, y.size()):
            cpI = 1. / (N.power(wti[i] * 1j, par[2]) + 1.)
            cpE = 1. / (N.power(wte[i] * 1j, par[5]) + 1.)
            y[i] = - N.imag(cpI) * par[0] - N.imag(cpE) * par[3] * self.si_
#            y[i] = - par[0] - N.imag(cpE) * par[3] * self.si_

        return y

def ReadAndRemoveEM(filename, readsecond=False, doplot=False,
                    dellast=True, ePhi=0.5, ePerc=1., lam=2000.):
    """
        Read res1file and remove EM effects using a double-Cole-Cole model
        fr,rhoa,phi,dphi = ReadAndRemoveEM(filename, readsecond/doplot bools)
    """
    fr, rhoa, phi, drhoa, dphi = read1resfile(filename,
                                              readsecond,
                                              dellast=dellast)
    # forward problem
    mesh = pg.meshtools.createMesh1D(1, 6)  # 6 independent parameters
    f = DoubleColeColeModelling(mesh, pg.asvector(fr), phi[2] / abs(phi[2]))
    f.regionManager().loadMap("region.control")
    model = f.createStartVector()

    # inversion
    inv = pg.Inversion(phi, f, True, False)
    inv.setAbsoluteError(phi * ePerc * 0.01 + ePhi / 1000.)
    inv.setRobustData(True)

    # inv.setCWeight(pg.Vector(6, 1.0)) # wozu war das denn gut?
    inv.setMarquardtScheme(0.8)
    inv.setLambda(lam)
    inv.setModel(model)
    erg = inv.run()
    inv.echoStatus()
    chi2 = inv.chi2()
    mod0 = pg.Vector(erg)
    mod0[0] = 0.0  # set IP term to zero to obtain pure EM term
    emphi = f.response(mod0)
    resid = (phi - emphi) * 1000.

    if doplot:
        s = "IP: m= " + str(rndig(erg[0])) + " t=" + str(rndig(erg[1])) + \
            " c =" + str(rndig(erg[2]))
        s += "  EM: m= " + str(rndig(erg[3])) + " t=" + str(rndig(erg[4])) + \
            " c =" + str(rndig(erg[5]))
        fig = P.figure(1)
        fig.clf()
        ax = P.subplot(111)
        P.errorbar(
            fr,
            phi *
            1000.,
            yerr=dphi *
            1000.,
            fmt='x-',
            label='measured')
        ax.set_xscale('log')
        P.semilogx(fr, emphi * 1000., label='EM term (CC)')
        P.errorbar(fr, resid, yerr=dphi * 1000., label='IP term')
        ax.set_yscale('log')
        P.xlim((min(fr), max(fr)))
        P.ylim((0.1, max(phi) * 1000.))
        P.xlabel('f in Hz')
        P.ylabel(r'-$\phi$ in mrad')
        P.grid(True)
        P.title(s)
        P.legend(loc=2)  # ('measured','2-cole-cole','residual'))
        fig.show()

    return N.array(fr), N.array(rhoa), N.array(resid), N.array(
        phi) * 1e3, dphi, chi2, N.array(emphi) * 1e3

''''''

# time domain model
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

''''''