from chord_utils import Timbre, ChordSpectrum, TransposeDomain
from roughness_plot import roughness_curve
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

# Dissertation ch. 2, figure 1
# Figure 1. A plot of Helmholtz’s pair-roughness function (Helmholtz,
# Sensations of Tone, 418, choosing β = 0.01). Given one sine tone fixed at
# 220 Hz, the graph shows Helmholtz’s estimate of the roughness created by
# adding a second sine tone of variable frequency.
def ch2_fig1():
    # 1 partial (fundamental only), amplitude 1
    tim = Timbre([1], [1])
    fund_hz = 220.0

    ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    transpose_domain = TransposeDomain(-100, 100, 400, 'HZ_SHIFT')
    # print(transpose_domain.domain)
    roughness = roughness_curve(ref_chord, test_chord, transpose_domain=transpose_domain, function_type='HELMHOLTZ', plot=False)

    fig1, ax = plt.subplots()

    plt.plot(transpose_domain.domain, roughness, 'k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    # ax.xaxis.set_major_locator(MultipleLocator(2))
    # ax.xaxis.set_major_formatter('{x:.0f}')
    # ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.show()

    return

def __main__():
    ch2_fig1()

if __name__ == '__main__':
    __main__()
