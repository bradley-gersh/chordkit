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
    roughness = roughness_curve(ref_chord, test_chord, transpose_domain=transpose_domain, function_type='HELMHOLTZ', plot=False, options={
        'ref': ref_chord.partials['hz']
    })

    # Plot
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
    # 10 partials (to match Helmholtz's figure 60A, constant amplitude)

    roughnesses = []

    # for i in range(2, 11): # Use this line for a family of curves like Helmholtz's
    #                          figure 60A
    for i in range(10, 11): # For one curve (Helmholtz's figure 61)
        tim = Timbre(range(1, i), 1)
        fund_hz = 264 # Helmholtz's starting pitch: 6/5 * 220, or a just-intoned C3

        ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
        test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
        transpose_domain = TransposeDomain(-0.5, 12.5, 1000, 'ST_DIFF')
        roughnesses.append(roughness_curve(ref_chord, test_chord, transpose_domain=transpose_domain, function_type='HELMHOLTZ', plot=False, options={
            'ref': ref_chord.partials['hz']
        }))

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    for roughness in roughnesses:
        plt.plot(transpose_domain.domain, roughness, 'k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    # ax.xaxis.set_minor_locator(MultipleLocator(1))
    # plt.subplots_adjust(left=0.15)
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig('ch2_fig2.png',dpi=350)
        print('ch2_fig2.png saved')

    else:
        plt.show()

def ch2_fig3a(action):

    # Plot
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
        plt.savefig('ch2_fig3a.png', dpi=350)
        print('ch2_fig3a.png saved')

    else:
        plt.show()

def __main__(argv):
    action = ''
    if len(argv) > 1:
        action = argv[1].lower()

    ch2_fig1(action)
    ch2_fig2(action)
    # ch2_fig3a(action)
    # ch2_fig3b(action)
    # ch2_fig4(action)
    # ch2_fig5(action)
    # ch2_fig6(action)
    # ch2_fig7a(action)
    # ch2_fig7b(action)
    # ch2_fig8(action)
    # ch2_fig9(action)
    # ch2_fig10(action)
    # ch2_fig11a(action)
    # ch2_fig11b(action)
    # ch2_fig12(action)
    # ch2_fig13(action)
    # ch2_fig14(action)
    # ch2_fig15(action)
    # ch2_fig16(action)
    # ch2_fig17(action)
    # ch2_fig19(action)


if __name__ == '__main__':
    __main__(sys.argv)
