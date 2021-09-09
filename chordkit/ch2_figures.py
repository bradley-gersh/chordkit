from chord_utils import Timbre, ChordSpectrum, TransposeDomain
from roughness_plot import roughness_curve
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import sys
import numpy as np

# Dissertation ch. 2, figure 1
# Figure 1a. A plot of Helmholtz’s pair-roughness function (Helmholtz 1895, appendix XV)
def ch2_fig1a(action):
    title = 'ch2_fig1a'

    # 1 partial (fundamental only), amplitude 1
    tim = Timbre([1], [1])
    fund_hz = 220.0

    ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    transpose_domain = TransposeDomain(-12, 12, 5000, 'ST_DIFF')
    roughness = roughness_curve(
        ref_chord,
        test_chord,
        transpose_domain=transpose_domain,
        function_type='HELMHOLTZ',
        plot=False,
        normalize=True,
        options={'ref': ref_chord.partials['hz']}
    )

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
        plt.savefig(f'{title}.png',dpi=350)
        print(f'{title}.png saved')

    else:
        plt.show()

# Figure 2a. Sethares pair roughness function (Sethares 1993)
def ch2_fig2a(action):
    title = 'ch2_fig2a'

    # 1 partial (fundamental only), amplitude 1
    tim = Timbre([1], [1])
    fund_hz = 220.0

    ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    transpose_domain = TransposeDomain(-12, 12, 5000, 'ST_DIFF')
    roughness = roughness_curve(
        ref_chord,
        test_chord,
        transpose_domain=transpose_domain,
        function_type='SETHARES',
        plot=False,
        normalize=True,
        options={'original': True}
    )

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
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')

    else:
        plt.show()

# Figure 2b. Sethares complex roughness function
def ch2_fig2b(action):
    title = 'ch2_fig2b'

    # 7 partials, partial p has amplitude 0.88^p (after Sethares 1993, Fig. 2)
    tim = Timbre(range(1, 8), [0.88 ** p for p in range(1,8)])
    fund_hz = 440.0

    ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)

    transpose_domain = TransposeDomain(-0.5, 12.5, 2300, 'ST_DIFF')

    roughness = roughness_curve(
        ref_chord,
        test_chord,
        transpose_domain=transpose_domain,
        function_type='SETHARES',
        plot=False,
        normalize=True,
        options={
          'original': False,
          'normalize': True,
          'amp_type': 'MIN'
        }
    )

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
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
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')

    else:
        plt.show()

#### APPENDIX FIGURES
# Figure 1b, appendix. My attempt to implement Helmholtz’s composite function.
def ch2_fig1b_appendix(action):
    title = 'ch2_fig1b_app'

    roughnesses = []

    # for i in range(2, 11): # Use this line for a family of curves like Helmholtz's
    #                          figure 60A
    for i in range(10, 11): # For one curve (Helmholtz's figure 61)
        # 10 partials (to match Helmholtz's figure 60A, constant amplitude)
        tim = Timbre(range(1, i), 1)
        fund_hz = 264 # Helmholtz's starting pitch: 6/5 * 220, or a just-intoned C3

        ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
        test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
        transpose_domain = TransposeDomain(-0.5, 12.5, 1000, 'ST_DIFF')
        roughnesses.append(
            roughness_curve(
                ref_chord,
                test_chord,
                transpose_domain=transpose_domain,
                function_type='HELMHOLTZ',
                plot=False,
                options={'ref': ref_chord.partials['hz']}
            )
        )

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
        plt.savefig(f'{title}.png',dpi=350)
        print(f'{title}.png saved')

    else:
        plt.show()

# Figure 2b, appendix. Compare Sethares's implementation to the current one
def ch2_fig2b_appendix(action):
    title = 'ch2_fig2b_app'

    # 7 partials, all of amplitude 1
    tim = Timbre(range(1, 8), 1)
    fund_hz = 500.0

    ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)
    test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund_hz)

    transpose_domain = TransposeDomain(1., 2.3, 2300, 'SCALE_FACTOR')

    roughness = roughness_curve(
        ref_chord,
        test_chord,
        transpose_domain=transpose_domain,
        function_type='SETHARES',
        plot=False,
        normalize=False,
        options={
            'original': True,
            'normalize': False,
            'amp_type': 'MIN'
        }
    )

    def setharesDissmeasure(fvec, amp):
    # Direct port of Sethares' MATLAB code from https://sethares.engr.wisc.edu/comprog.html
    # for comparison
        Dstar = 0.24
        S1 = 0.0207
        S2 = 18.96
        C1 = 5
        C2 = -5
        A1 = -3.51
        A2 = -5.75
        # firstpass = 1 # This variable not used
        N = len(fvec)

        fves, ams = [np.array(x) for x in zip(*sorted(zip(fvec, amp)))]
        D = 0
        for i in range(1, N):
            Fmin = fves[0:(N - i)]
            S = Dstar / (S1 * Fmin + S2)
            Fdif = fves[i:N] - fves[0:(N - i)]
            a = min(*ams[i:N], *ams[0:(N - i)])
            Dnew = a * (C1 * np.exp(A1 * S * Fdif) + C2 * np.exp(A2 * S * Fdif))
            D = D + np.dot(Dnew, np.ones(np.size(Dnew)))

        return D

    # Sethares's test cast for Figure 3 of his 1993 paper
    freq = 500 * np.array([1, 2, 3, 4, 5, 6, 7])
    amp = np.ones(np.size(freq))
    end = 2.3
    inc = 0.001
    setharesDiss = [0]

    for alpha in np.arange(1+inc, end, inc):
        f = np.concatenate([freq, alpha * freq])
        a = np.concatenate([amp, amp])
        d = [setharesDissmeasure(f, a)]
        setharesDiss = np.concatenate([setharesDiss, d]);

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(transpose_domain.domain, roughness, 'k')
    # Uncomment the next line to plot Sethares's own version, from https://sethares.engr.wisc.edu/comprog.html.
    # NOTE: If comparing to Sethares' code, be sure set options['normalize'] to False
    # in the call to roughness_curve at the top of this function, and change the
    # transpose_domain (uncomment the recommended line).

    plt.plot(np.arange(1, end, inc), setharesDiss, 'k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')

    else:
        plt.show()

def __main__(argv):
    action = ''
    if len(argv) > 1:
        action = argv[1].lower()

    ch2_fig1a(action)
    ch2_fig2a(action)
    ch2_fig2b(action)
    # ch2_fig3(action)
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
