from chord_utils import Timbre, MergedSpectrum, ChordSpectrum, TransposeDomain
from defaults import (SineTone, SetharesTone, FlatSawTone, SetharesMajTriad, FlatSawTimbre, SetharesTimbre, c4, d4, midi_zero, a3, a4, one_octave, two_octaves, two_octaves_symm)
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
# Figure 13 (also). Sethares roughness and relative roughness for Fratres chords
def ch2_fig3_13(action):
    title1 = 'ch2_fig3'
    title2 = 'ch2_fig13'

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
        [45, 61]
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
        [45, 61, 52]
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
        [45, 61, 52]
    ]]

    fratres_outer_diss = np.array([
        roughness_complex(MergedSpectrum(fratres_drone, chord), 'SETHARES') for chord in fratres_tenths
    ])

    # fratres_var_1_diss = [
        # roughness_complex(MergedSpectrum(fratres_drone, chord), 'SETHARES') for chord in fratres_upper_var_1
    # ]

    # fratres_var_2_diss = [
        # roughness_complex(MergedSpectrum(fratres_drone, chord), 'SETHARES') for chord in fratres_upper_var_2
    # ]

    fratres_outer_overlap = np.array([
        overlap_complex(MergedSpectrum(fratres_drone, chord), 'BELL') for chord in fratres_tenths
    ])

    fratres_outer_ratio = fratres_outer_diss / fratres_outer_overlap

    # Normalize so drone has roughness 1
    fratres_outer_diss_n = fratres_outer_diss / fratres_outer_diss[0]
    fratres_outer_ratio_n = fratres_outer_ratio / fratres_outer_ratio[0]
    # fratres_var_1_diss_n = [float(x) / fratres_var_1_diss[0] for x in fratres_var_1_diss]
    # fratres_var_2_diss_n = [float(x) / fratres_var_2_diss[0] for x in fratres_var_2_diss]

    # Plots

    # Fig 3
    plt.figure(3)
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
        plt.savefig(f'{title1}.png', dpi=350)
        print(f'{title1}.png saved')

    else:
        plt.show(block=False)

    # Fig 13
    plt.figure(13)
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(['drone'] + list(range(1,10)), fratres_outer_ratio_n, 'k', linewidth=3)
    plt.plot(['drone'] + list(range(1,10)), fratres_outer_diss_n, 'k--')
    plt.legend(['relative roughness', 'roughness'])
    plt.xlabel('section')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title2}.png', dpi=350)
        print(f'{title2}.png saved')

    else:
        plt.show(block=False)

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
    ax[0,2].set_ylim([0, data['[C4, E4, G4]'] * 1.1])
    ax[0,2].spines['right'].set_visible(False)
    ax[0,2].spines['top'].set_visible(False)
    ax[0,2].set_ylabel('roughness\n(arbitrary units)')

    ax[1,0].stem(maj3_dyad.partials['hz'], maj3_dyad.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    ax[1,0].set_title('[C4, E4]')
    ax[1,1].stem(maj7_dyad.partials['hz'], maj7_dyad.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    ax[1,1].set_title('[C4, B4]')
    ax[1,2].bar(plot1_names, plot1_vals, fill=False, hatch='///')
    ax[1,2].set_ylim([0, data['[C4, E4, G4]'] * 1.1])
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

    ref_tone_short = SetharesTone(7)
    ref_tone_long = SetharesTone(14)
    test_tone = SetharesTone(7)
    T = two_octaves
    # T = TransposeDomain(-0.5, 24.5, 2401, 'ST_DIFF')

    roughness_short = roughness_curve(ref_tone_short, test_tone, transpose_domain=T, function_type='SETHARES', normalize=True)
    roughness_long = roughness_curve(ref_tone_long, test_tone, transpose_domain=T, function_type='SETHARES', normalize=True)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(T.domain, roughness_short, 'k')
    plt.plot(T.domain, roughness_long, 'k--')
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

# Figure 6a. Pair-overlap curve.
def ch2_fig6a(action):
    title = 'ch2_fig6a'

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

# Fi6ure 6b. Complex overlap curve.
def ch2_fig6b(action):
    title = 'ch2_fig6b'

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

def ch2_fig7(action):
    title = 'ch2_fig7'

    ref_tone = SetharesTone(7)
    test_tone = SetharesTone(7)
    fund = a3
    T = one_octave
    # T = TransposeDomain(-0.5, 12.5, 200, 'ST_DIFF')

    overlap_bell = overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='BELL')
    overlap_cos = overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='COS')
    overlap_cbw = overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='CBW')
    overlap_bell /= np.max(overlap_bell)
    overlap_cos /= np.max(overlap_cos)
    overlap_cbw /= np.max(overlap_cbw)

    Ks = [-0.2374, -2.374, -23.74]
    overlaps_k = [overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='BELL', options={
        'amp_type': 'MIN',
        'crossterms_only': False,
        'cutoff': False,
        'show_partials': False,
        'K': k
        }) for k in Ks
    ]
    overlaps_k = [curve / np.max(curve) for curve in overlaps_k]

    #Plot
    fig, ax = plt.subplots(2,1)
    fig.set_figheight(6)
    fig.set_figwidth(10)
    plt.tight_layout()
    plt.subplots_adjust(left=0.16, hspace=0.3, bottom=0.1)
    ax[0].plot(T.domain, overlap_bell, 'k')
    ax[0].plot(T.domain, overlap_cos, 'k--')
    ax[0].plot(T.domain, overlap_cbw, 'k-.')
    ax[0].legend(['current', 'cos', 'indicator'])
    ax[0].set_ylim(0, 1.1)
    ax[1].set_ylim(0, 1.1)
    ax[1].plot(T.domain, overlaps_k[0], 'k-.')
    ax[1].plot(T.domain, overlaps_k[1], 'k-')
    ax[1].plot(T.domain, overlaps_k[2], 'k--')
    ax[1].legend(['K = -0.24', 'K = -2.4', 'K = -24'])
    ax[0].xaxis.set_major_locator(MultipleLocator(1))
    ax[0].xaxis.set_major_formatter('{x:.0f}')
    ax[1].xaxis.set_major_locator(MultipleLocator(1))
    ax[1].xaxis.set_major_formatter('{x:.0f}')
    ax[0].set_xlabel('interval (semitones)')
    ax[0].set_ylabel('overlap\n(arbitrary units)')
    ax[0].yaxis.set_label_coords(-0.06, 0.50)
    ax[1].set_xlabel('interval (semitones)')
    ax[1].set_ylabel('relative roughness\n(arbitrary units)')
    ax[1].yaxis.set_label_coords(-0.06, 0.50)
    fig.add_artist(plt.Text(0.03, 0.75, '(a)', size=16.0, weight='bold'))
    fig.add_artist(plt.Text(0.03, 0.25, '(b)', size=16.0, weight='bold'))

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

# Figure 8. Plot of relative roughness over 1 octave, above A3.
def ch2_fig8(action):
    title = 'ch2_fig8'

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

def ch2_fig8_app(action):
    title = 'ch2_fig8_app'

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

# Figure 9. Sensitivity of relative roughness to presence of higher partials.
def ch2_fig9(action):
    title = 'ch2_fig9'

    ref_8 = SetharesTone(8)
    test_8 = SetharesTone(8)
    ref_9 = SetharesTone(9)
    test_9 = SetharesTone(9)
    T = one_octave
    # T = TransposeDomain(-0.5, 12.5, 11, 'ST_DIFF')

    rough_8 = roughness_curve(ref_8, test_8, transpose_domain=T, function_type='SETHARES', normalize=True)
    rough_9 = roughness_curve(ref_9, test_9, transpose_domain=T, function_type='SETHARES', normalize=True)
    overlap_8 = overlap_curve(ref_8, test_8, transpose_domain=T, function_type='BELL', normalize=True)
    overlap_9 = overlap_curve(ref_9, test_9, transpose_domain=T, function_type='BELL', normalize=True)
    ratio_8 = rough_8 / overlap_8
    ratio_9 = rough_9 / overlap_9
    ratio_8 /= max(ratio_8)
    ratio_9 /= max(ratio_9)

    # Plots
    fig, ax = plt.subplots(2,1)
    fig.set_figheight(6)
    fig.set_figwidth(10)
    plt.tight_layout()
    plt.subplots_adjust(left=0.16, hspace=0.3, bottom=0.1)
    ax[0].plot(T.domain, overlap_8, 'k')
    ax[0].plot(T.domain, overlap_9, 'k--')
    ax[0].legend(['8 partials', '9 partials'])
    ax[0].set_ylim(0, 1.1)
    ax[1].set_ylim(0, 1.1)
    ax[1].plot(T.domain, ratio_8, 'k')
    ax[1].plot(T.domain, ratio_9, 'k--')
    ax[1].legend(['8 partials', '9 partials'])
    ax[0].xaxis.set_major_locator(MultipleLocator(1))
    ax[0].xaxis.set_major_formatter('{x:.0f}')
    ax[1].xaxis.set_major_locator(MultipleLocator(1))
    ax[1].xaxis.set_major_formatter('{x:.0f}')
    ax[0].set_xlabel('interval (semitones)')
    ax[0].set_ylabel('overlap\n(arbitrary units)')
    ax[0].yaxis.set_label_coords(-0.06, 0.50)
    ax[1].set_xlabel('interval (semitones)')
    ax[1].set_ylabel('relative roughness\n(arbitrary units)')
    ax[1].yaxis.set_label_coords(-0.06, 0.50)
    ax[0].annotate('', xy=(2,0.1), xytext=(2,0.2), arrowprops={'arrowstyle': '->'})
    ax[1].annotate('', xy=(1.9,0.09), xytext=(1.5,0.03), arrowprops={'arrowstyle': '->'})
    fig.add_artist(plt.Text(0.03, 0.75, '(a)', size=16.0, weight='bold'))
    fig.add_artist(plt.Text(0.03, 0.25, '(b)', size=16.0, weight='bold'))

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

# Figure 10. Relative roughnesses of a major seventh chord and its subsets.
def ch2_fig10(action):
    title = 'ch2_fig10'

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

def ch2_fig11(action):
    title = 'ch2_fig11'

    ref_triad = SetharesMajTriad(12, a3)
    test_tone = SetharesTone(12, a3)
    T = TransposeDomain(-0.5, 17.5, 1801, 'ST_DIFF')

    roughness = roughness_curve(
        ref_triad,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES'
    )

    overlap = overlap_curve(
        ref_triad,
        test_tone,
        transpose_domain=T,
        function_type='BELL'
    )

    ratio = roughness / overlap
    ratio = ratio / np.max(ratio)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(T.domain, ratio, 'k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('relative roughness\n(arbitrary units)')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    # Some points to annotate
    triad_unison_coords = [51, 451, 751]
    triad_unison = list(zip(
        [T.domain[i] for i in triad_unison_coords],
        [ratio[i] for i in triad_unison_coords]
    ))
    for point in triad_unison:
        ax.plot(point[0], point[1], 'o', ms=20, mew=2, mfc='none', mec='k')

    triad_octave_coords = [1251, 1651]
    triad_octave = list(zip(
        [T.domain[i] for i in triad_octave_coords],
        [ratio[i] for i in triad_octave_coords]
    ))
    for point in triad_octave:
        ax.plot(point[0], point[1], 's', ms=20, mew=2, mfc='none', mec='k')

    triad_added_coords = [251, 951, 1151, 1451]
    triad_added = list(zip(
        [T.domain[i] for i in triad_added_coords],
        [ratio[i] for i in triad_added_coords]
    ))
    for point in triad_added:
        ax.plot(point[0], point[1], 'd', ms=20, mew=2, mfc='none', mec='k')

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig13(action):
    title = 'ch2_fig13'

    tim = SetharesTimbre(12)
    fund = midi_zero

    backdrop_pitches = [
        [62, 69, 74, 76, 81, 86],
        [62, 64, 69, 74, 76, 81, 86],
        [64, 69, 76, 81, 88],
        [64, 69, 71, 76, 81, 83, 88],
        [71, 76, 83, 88, 95, 100],
        [85, 90, 97, 102],
        [73, 80, 81, 85, 92, 93, 97, 102],
        [66, 68, 69, 71, 73, 78],
        [61, 66, 68, 69, 71, 73, 76, 80, 83, 88],
        [66, 68, 69, 76, 81, 88],
        [64, 66, 67, 69, 71, 74, 76, 81, 86]
    ]

    m18m_backdrops = [
        ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund) for chord in backdrop_pitches
    ]

    m18m_backdrop_diss = np.array([
        roughness_complex(MergedSpectrum(chord), 'SETHARES') for chord in m18m_backdrops
    ])

    m18m_backdrop_overlap = np.array([
        overlap_complex(MergedSpectrum(chord), 'BELL') for chord in m18m_backdrops
    ])

    m18m_backdrop_ratio = m18m_backdrop_diss / m18m_backdrop_overlap

    # Normalize so drone has roughness 1
    m18m_backdrop_ratio /= m18m_backdrop_ratio[0]

    # Plots
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(range(1,12), m18m_backdrop_ratio, 'k')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    plt.xlabel('section')
    plt.ylabel('relative roughness of pulsed chord\n(arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig14a(action):
    title = 'ch2_fig14a'

    tim = SetharesTimbre(12)
    fund_i = d4

    m18m_i_arch_a = [
        [0,7,12,14,19,24,4,-3,-8],
        [0,7,12,14,19,24,4,-8,-15],
        [0,7,12,14,19,24,16,-8,-15],
        [0,7,12,14,19,24,16,9,-12,-19],
        [0,7,12,14,19,24,16,-8,-15],
        [0,7,12,14,19,24,4,-8,-15],
        [0,7,12,14,19,24,4,-3,-8],
    ]

    m18m_i_arch_b = [
        [0,7,12,14,19,24,4,2,-1,-8],
        [0,7,12,14,19,24,14,4,-8,-13],
        [0,7,12,14,19,24,16,14,-13,-20],
        [0,7,12,14,19,24,16,11,-12,-17],
        [0,7,12,14,19,24,16,14,-13,-20],
        [0,7,12,14,19,24,14,4,-8,-13],
        [0,7,12,14,19,24,4,2,-1,-8],
    ]

    a_rough = np.array([roughness_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_i)), function_type='SETHARES') for chord in m18m_i_arch_a])
    a_overlap = np.array([overlap_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_i)), function_type='BELL') for chord in m18m_i_arch_a])
    a_ratio = a_rough / a_overlap
    a_ratio /= np.max(a_ratio)

    b_rough = np.array([roughness_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_i)), function_type='SETHARES') for chord in m18m_i_arch_b])
    b_overlap = np.array([overlap_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_i)), function_type='BELL') for chord in m18m_i_arch_b])
    b_ratio = b_rough / b_overlap
    b_ratio /= np.max(b_ratio)

    chord_names = ['I-a', 'I-b', 'I-c', 'I-d', 'I-c', 'I-b', 'I-a']

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.bar(chord_names, a_ratio, fill=False)
    ax.bar(chord_names, b_ratio, fill=False, hatch='///')
    plt.xlabel('chord pair (see example)')
    plt.ylabel('relative roughness\n(arbitrary units)')
    plt.ylim(ymin=0.5, ymax=1.5)
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig14b(action):
    title = 'ch2_fig14b'

    tim = SetharesTimbre(12)
    fund_ix = midi_zero
    m18m_ix_backdrop = [61, 66, 68, 69, 71, 73, 76, 80, 83, 88]
    m18m_ix_loop_top = [
        [],
        [45,52,61,68],
        [42,49,57,64],
        [42,47,57,64],
        [44,49,59,64]
    ]
    m18m_ix_loop = [m18m_ix_backdrop + chord for chord in m18m_ix_loop_top]

    sect_ix_rough = np.array([roughness_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_ix)), function_type='SETHARES') for chord in m18m_ix_loop])
    sect_ix_overlap = np.array([overlap_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_ix)), function_type='BELL') for chord in m18m_ix_loop])
    sect_ix_ratio = sect_ix_rough / sect_ix_overlap
    sect_ix_ratio /= np.max(sect_ix_ratio)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(5)
    ax.plot(['backdrop alone'] + list(range(1, 5)), sect_ix_ratio, 'k')
    plt.xlabel('chord (see example)')
    plt.ylabel('relative roughness\n(arbitrary units)')
    plt.ylim(ymin=0.5, ymax=1.5)
    ax.yaxis.set_label_coords(-0.1, 0.5)
    plt.subplots_adjust(left=0.16)


    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

def ch2_fig16(action):
    title = 'ch2_fig16'

    maxDenom = 12

    interval = []
    overlap_ideal = []

    # Idealized overlap function
    for denom in range(1, maxDenom + 1):
        for num in range(denom, (2 * denom) + 1):
            if np.gcd(num, denom) == 1:
                interval.append(float(num) / denom)
                overlap_ideal.append(1 / float(num))

    # Reference
    ref_tone = FlatSawTone(12)
    test_tone = FlatSawTone(12)
    T = TransposeDomain(1.0, 2.0, 1000, 'SCALE_FACTOR')

    overlap = overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='BELL', normalize=True)

    # Plot
    fig, ax = plt.subplots()
    ax.plot(T.domain, overlap, 'k--', linewidth=0.5)
    ax.stem(interval, overlap_ideal, linefmt='k', markerfmt=' ', basefmt=' ')
    ax.set_ylim(0)
    plt.xlabel('interval (ratio)')
    plt.ylabel('overlap (arbitrary units)')
    ax.xaxis.set_major_formatter('{x:.1f}')
    ax.yaxis.set_label_coords(-0.1, 0.5)

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

def __main__(argv):
    action = ''
    if len(argv) > 1:
        action = argv[1].lower()

    # ch2_fig1a(action)
    # ch2_fig2a(action)
    # ch2_fig2b(action)
    # ch2_fig3_13(action)
    # ch2_fig4(action)
    # ch2_fig5(action)
    # ch2_fig6(action)
    # ch2_fig7(action)
    # ch2_fig8(action)
    # ch2_fig9(action)
    # ch2_fig10(action)
    # ch2_fig11(action)
    # ch2_fig12(action)
    # ch2_fig13(action)
    # ch2_fig14a(action)
    ch2_fig14b(action)
    # ch2_fig16(action)

if __name__ == '__main__':
    __main__(sys.argv)
