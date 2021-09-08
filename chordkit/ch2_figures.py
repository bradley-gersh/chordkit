from chord_utils import Timbre, ChordSpectrum, TransposeDomain
from roughness_plot import roughness_curve
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import sys

# Dissertation ch. 2, figure 1
# Figure 1. A plot of Helmholtz’s pair-roughness function (Helmholtz,
# Sensations of Tone, 418, choosing β = 0.01). Given one sine tone fixed at
# 220 Hz, the graph shows Helmholtz’s estimate of the roughness created by
# adding a second sine tone of variable frequency.
def ch2_fig1(action):
    # 1 partial (fundamental only), amplitude 1
    tim = Timbre([1], [1])
    fund_hz = 220.0

    ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    transpose_domain = TransposeDomain(-12, 12, 5000, 'ST_DIFF')
    # print(transpose_domain.domain)
    roughness = roughness_curve(ref_chord, test_chord, transpose_domain=transpose_domain, function_type='HELMHOLTZ', plot=False, options={
        'ref': ref_chord.partials['hz']
    })

    _, ax = plt.subplots()

    plt.plot(transpose_domain.domain, roughness, 'k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.subplots_adjust(left=0.15)
    ax.yaxis.set_label_coords(-0.13, 0.5)

    if action.lower() == 'save':
        plt.savefig('ch2_fig1.png',dpi=350)
        print('ch2_fig1.png saved')

    else:
        plt.show()

def ch2_fig2(action):


def __main__(action):
    ch2_fig1(action.lower())

if __name__ == '__main__':
    __main__(sys.argv[1])
