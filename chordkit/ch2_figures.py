from chord_utils import Timbre, MergedSpectrum, ChordSpectrum, TransposeDomain
from defaults import (SineTone, SetharesTone, FlatSawTimbre, SetharesTimbre, c4, midi_zero, a3, a4, one_octave, two_octaves, two_octaves_symm)
from chord_plots import overlap_curve, roughness_curve
from roughness_models import roughness_complex
from overlap_models import overlap_complex
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FixedLocator
from pair_constants import AUDITORY_CONSTANTS as ac
import sys
import numpy as np

# Dissertation ch. 2, figure 1
# Figure 1a. A plot of Helmholtz’s pair-roughness function (Helmholtz 1895, appendix XV)
def ch2_fig1a(action):
    title = 'ch2_fig1a'

    ref_tone = SineTone(a3)
    test_tone = SineTone(a3)
    T = two_octaves_symm

    roughness = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='HELMHOLTZ',
        normalize=True,
        options={
            'crossterms_only': False,
            'ref': ref_tone.partials['hz'],
            'show_partials': False
        }
    )

    # Plot
    _, ax = plt.subplots()
    plt.plot(T.domain, roughness, 'k')
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

    ref_tone = SineTone(a3)
    test_tone = SineTone(a3)
    T = two_octaves_symm

    roughness = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES',
        normalize=True,
        options={
            'crossterms_only': False,
            'cutoff': False,
            'original': True,
            'show_partials': False
        }
    )

    # Plot
    _, ax = plt.subplots()
    plt.plot(T.domain, roughness, 'k')
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

    # Would make sense to use `sethares_timbre` here, but it has too few partials (7)
    # for the overlap function later.
    ref_tone = SetharesTone(12, a3)
    test_tone = SetharesTone(12, a3)
    T = one_octave

    roughness = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES',
        normalize=True,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'normalize': True,
          'original': False,
          'show_partials': False
        }
    )

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(T.domain, roughness, 'k')
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

# Figure 3. Sethares roughness for Fratres chords
def ch2_fig3(action):
    title = 'ch2_fig3'

    tim = SetharesTimbre(12)
    fund = midi_zero

    # The lower octave is not doubled, following the holograph score shown at
    # on the Arvo Pärt Centre website, https://www.arvopart.ee/en/arvo-part/work/390/
    fratres_drone = ChordSpectrum([45, 52], 'ST_DIFF', timbre=tim, fund_hz=fund)

    fratres_tenths = [ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund) for chord in [
        [],
        [73, 88],
        [69, 85],
        [65, 81],
        [62, 77],
        [58, 74],
        [55, 70],
        [52, 67],
        [49, 64],
        [57, 61]
    ]]

    fratres_upper_var_1 = [ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund) for chord in [
        [],
        [73, 88, 81],
        [69, 85, 76],
        [65, 81, 72],
        [62, 77, 72], # variable 72/69
        [58, 74, 69], # variable 69/64
        [55, 70, 64], # variable 64/60
        [52, 67, 60],
        [49, 64, 57],
        [57, 61, 52]
    ]]

    # The next one includes the other variable sonorities
    fratres_upper_var_2 = [ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund) for chord in [
        [],
        [73, 88, 81],
        [69, 85, 76],
        [65, 81, 72],
        [62, 77, 69], # variable 72/69
        [58, 74, 64], # variable 69/64
        [55, 70, 60], # variable 64/60
        [52, 67, 60],
        [49, 64, 57],
        [57, 61, 52]
    ]]

    fratres_outer_diss = [
        roughness_complex(MergedSpectrum(fratres_drone, chord), 'SETHARES') for chord in fratres_tenths
    ]

    fratres_var_1_diss = [
        roughness_complex(MergedSpectrum(fratres_drone, chord), 'SETHARES') for chord in fratres_upper_var_1
    ]

    fratres_var_2_diss = [
        roughness_complex(MergedSpectrum(fratres_drone, chord), 'SETHARES') for chord in fratres_upper_var_2
    ]

    # Normalize so drone has roughness 1
    fratres_outer_diss_n = [float(x) / fratres_outer_diss[0] for x in fratres_outer_diss]
    fratres_var_1_diss_n = [float(x) / fratres_var_1_diss[0] for x in fratres_var_1_diss]
    fratres_var_2_diss_n = [float(x) / fratres_var_2_diss[0] for x in fratres_var_2_diss]

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(['drone'] + list(range(1,10)), fratres_outer_diss_n, 'k')
    # plt.plot(['drone'] + list(range(1,10)), fratres_var_1_diss_n, 'k')
    # plt.plot(['drone'] + list(range(1,10)), fratres_var_2_diss_n, 'k')
    plt.xlabel('section')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')

    else:
        plt.show()

# Figure 4. Discrepancies between Sethares roughness and dissonance.
def ch2_fig4(action):
    title = 'ch2_fig4'

    tim = SetharesTimbre(12)
    fund = c4

    maj3_dyad = ChordSpectrum([0, 4], 'ST_DIFF', timbre=tim, fund_hz=fund)
    maj53_triad = ChordSpectrum([0, 4, 7], 'ST_DIFF', timbre=tim, fund_hz=fund)
    maj7_dyad = ChordSpectrum([0, 11], 'ST_DIFF', timbre=tim, fund_hz=fund)

    data = {
        '[C4, E4]': roughness_complex(maj3_dyad, 'SETHARES'),
        '[C4, E4, G4]': roughness_complex(maj53_triad, 'SETHARES'),
        '[C4, B4]': roughness_complex(maj7_dyad, 'SETHARES')
    }

    plot0_names = ['[C4, E4]', '[C4, E4, G4]']
    plot1_names = ['[C4, E4]', '[C4, B4]']
    plot0_vals = [data[name] for name in plot0_names]
    plot1_vals = [data[name] for name in plot1_names]

    # Plot
    fig, ax = plt.subplots(2, 3, figsize=(12,5), gridspec_kw={'width_ratios': [2, 2, 1]})
    plt.subplots_adjust(wspace=0.5, hspace=0.7)
    for row in ax:
        for panel in row[0:2]:
            panel.spines['right'].set_visible(False)
            panel.spines['top'].set_visible(False)
            panel.set_ylim([0, 1.1])
            panel.set_xlim([0, 3600.])
            panel.set_ylabel('amplitude\n(arbitrary units)')
            panel.set_xlabel('frequency (Hz)')

    ax[0,0].stem(maj3_dyad.partials['hz'], maj3_dyad.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    ax[0,0].set_title('[C4, E4]')
    ax[0,1].stem(maj53_triad.partials['hz'], maj53_triad.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    ax[0,1].set_title('[C4, E4, G4]')
    ax[0,2].bar(plot0_names, plot0_vals, fill=False, hatch='///')
    ax[0,2].set_ylim([0, maj53_diss * 1.1])
    ax[0,2].spines['right'].set_visible(False)
    ax[0,2].spines['top'].set_visible(False)
    ax[0,2].set_ylabel('roughness\n(arbitrary units)')

    ax[1,0].stem(maj3_dyad.partials['hz'], maj3_dyad.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    ax[1,0].set_title('[C4, E4]')
    ax[1,1].stem(maj7_dyad.partials['hz'], maj7_dyad.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    ax[1,1].set_title('[C4, B4]')
    ax[1,2].bar(plot1_names, plot1_vals, fill=False, hatch='///')
    ax[1,2].set_ylim([0, maj53_diss * 1.1])
    ax[1,2].spines['right'].set_visible(False)
    ax[1,2].spines['top'].set_visible(False)
    ax[1,2].set_ylabel('roughness\n(arbitrary units)')

    fig.add_artist(plt.Line2D([0, 1], [0.48, 0.48], color='k'))
    fig.add_artist(plt.Text(0.02, 0.75, '(a)', size=16.0, weight='bold'))
    fig.add_artist(plt.Text(0.02, 0.25, '(b)', size=16.0, weight='bold'))

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')

    else:
        plt.show()

# Figure 5. Octave drift and correction in Sethares roughness.
def ch2_fig5(action): # Not working yet
    title = 'ch2_fig5'

    tim = FlatSawTimbre(7)
    long_tim = FlatSawTimbre(14)
    fund = a4

    # ref_chord_1 = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund)
    ref_chord_2 = ChordSpectrum([0], 'ST_DIFF', timbre=long_tim, fund_hz=fund)
    test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund)

    T = TransposeDomain(-0.5, 12.5, 150, 'ST_DIFF')

    roughness_1 = roughness_curve(
        ref_chord_2,
        test_chord,
        transpose_domain=T,
        function_type='SETHARES',
        normalize=True,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    roughness_2 = roughness_curve(
        ref_chord_2,
        test_chord,
        transpose_domain=T,
        function_type='SETHARES',
        normalize=True,
        options={
          'amp_type': 'MIN',
          'crossterms_only': True,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(T.domain, roughness_1, 'k.')
    plt.plot(T.domain, roughness_2, 'k')
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

# Figure 6. A wide chord.
def ch2_fig6(action):
    title = 'ch2_fig6'

    chord = ChordSpectrum([49, 60, 71], 'ST_DIFF', timbre=SetharesTimbre(12), fund_hz=midi_zero)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.stem(chord.partials['hz'], chord.partials['amp'])
    plt.xlabel('frequency (Hz)')
    plt.ylabel('amplitude (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

# Figure 7a. Pair-overlap curve.
def ch2_fig7a(action):
    title = 'ch2_fig7a'

    ref_tone = SineTone(a3)
    test_tone = SineTone(a3)
    T = two_octaves_symm

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='BELL',
        normalize=True,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    roughness = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES',
        normalize=True,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    # Plot
    _, ax = plt.subplots()
    ax.plot(T.domain, overlap, color='k', linestyle='-', linewidth=3)
    ax.plot(T.domain, roughness, color='k', linestyle='--', linewidth=1)
    ax.legend(['overlap', 'roughness'], edgecolor='k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('(arbitrary units)')
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.ylim(ymin=0.0)
    plt.subplots_adjust(left=0.15)
    ax.yaxis.set_label_coords(-0.13, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

# Figure 7b. Complex overlap curve.
def ch2_fig7b(action):
    title = 'ch2_fig7b'

    ref_tone = SetharesTone(12, a3)
    test_tone = SetharesTone(12, a3)
    T = one_octave

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='BELL',
        normalize=False,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    roughness = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES',
        normalize=False,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    ratio = roughness / overlap

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(T.domain, overlap, 'k', linewidth=1)
    ax.plot(T.domain, ratio, 'k', linewidth=3)
    ax.plot(T.domain, roughness, 'k--', linewidth=1)
    ax.legend(['overlap', 'roughness'], edgecolor='k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('(arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig8a(action):
    title = 'ch2_fig8a'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig8b(action):
    title = 'ch2_fig8b'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

# Figure 9. Plot of relative roughness over 1 octave, above A3.
def ch2_fig9(action):
    title = 'ch2_fig9'

    ref_tone = SetharesTone(12, a3)
    test_tone = SetharesTone(12, a3)
    T = one_octave

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='BELL',
        normalize=False,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    roughness = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES',
        normalize=False,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    # log_ratio = np.log(roughness / overlap)
    ratio = (roughness / overlap)

    # log_ratio = log_ratio / np.max(np.abs(log_ratio))
    ratio = ratio / np.max(ratio)
    roughness = roughness / np.max(roughness)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    # ax.plot(T.domain, log_ratio, 'k', linewidth=3)
    ax.plot(T.domain, ratio, 'k', linewidth=3)
    ax.plot(T.domain, roughness, 'k--')
    plt.xlabel('interval (semitones)')
    plt.ylabel('relative roughness\n(arbitrary units)')
    ax.legend(['relative roughness', 'roughness'], edgecolor='k')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig9_app(action):
    title = 'ch2_fig9_app'

    ref_tone = SetharesTone(7)
    test_tone = SetharesTone(7)
    T = one_octave

    overlap1= overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='BELL',
        normalize=False,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    roughness1 = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES',
        normalize=False,
        options={
          'amp_type': 'MIN',
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    # overlap2= overlap_curve(
    #     ref_tone,
    #     test_tone,
    #     transpose_domain=T,
    #     function_type='BELL',
    #     normalize=False,
    #     options={
    #       'amp_type': 'MIN',
    #       'crossterms_only': False,
    #       'cutoff': False,
    #       'original': False,
    #       'show_partials': False
    #     }
    # )

    # roughness2 = roughness_curve(
    #     ref_tone,
    #     test_tone,
    #     transpose_domain=T,
    #     function_type='SETHARES',
    #     normalize=False,
    #     options={
    #       'amp_type': 'MIN',
    #       'crossterms_only': False,
    #       'cutoff': False,
    #       'original': False,
    #       'show_partials': False
    #     }
    # )

    roughness1 = roughness1 / max(roughness1)
    overlap1 = overlap1 / max(overlap1)

    ratio1 = (roughness1 / overlap1)
    ratio1 = ratio1 / np.max(ratio1)
    # ratio2 = (roughness2 / overlap2)
    # ratio2 = ratio2 / np.max(ratio2)

    roughness1 = roughness1 / np.max(roughness1)
    overlap1 = overlap1 / np.max(overlap1)
    # roughness2 = roughness2 / np.max(roughness2)
    # overlap2 = overlap2 / np.max(overlap2)

    strength1 = overlap1 + roughness1
    overlap1 += 0.00000000001
    ratio1 = (2/np.pi) * np.arctan(np.log(roughness1 / overlap1))


    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    # ax.plot(T.domain, ratio1, 'k')
    # ax.plot(T.domain, strength1, 'k--')
    ax.plot(T.domain, roughness1, 'k-.')
    ax.plot(T.domain, overlap1, 'k--')
    # ax.plot(T.domain, ratio2, 'c')
    # ax.plot(T.domain, roughness2, 'c-.')
    # ax.plot(T.domain, overlap2, 'c--')
    plt.xlabel('interval (semitones)')
    plt.ylabel('relative roughness\n(arbitrary units)')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

# Figure 10. Sensitivity of relative roughness to presence of higher partials.
def ch2_fig10(action):
    title = 'ch2_fig10'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

# Figure 11. Relative roughnesses of a major seventh chord and its subsets.
def ch2_fig11(action):
    title = 'ch2_fig11'

    tim = SetharesTimbre(12)
    fund = c4

    chord_names = [
        ('[C4, E4]', [0, 4]),
        ('[C4, G4]', [0, 7]),
        ('[C4, B4]', [0, 11]),
        ('[E4, G4]', [4, 7]),
        ('[E4, B4]', [4, 11]),
        ('[G4, B4]', [7, 11]),
        ('[C4, E4, G4]', [0, 4, 7]),
        ('[C4, E4, B4]', [0, 4, 11]),
        ('[C4, G4, B4]', [0, 7, 11]),
        ('[E4, G4, B4]', [4, 7, 11]),
        ('[C4, E4, G4, B4]', [0, 4, 7, 11])
    ]

    chords = [ChordSpectrum(chord_name[1], 'ST_DIFF', timbre=tim, fund_hz=fund) for chord_name in chord_names]
    roughnesses = np.array([roughness_complex(chord, 'SETHARES') for chord in chords])
    overlaps = np.array([overlap_complex(chord, 'BELL') for chord in chords])
    # log_ratios = np.log(roughnesses / overlaps)
    ratios = (roughnesses / overlaps)

    # chord_data = zip(chord_names, roughnesses, log_ratios)
    chord_data = zip(chord_names, roughnesses, ratios)
    # print(list(zip(*sorted(chord_data, key=lambda chord: chord[1]))))
    [roughness_sorted_names, roughness_sorted_vals, _] = list(zip(*sorted(chord_data, key=lambda chord: chord[1])))
    # chord_data = zip(chord_names, roughnesses, log_ratios)
    chord_data = zip(chord_names, roughnesses, ratios)
    [ratio_sorted_names, _, ratio_sorted_vals] = list(zip(*sorted(chord_data, key=lambda chord: chord[2])))
    roughness_sorted_labels = [name[0] for name in roughness_sorted_names]
    ratio_sorted_labels = [name[0] for name in ratio_sorted_names]

    # Plot
    fig, ax = plt.subplots(1,2)
    plt.tight_layout()
    fig.set_figwidth(10.5)
    ax[0].bar(roughness_sorted_labels, roughness_sorted_vals, fill=False, hatch='///')
    ax[1].bar(ratio_sorted_labels, ratio_sorted_vals, fill=False, hatch='///')

    ax[0].set_ylabel('roughness\n(arbitrary units)')
    ax[1].set_ylabel('relative roughness\n(arbitrary units)')
    ax[0].tick_params(axis='x', labelrotation=90)
    ax[1].tick_params(axis='x', labelrotation=90)
    plt.subplots_adjust(bottom=0.3)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig12(action):
    title = 'ch2_fig12'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig13(action):
    title = 'ch2_fig13'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig14a(action):
    title = 'ch2_fig14a'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig14b(action):
    title = 'ch2_fig14b'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig15a(action):
    title = 'ch2_fig15a'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig15b(action):
    title = 'ch2_fig15b'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig16(action):
    title = 'ch2_fig16'

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()





##########################
#### APPENDIX FIGURES ####
##########################

# Figure 1b, appendix. My attempt to implement Helmholtz’s composite function.
def ch2_fig1b_appendix(action):
    title = 'ch2_fig1b_app'

    roughnesses = []

    # for i in range(2, 11): # Use this line for a family of curves like Helmholtz's
    #                          figure 60A
    for i in range(10, 11): # For one curve (Helmholtz's figure 61)
        # 10 partials (to match Helmholtz's figure 60A, constant amplitude)
        tim = FlatSawTimbre(i)
        fund = 264 # Helmholtz's starting pitch: 6/5 * 220, or a just-intoned C3

        ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund)
        test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund)
        T = one_octave

        roughnesses.append(
            roughness_curve(
                ref_chord,
                test_chord,
                transpose_domain=T,
                function_type='HELMHOLTZ',
                options={'ref': ref_chord.partials['hz']}
            )
        )

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    for roughness in roughnesses:
        plt.plot(T.domain, roughness, 'k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
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
    tim = FlatSawTimbre(7)
    fund = 500.0

    ref_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund)
    test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund)

    T = TransposeDomain(1., 2.3, 2300, 'SCALE_FACTOR')

    roughness = roughness_curve(
        ref_chord,
        test_chord,
        transpose_domain=T,
        function_type='SETHARES',
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
    plt.plot(T.domain, roughness, 'k')
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

    # ch2_fig1a(action)
    # ch2_fig2a(action)
    # ch2_fig2b(action)
    # ch2_fig3(action)
    # ch2_fig4(action)
    # ch2_fig5(action)
    # ch2_fig6(action)
    # ch2_fig7a(action)
    # ch2_fig7b(action)
    # ch2_fig8(action)
    # ch2_fig9(action)
    # ch2_fig10(action)
    ch2_fig11(action)
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
