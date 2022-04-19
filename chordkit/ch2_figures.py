import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib import pyplot as plt
import sys

from chord_utils import MergedSpectrum, ChordSpectrum, TransposeDomain
from defaults import (SineTone, SetharesTone, HarrisonTone, FlatSawTone,
    SetharesMajTriad, HarrisonMajTriad, FlatSawTimbre, HarrisonTimbre,
    SetharesTimbre, c3, c4, d4, midi_zero, a3, a4, one_octave, two_octaves,
    two_octaves_symm)
from chord_plots import overlap_curve, roughness_curve
from roughness_models import roughness_complex
from overlap_models import overlap_complex
from pair_constants import AUDITORY_CONSTANTS as ac
from chord_lists import (fratres_8vedrone_nocb8ves, fratres_8vedrone_cb8va,
    fratres_no8ves, fratres_phrase_end_sonorities, fratres_phrase_start_sonorities,
    fratres_tenths_only, fratres_tenths_only_thindrone)


figure_idx = {
    'helmholtz_pair': '1a',
    'timbre_plots': '2',
    'pair_roughness': '3a',
    'complex_roughness': '3b', # add on from here
    'fratres_roughness': '6',
    'cardinality_proximity': '7',
    'octave_drift_sethares': '8a',
    'octave_drift_parncutt': '8b',
    'pair_overlap_sethares': '9a1',
    'pair_overlap_parncutt': '9a2',
    'complex_overlap_sethares': '9b1',
    'complex_overlap_parncutt': '9b2',
    'vary_k_overlap': '10',
    'rel_roughness_8ve_h11_sethares': '11a1',
    'rel_roughness_8ve_h11_parncutt': '11a2',
    'rel_roughness_8ve_e11_sethares': '11b1',
    'rel_roughness_8ve_e11_parncutt': '11b2',
    'different_operations_roughness_overlap': '11_app',
    'maj7_chord': '12',
    'add_to_triad': '13',
    'm18m_chorale': '14',
    'm18m_i': '15',
    'm18m_ix': '16',
    'high_partials_sensitivity': '17',
    'idealized_overlap': '19',
    'complex_roughness_helmholtz': '1b_app'
}

def save_show(name, action):
    if action.lower() == 'save':
        title = f'ch2_fig{figure_idx[name]}_{name}.png'
        plt.savefig(title, dpi=350)
        print(f'{title} saved')
    
    else:
        plt.show()
    
    plt.close()

# A plot of Helmholtz’s pair-roughness function (Helmholtz 1895, appendix XV)
def pair_roughness_helmholtz(action):
    name = 'pair_roughness_helmholtz'

    ref_tone = SineTone(a4)
    test_tone = SineTone(a4)
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

    save_show(name, action)

# Plots of individual timbres
def timbre_plots(action):
    name = 'timbre_plots'
    
    h_tim = HarrisonTimbre(11)
    s_tim = SetharesTimbre(11)
    fund = 1

    h = ChordSpectrum([0], 'ST_DIFF', timbre=h_tim, fund_hz=fund)
    s = ChordSpectrum([0], 'ST_DIFF', timbre=s_tim, fund_hz=fund)

    f0 = r'$\mathsf{f_0}$'
    freqs = [f0] + [str(x) + f0 for x in range(2, 12)]
    
    # Plot
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    plt.subplots_adjust(wspace=0.3, hspace=0.7)
    for panel in ax:
        panel.spines['right'].set_visible(False)
        panel.spines['top'].set_visible(False)
        panel.set_ylim([0, 1.1])
        panel.set_xlim([-1, 12.])
        panel.set_ylabel('amplitude\n(arbitrary units)')
        panel.set_xlabel('frequency (Hz)')

    ax[0].stem(freqs, h.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    ax[0].set_title('H(11)')
    ax[1].stem(freqs, s.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    ax[1].set_title(r'E$_{\mathsf{0.88}}$(11)', usetex=True)
    
    fig.add_artist(plt.Text(0.05, 0.8, '(a)', size=16.0, weight='bold'))
    fig.add_artist(plt.Text(0.5, 0.8, '(b)', size=16.0, weight='bold'))

    save_show(name, action)


# Sethares + Parncutt pair roughness function (Sethares 1993, BPL 1996)
def pair_roughness(action):
    name = 'pair_roughness'

    ref_tone = SineTone(a4)
    test_tone = SineTone(a4)
    T = two_octaves_symm

    roughness_sethares = roughness_curve(
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
    
    
    roughness_parncutt = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='PARNCUTT',
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
    plt.plot(T.domain, roughness_sethares, 'k', linewidth=1)
    plt.plot(T.domain, roughness_parncutt, 'k', linewidth=3)
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.subplots_adjust(left=0.15)
    ax.yaxis.set_label_coords(-0.13, 0.5)

    save_show(name, action)

# Figure 2b. Sethares + Parncutt complex roughness function
def complex_roughness(action):
    name = 'complex_roughness'

    # Would make sense to use `sethares_timbre` here, but it has too few partials (7)
    # for the overlap function later.
    # ref_tone = HarrisonTone(11, c3)
    # test_tone = HarrisonTone(11, c3)
    ref_tone = HarrisonTone(11, a4)
    test_tone = HarrisonTone(11, a4)
    T = one_octave

    sethares_roughness = roughness_curve(
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
    
    parncutt_roughness = roughness_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='PARNCUTT',
        normalize=True,
        options={
            'crossterms_only': False,
            'cutoff': False,
            'normalize': True,
            'original': True,
            'show_partials': False
        }
    )

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(T.domain, sethares_roughness, 'k', linewidth=1)
    plt.plot(T.domain, parncutt_roughness, 'k', linewidth=3)
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 9})
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)

# Fratre graphs
# Figure 5. HKP and Sethares roughness for Fratres chords
# Figure 13. HKP and Sethares relative roughness for Fratres chords
def fratres_roughness(action):
    name1a = 'fratres_roughness_full'
    name1b = 'fratres_roughness_no_cb8ves'
    name1c = 'fratres_roughness_structural'
    name1d = 'fratres_roughness_tenths'
    name1e = 'fratres_roughness_tenths_no8vedrone'
    name2a = 'fratres_ratio_full'
    name2b = 'fratres_ratio_no_cb8ves'
    name2c = 'fratres_ratio_structural'
    name2d = 'fratres_ratio_tenths'
    name2e = 'fratres_ratio_tenths_no8vedrone'
    
    tim = HarrisonTimbre(11)
    fund = midi_zero
    
    # A helpful function to normalize so the first value is 1
    def first_value_one(lst):
        return lst / lst[0]
    
    # Helper function perform the various manipulations for each curve
    def get_curves(lst):
        fratres = [ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund) for chord in lst]
        sethares_roughness = np.array([roughness_complex(chord, 'SETHARES') for chord in fratres])
        sethares_overlap = np.array([overlap_complex(chord, 'SETHARES_BELL') for chord in fratres])
        parncutt_roughness = np.array([roughness_complex(chord, 'PARNCUTT') for chord in fratres])
        parncutt_overlap = np.array([overlap_complex(chord, 'PARNCUTT_BELL') for chord in fratres])
        
        sethares_ratio = sethares_roughness / sethares_overlap
        parncutt_ratio = parncutt_roughness / parncutt_overlap
        
        sethares_roughness_n = first_value_one(sethares_roughness)
        parncutt_roughness_n = first_value_one(parncutt_roughness)
        sethares_ratio_n = first_value_one(sethares_ratio)
        parncutt_ratio_n = first_value_one(parncutt_ratio)
        
        return {
            'sethares_roughness': sethares_roughness_n,
            'parncutt_roughness': parncutt_roughness_n,
            'sethares_ratio': sethares_ratio_n,
            'parncutt_ratio': parncutt_ratio_n
        }
    
    # The lower octave is not doubled, following the holograph score shown at
    # on the Arvo Pärt Centre website, https://www.arvopart.ee/en/arvo-part/work/390/
    
    fratres_all = get_curves(fratres_8vedrone_cb8va)
    fratres_no_cb = get_curves(fratres_8vedrone_nocb8ves)
    fratres_sections_start = get_curves(fratres_phrase_start_sonorities)
    fratres_sections_end = get_curves(fratres_phrase_end_sonorities)
    fratres_tenths = get_curves(fratres_tenths_only)
    fratres_tenths_thindrone = get_curves(fratres_tenths_only_thindrone)
    
    section_axis = ['drone'] + list(range(1,10))
    
    # Plots
    
    # Fig 5a
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_all['sethares_roughness'])
    plt.plot(np.arange(l), fratres_all['sethares_roughness'], 'k', linewidth=1)
    plt.plot(np.arange(l), fratres_all['parncutt_roughness'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.xlabel('quarter-note beats from start')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name1a, action)
    
    # Fig 5b
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_no_cb['sethares_roughness'])
    plt.plot(np.arange(l), fratres_no_cb['sethares_roughness'], 'k', linewidth=1)
    plt.plot(np.arange(l), fratres_no_cb['parncutt_roughness'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.xlabel('quarter-note beats from start')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name1b, action)
    
    # Fig 5c
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_sections_start)
    plt.plot(section_axis, fratres_sections_start['sethares_roughness'], 'k', linewidth=1)
    plt.plot(section_axis, fratres_sections_start['parncutt_roughness'], 'k', linewidth=3)
    plt.plot(section_axis, fratres_sections_end['sethares_roughness'], 'k', linewidth=1)
    plt.plot(section_axis, fratres_sections_end['parncutt_roughness'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.xlabel('section')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0, ymax=3.4)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name1c, action)
    
    # Fig 5d
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_tenths)
    plt.plot(section_axis, fratres_tenths['sethares_roughness'], 'k', linewidth=1)
    plt.plot(section_axis, fratres_tenths['parncutt_roughness'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.xlabel('section')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0, ymax=3.4)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name1d, action)
    
    # Fig 5e
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_tenths)
    plt.plot(section_axis, fratres_tenths_thindrone['sethares_roughness'], 'k', linewidth=1)
    plt.plot(section_axis, fratres_tenths_thindrone['parncutt_roughness'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5},loc="upper left")
    plt.xlabel('section')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name1e, action)
    
    # Fig 15a
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_all['sethares_ratio'])
    plt.plot(np.arange(l), fratres_all['sethares_ratio'], 'k', linewidth=1)
    plt.plot(np.arange(l), fratres_all['parncutt_ratio'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.xlabel('quarter-note beat')
    plt.ylabel('roughness/overlap (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name2a, action)
    
    # Fig 15b
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_no_cb['sethares_roughness'])
    plt.plot(np.arange(l), fratres_no_cb['sethares_ratio'], 'k', linewidth=1)
    plt.plot(np.arange(l), fratres_no_cb['parncutt_ratio'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.xlabel('quarter-note beats from start')
    plt.ylabel('roughness/overlap (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name2b, action)
    
    # Fig 15c
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_sections_start)
    plt.plot(section_axis, fratres_sections_start['sethares_ratio'], 'k', linewidth=1)
    plt.plot(section_axis, fratres_sections_start['parncutt_ratio'], 'k', linewidth=3)
    plt.plot(section_axis, fratres_sections_end['sethares_ratio'], 'k', linewidth=1)
    plt.plot(section_axis, fratres_sections_end['parncutt_ratio'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.xlabel('section')
    plt.ylabel('roughness/overlap (arbitrary units)')
    plt.ylim(ymin=0.0, ymax=3.4)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name2c, action)
    
    # Fig 15d
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_tenths)
    plt.plot(section_axis, fratres_tenths['sethares_ratio'], 'k', linewidth=1)
    plt.plot(section_axis, fratres_tenths['parncutt_ratio'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5})
    plt.xlabel('section')
    plt.ylabel('roughness/overlap (arbitrary units)')
    plt.ylim(ymin=0.0, ymax=3.4)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name2d, action)
    
    # Fig 15e
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    l = len(fratres_tenths)
    plt.plot(section_axis, fratres_tenths_thindrone['sethares_ratio'], 'k', linewidth=1)
    plt.plot(section_axis, fratres_tenths_thindrone['parncutt_ratio'], 'k', linewidth=3)
    plt.legend(['S model', 'HKP model'],edgecolor='k',prop={'size': 8.5},loc="upper left")
    plt.xlabel('section')
    plt.ylabel('roughness/overlap (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.yaxis.set_label_coords(-0.06, 0.5)
    
    save_show(name2e, action)

# Figure 6. Discrepancies between HKP/S roughness and dissonance.
def cardinality_proximity(action):
    name = 'cardinality_proximity'

    tim = HarrisonTimbre(11)
    fund = c4

    c = ChordSpectrum([0], 'ST_DIFF', timbre=tim, fund_hz=fund)
    e = ChordSpectrum([4], 'ST_DIFF', timbre=tim, fund_hz=fund)
    g = ChordSpectrum([7], 'ST_DIFF', timbre=tim, fund_hz=fund)
    b = ChordSpectrum([11], 'ST_DIFF', timbre=tim, fund_hz=fund)
    maj3_dyad = ChordSpectrum([0, 4], 'ST_DIFF', timbre=tim, fund_hz=fund)
    maj53_triad = ChordSpectrum([0, 4, 7], 'ST_DIFF', timbre=tim, fund_hz=fund)
    maj7_dyad = ChordSpectrum([0, 11], 'ST_DIFF', timbre=tim, fund_hz=fund)

    sethares_data = {
        '[C4, E4]': roughness_complex(maj3_dyad, 'SETHARES'),
        '[C4, E4, G4]': roughness_complex(maj53_triad, 'SETHARES'),
        '[C4, B4]': roughness_complex(maj7_dyad, 'SETHARES')
    }
    
    parncutt_data = {
        '[C4, E4]': roughness_complex(maj3_dyad, 'PARNCUTT'),
        '[C4, E4, G4]': roughness_complex(maj53_triad, 'PARNCUTT'),
        '[C4, B4]': roughness_complex(maj7_dyad, 'PARNCUTT')
    }

    plot0_names = ['[C4, E4]', '[C4, E4, G4]']
    plot1_names = ['[C4, E4]', '[C4, B4]']
    sethares_plot0_vals = [sethares_data[name] for name in plot0_names]
    parncutt_plot0_vals = [parncutt_data[name] for name in plot0_names]
    sethares_plot1_vals = [sethares_data[name] for name in plot1_names]
    parncutt_plot1_vals = [parncutt_data[name] for name in plot1_names]

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

    xaxis = np.arange(2)
    slide = 0.15
    
    ax[0,0].stem(c.partials['hz'], c.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    markerface1, _, _ = ax[0,0].stem(e.partials['hz'], e.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    markerface1.set_markerfacecolor('w')
    ax[0,0].set_xlim([0, 5550])
    ax[0,0].set_title('[C4, E4]')
    
    ax[0,1].stem(c.partials['hz'], c.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    markerface1, _, _ = ax[0,1].stem(e.partials['hz'], e.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    markerface1.set_markerfacecolor('w')
    markerface2, _, _ = ax[0,1].stem(g.partials['hz'], e.partials['amp'], linefmt='k', markerfmt='kD', basefmt=' ')
    markerface2.set_markerfacecolor('w')
    ax[0,1].set_xlim([0, 5550])
    ax[0,1].set_title('[C4, E4, G4]')

    ax[0,2].bar(xaxis - slide, sethares_plot0_vals, width=0.3, fill=False, hatch='///', tick_label=plot0_names)
    ax[0,2].bar(xaxis + slide, parncutt_plot0_vals, width=0.3, fill=True, color='k')
    ax[0,2].legend(['S model', 'HKP model'], edgecolor='k', prop={'size': 8.5})
    ax[0,2].set_ylim([0, max(parncutt_data['[C4, E4, G4]'], sethares_data['[C4, E4, G4]']) * 1.7])
    ax[0,2].spines['right'].set_visible(False)
    ax[0,2].spines['top'].set_visible(False)
    ax[0,2].set_ylabel('roughness\n(arbitrary units)')

    ax[1,0].stem(c.partials['hz'], c.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    markerface1, _, _ = ax[1,0].stem(e.partials['hz'], e.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    markerface1.set_markerfacecolor('w')
    ax[1,0].set_xlim([0, 5550])
    ax[1,0].set_title('[C4, E4]')
    
    ax[1,1].stem(c.partials['hz'], c.partials['amp'], linefmt='k', markerfmt='ko', basefmt=' ')
    markerface1, _, _ = ax[1,1].stem(b.partials['hz'], e.partials['amp'], linefmt='k', markerfmt='ks', basefmt=' ')
    ax[1,1].set_xlim([0, 5550])
    ax[1,1].set_title('[C4, B4]')
    
    ax[1,2].bar(xaxis - slide, sethares_plot1_vals, width=0.3, fill=False, hatch='///', tick_label=plot1_names)
    ax[1,2].bar(xaxis + slide, parncutt_plot1_vals, width=0.3, fill=True, color='k')
    ax[1,2].legend(['S model', 'HKP model'], edgecolor='k', prop={'size': 8.5})
    ax[1,2].set_ylim([0, max(parncutt_data['[C4, E4]'], sethares_data['[C4, E4]']) * 1.7])
    ax[1,2].spines['right'].set_visible(False)
    ax[1,2].spines['top'].set_visible(False)
    ax[1,2].set_ylabel('roughness\n(arbitrary units)')

    fig.add_artist(plt.Line2D([0, 1], [0.48, 0.48], color='k'))
    fig.add_artist(plt.Text(0.02, 0.75, '(a)', size=16.0, weight='bold'))
    fig.add_artist(plt.Text(0.02, 0.25, '(b)', size=16.0, weight='bold'))

    save_show(name, action)

# More partials in the lower tone can reduce the proximity effect (Sethares)
def octave_drift_sethares(action):
    name = 'octave_drift_sethares'

    ref_tone_short = HarrisonTone(11)
    ref_tone_long = HarrisonTone(22)
    test_tone = HarrisonTone(11)
    T = two_octaves

    sethares_roughness_short = roughness_curve(ref_tone_short, test_tone, transpose_domain=T, function_type='SETHARES', normalize=True)
    sethares_roughness_long = roughness_curve(ref_tone_long, test_tone, transpose_domain=T, function_type='SETHARES', normalize=True)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(T.domain, sethares_roughness_long, 'k', linewidth=1)
    plt.plot(T.domain, sethares_roughness_short, 'k--', linewidth=1)
    plt.legend(['S model, different times', 'S model, same timbres'], edgecolor='k', prop={'size': 8.5})
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)

# More partials in the lower tone can reduce the proximity effect (Parncutt)
def octave_drift_parncutt(action):
    name = 'octave_drift_parncutt'

    ref_tone_short = HarrisonTone(11)
    ref_tone_long = HarrisonTone(22)
    test_tone = HarrisonTone(11)
    T = two_octaves

    parncutt_roughness_short = roughness_curve(ref_tone_short, test_tone, transpose_domain=T, function_type='PARNCUTT', normalize=True)
    parncutt_roughness_long = roughness_curve(ref_tone_long, test_tone, transpose_domain=T, function_type='PARNCUTT', normalize=True)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    plt.plot(T.domain, parncutt_roughness_long, 'k', linewidth=2)
    plt.plot(T.domain, parncutt_roughness_short, 'k--', linewidth=2)
    plt.legend(['HKP model, different timbres', 'HKP model, same timbres'], edgecolor='k', prop={'size': 8.5})
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness (arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)

# Pair-overlap curve (Sethares-like)
def pair_overlap_sethares(action):
    name = 'pair_overlap'

    ref_tone = SineTone(a4)
    test_tone = SineTone(a4)
    T = two_octaves_symm

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES_BELL',
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
    ax.plot(T.domain, overlap, color='k', linestyle='-', linewidth=1)
    ax.plot(T.domain, roughness, color='k', linestyle='--', linewidth=1)
    ax.legend(['S overlap', 'S roughness'], edgecolor='k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('(arbitrary units)')
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.ylim(ymin=0.0)
    plt.subplots_adjust(left=0.15)
    ax.yaxis.set_label_coords(-0.13, 0.5)

    save_show(name, action)

# Pair-overlap curve (Parncutt-like)
def pair_overlap_parncutt(action):
    name = 'pair_overlap_parncutt'

    ref_tone = SineTone(a4)
    test_tone = SineTone(a4)
    T = two_octaves_symm

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='PARNCUTT_BELL',
        normalize=True,
        options={
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
        function_type='PARNCUTT',
        normalize=True,
        options={
            'crossterms_only': False,
            'cutoff': False,
            'original': False,
            'show_partials': False
        }
    )

    # Plot
    _, ax = plt.subplots()
    ax.plot(T.domain, overlap, color='k', linestyle='-', linewidth=2)
    ax.plot(T.domain, roughness, color='k', linestyle='--', linewidth=2)
    ax.legend(['HKP overlap', 'HKP roughness'], edgecolor='k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('(arbitrary units)')
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.xaxis.set_minor_locator(MultipleLocator(1))
    plt.ylim(ymin=0.0)
    plt.subplots_adjust(left=0.15)
    ax.yaxis.set_label_coords(-0.13, 0.5)

    save_show(name, action)

# Complex overlap curve (Sethares-like)
def complex_overlap_sethares(action):
    name = 'complex_overlap_sethares'

    ref_tone = HarrisonTone(11, a3)
    test_tone = HarrisonTone(11, a3)
    T = one_octave

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES_BELL',
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

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(T.domain, overlap, 'k', linewidth=1)
    ax.plot(T.domain, roughness, 'k--', linewidth=1)
    ax.legend(['S overlap', 'S roughness'], edgecolor='k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('(arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)

# Complex overlap curve (Parncutt-like)
def complex_overlap_parncutt(action):
    name = 'complex_overlap_parncutt'

    ref_tone = HarrisonTone(11, a3)
    test_tone = HarrisonTone(11, a3)
    T = one_octave

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='PARNCUTT_BELL',
        normalize=False,
        options={
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
        function_type='PARNCUTT',
        normalize=False,
        options={
            'crossterms_only': False,
            'cutoff': False,
            'original': False,
            'show_partials': False
        }
    )

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(T.domain, overlap, 'k', linewidth=2)
    ax.plot(T.domain, roughness, 'k--', linewidth=2)
    ax.legend(['HKP overlap', 'HKP roughness'], edgecolor='k')
    plt.xlabel('interval (semitones)')
    plt.ylabel('(arbitrary units)')
    plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)

# Effects of varying slope of overlap curve
def vary_k_overlap(action):
    name = 'vary_k_overlap'

    fund = a3
    ref_tone = HarrisonTone(11, fund)
    test_tone = HarrisonTone(11, fund)
    T = one_octave
    # T = TransposeDomain(-0.5, 12.5, 200, 'ST_DIFF')

    overlap_sethares_bell = overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='SETHARES_BELL')
    overlap_parncutt_bell = overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='PARNCUTT_BELL')
    overlap_cos = overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='COS')
    overlap_cbw = overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='CBW')
    overlap_sethares_bell /= np.max(overlap_sethares_bell)
    overlap_parncutt_bell /= np.max(overlap_parncutt_bell)
    overlap_cos /= np.max(overlap_cos)
    overlap_cbw /= np.max(overlap_cbw)

    Ks = [-0.2374, -2.374, -23.74]
    sethares_overlaps_k = [overlap_curve(ref_tone, test_tone, transpose_domain=T, function_type='SETHARES_BELL', options={
        'amp_type': 'MIN',
        'crossterms_only': False,
        'cutoff': False,
        'show_partials': False,
        'K': k
        }) for k in Ks
    ]
    sethares_overlaps_k = [curve / np.max(curve) for curve in sethares_overlaps_k]

    #Plot
    fig, ax = plt.subplots(2,1)
    fig.set_figheight(6)
    fig.set_figwidth(10)
    plt.tight_layout()
    plt.subplots_adjust(left=0.16, hspace=0.3, bottom=0.1)
    ax[0].plot(T.domain, overlap_sethares_bell, 'k', linewidth=1)
    ax[0].plot(T.domain, overlap_parncutt_bell, 'k', linewidth=2)
    ax[0].plot(T.domain, overlap_cos, 'k--')
    ax[0].plot(T.domain, overlap_cbw, 'k-.')
    ax[0].legend(['S-like model', 'HKP-like model', 'cos', 'indicator'], edgecolor='k')
    ax[0].set_ylim(0, 1.1)
    ax[1].set_ylim(0, 1.1)
    ax[1].plot(T.domain, sethares_overlaps_k[0], 'k-.')
    ax[1].plot(T.domain, sethares_overlaps_k[1], 'k-')
    ax[1].plot(T.domain, sethares_overlaps_k[2], 'k--')
    ax[1].legend(['K = -0.24', 'K = -2.4', 'K = -24'], edgecolor='k')
    ax[0].xaxis.set_major_locator(MultipleLocator(1))
    ax[0].xaxis.set_major_formatter('{x:.0f}')
    ax[1].xaxis.set_major_locator(MultipleLocator(1))
    ax[1].xaxis.set_major_formatter('{x:.0f}')
    ax[0].set_xlabel('interval (semitones)')
    ax[0].set_ylabel('overlap\n(arbitrary units)')
    ax[0].yaxis.set_label_coords(-0.06, 0.50)
    ax[1].set_xlabel('interval (semitones)')
    ax[1].set_ylabel('S-like overlap\n(arbitrary units)')
    ax[1].yaxis.set_label_coords(-0.06, 0.50)
    fig.add_artist(plt.Text(0.03, 0.75, '(a)', size=16.0, weight='bold'))
    fig.add_artist(plt.Text(0.03, 0.25, '(b)', size=16.0, weight='bold'))

    save_show(name, action)

# Plot of Sethares-like relative roughness over 1 octave, above A3, H(11) tone.
def rel_roughness_8ve_h11_sethares(action):
    name = 'rel_roughness_8ve_h11_sethares'

    ref_tone = HarrisonTone(11, a3)
    test_tone = HarrisonTone(11, a3)
    T = one_octave

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES_BELL',
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

    log_ratio = np.log(roughness / overlap)
    ratio = (roughness / overlap)

    log_ratio = log_ratio / np.max(np.abs(log_ratio))
    ratio = ratio / np.max(ratio)
    roughness = roughness / np.max(roughness)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(T.domain, log_ratio, 'k', linewidth=1)
    # ax.plot(T.domain, ratio, 'k', linewidth=1)
    # ax.plot(T.domain, roughness, 'k--', linewidth=1)
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness\n(arbitrary units)')
    ax.legend(['S-like relative roughness', 'S-model roughness'], edgecolor='k', loc='upper center')
    # plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)

# Plot of Parncutt-like relative roughness over one octave, above A3, H(11) tone.
def rel_roughness_8ve_h11_parncutt(action):
    name = 'rel_roughness_8ve_h11_parncutt'

    ref_tone = HarrisonTone(11, a3)
    test_tone = HarrisonTone(11, a3)
    T = one_octave

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='PARNCUTT_BELL',
        normalize=False,
        options={
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
        function_type='PARNCUTT',
        normalize=False,
        options={
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    log_ratio = np.log(roughness / overlap)
    ratio = (roughness / overlap)

    log_ratio = log_ratio / np.max(np.abs(log_ratio))
    ratio = ratio / np.max(ratio)
    roughness = roughness / np.max(roughness)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(T.domain, log_ratio, 'k', linewidth=2)
    # ax.plot(T.domain, ratio, 'k', linewidth=2)
    # ax.plot(T.domain, roughness, 'k--', linewidth=2)
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness\n(arbitrary units)')
    ax.legend(['HKP-like relative roughness', 'HKP-model roughness'], edgecolor='k', loc='upper center')
    # plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    if action.lower() == 'save':
        plt.savefig(f'{title}.png', dpi=350)
        print(f'{title}.png saved')
    else:
        plt.show()

# Plot of Sethares-like relative roughness over one octave, above A3, E(11) tone.
def rel_roughness_8ve_e11_sethares(action):
    name = 'rel_roughness_8ve_e11_sethares'

    ref_tone = SetharesTone(11, a3)
    test_tone = SetharesTone(11, a3)
    T = one_octave

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES_BELL',
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

    log_ratio = np.log(roughness / overlap)
    ratio = (roughness / overlap)

    log_ratio = log_ratio / np.max(np.abs(log_ratio))
    ratio = ratio / np.max(ratio)
    roughness = roughness / np.max(roughness)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(T.domain, log_ratio, 'k', linewidth=1)
    # ax.plot(T.domain, ratio, 'k', linewidth=1)
    # ax.plot(T.domain, roughness, 'k--', linewidth=1)
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness\n(arbitrary units)')
    ax.legend(['S-like relative roughness', 'S-model roughness'], edgecolor='k', loc='upper center')
    # plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)

# Plot of Parncutt-like relative roughness over one octave, above A3, E(11) tone.
def rel_roughness_8ve_e11_parncutt(action):
    name = 'rel_roughness_8ve_e11_parncutt'

    ref_tone = SetharesTone(11, a3)
    test_tone = SetharesTone(11, a3)
    T = one_octave

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='PARNCUTT_BELL',
        normalize=False,
        options={
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
        function_type='PARNCUTT',
        normalize=False,
        options={
          'crossterms_only': False,
          'cutoff': False,
          'original': False,
          'show_partials': False
        }
    )

    log_ratio = np.log(roughness / overlap)
    ratio = (roughness / overlap)

    log_ratio = log_ratio / np.max(np.abs(log_ratio))
    ratio = ratio / np.max(ratio)
    roughness = roughness / np.max(roughness)

    # Plot
    fig, ax = plt.subplots()
    fig.set_figwidth(10)
    ax.plot(T.domain, log_ratio, 'k', linewidth=2)
    # ax.plot(T.domain, ratio, 'k', linewidth=2)
    # ax.plot(T.domain, roughness, 'k--', linewidth=2)
    plt.xlabel('interval (semitones)')
    plt.ylabel('roughness\n(arbitrary units)')
    ax.legend(['HKP-like relative roughness', 'HKP-model roughness'], edgecolor='k', loc='upper center')
    # plt.ylim(ymin=0.0)
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)

# Sethares-like relative-roughness curve of H(11) tones over one 8ve,
# along with some other operations on the roughness and overlap curves.
def different_operations_roughness_overlap(action):
    name = 'different_operations_roughness_overlap'

    ref_tone = HarrisonTone(11)
    test_tone = HarrisonTone(11)
    T = one_octave

    overlap1= overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES_BELL',
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
    plt.ylabel('(arbitrary units)')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.xaxis.set_major_formatter('{x:.0f}')
    ax.yaxis.set_label_coords(-0.06, 0.5)

    save_show(name, action)



# Relative roughnesses of a major seventh chord and its subsets.
def maj7_chord(action):
    name = 'maj7_chord'

    # tim = HarrisonTimbre(11)
    tim = SetharesTimbre(11)
    fund = a3

    # chord_names = [
    #     ('[C4, E4]', [0, 4]),
    #     ('[C4, G4]', [0, 7]),
    #     ('[C4, B4]', [0, 11]),
    #     ('[E4, G4]', [4, 7]),
    #     ('[E4, B4]', [4, 11]),
    #     ('[G4, B4]', [7, 11]),
    #     ('[C4, E4, G4]', [0, 4, 7]),
    #     ('[C4, E4, B4]', [0, 4, 11]),
    #     ('[C4, G4, B4]', [0, 7, 11]),
    #     ('[E4, G4, B4]', [4, 7, 11]),
    #     ('[C4, E4, G4, B4]', [0, 4, 7, 11])
    # ]
    
    chord_names = [
        ('0', [0, 0]),
        ('1', [0, 1]),
        ('2', [0, 2]),
        ('3', [0, 3]),
        ('4', [0, 4]),
        ('5', [0, 5]),
        ('6', [0, 6]),
        ('7', [0, 7]),
        ('8', [0, 8]),
        ('9', [0, 9]),
        ('10', [0, 10]),
        ('11', [0, 11])
    ]

    chords = [ChordSpectrum(chord_name[1], 'ST_DIFF', timbre=tim, fund_hz=fund) for chord_name in chord_names]
    # roughnesses = np.array([roughness_complex(chord, 'SETHARES') for chord in chords])
    # overlaps = np.array([overlap_complex(chord, 'SETHARES_BELL') for chord in chords])
    roughnesses = np.array([roughness_complex(chord, 'PARNCUTT') for chord in chords])
    overlaps = np.array([overlap_complex(chord, 'PARNCUTT_BELL') for chord in chords])
    log_ratios = np.log(roughnesses / overlaps)
    # ratios = (roughnesses / overlaps)

    chord_data = zip(chord_names, roughnesses, log_ratios)
    # chord_data = zip(chord_names, roughnesses, ratios)
    # print(list(zip(*sorted(chord_data, key=lambda chord: chord[1]))))
    [roughness_sorted_names, roughness_sorted_vals, _] = list(zip(*sorted(chord_data, key=lambda chord: chord[1])))
    chord_data = zip(chord_names, roughnesses, log_ratios)
    # chord_data = zip(chord_names, roughnesses, ratios)
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
    ax[0].set_xlabel('interval above A3')
    ax[1].set_ylabel('relative roughness\n(arbitrary units)')
    ax[1].set_xlabel('interval above A3')
    # ax[0].tick_params(axis='x', labelrotation=90)
    # ax[1].tick_params(axis='x', labelrotation=90)
    plt.subplots_adjust(bottom=0.3)

    save_show(name, action)

# Adding one note to a triad
def add_to_triad(action):
    name = 'add_to_triad'

    ref_triad = HarrisonMajTriad(11, a3)
    test_tone = HarrisonTone(11, a3)
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
        function_type='SETHARES_BELL'
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

    save_show(name, action)

# Music for 18 Musicians chorale
def m18m_chorale(action):
    name = 'm18m_chorale'

    tim = HarrisonTimbre(11)
    fund = midi_zero

    backdrop_pitches = [
        # data redacted
    ]

    m18m_backdrops = [
        ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund) for chord in backdrop_pitches
    ]

    m18m_backdrop_diss = np.array([
        roughness_complex(MergedSpectrum(chord), 'SETHARES') for chord in m18m_backdrops
    ])

    m18m_backdrop_overlap = np.array([
        overlap_complex(MergedSpectrum(chord), 'SETHARES_BELL') for chord in m18m_backdrops
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

    save_show(name, action)

# Music for 18 Musicians, Section I
def m18m_i(action):
    name = 'm18m_i'

    tim = HarrisonTimbre(11)
    fund_i = d4

    m18m_i_arch_a = [
        # data redacted
    ]

    m18m_i_arch_b = [
        # data redacted
    ]

    a_rough = np.array([roughness_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_i)), function_type='SETHARES') for chord in m18m_i_arch_a])
    a_overlap = np.array([overlap_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_i)), function_type='SETHARES_BELL') for chord in m18m_i_arch_a])
    a_ratio = a_rough / a_overlap
    a_ratio /= np.max(a_ratio)

    b_rough = np.array([roughness_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_i)), function_type='SETHARES') for chord in m18m_i_arch_b])
    b_overlap = np.array([overlap_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_i)), function_type='SETHARES_BELL') for chord in m18m_i_arch_b])
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

    save_show(name, action)

# Music for 18 Musicians, Section IX
def m18m_ix(action):
    name = 'm18m_ix'

    tim = HarrisonTimbre(11)
    fund_ix = midi_zero
    m18m_ix_backdrop = [] # data temporarily redacted
    m18m_ix_loop_top = [
        [],
        # data temporarily redacted
    ]
    m18m_ix_loop = [m18m_ix_backdrop + chord for chord in m18m_ix_loop_top]

    sect_ix_rough = np.array([roughness_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_ix)), function_type='SETHARES') for chord in m18m_ix_loop])
    sect_ix_overlap = np.array([overlap_complex(MergedSpectrum(ChordSpectrum(chord, 'ST_DIFF', timbre=tim, fund_hz=fund_ix)), function_type='SETHARES_BELL') for chord in m18m_ix_loop])
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

    save_show(name, action)

# Sensitivity of relative roughness to presence of higher partials.
def high_partials_sensitivity(action):
    name = 'high_partials_sensitivity'

    ref_8 = HarrisonTone(8)
    test_8 = HarrisonTone(8)
    ref_9 = HarrisonTone(9)
    test_9 = HarrisonTone(9)
    T = one_octave
    # T = TransposeDomain(-0.5, 12.5, 11, 'ST_DIFF')

    rough_8 = roughness_curve(ref_8, test_8, transpose_domain=T, function_type='SETHARES', normalize=True)
    rough_9 = roughness_curve(ref_9, test_9, transpose_domain=T, function_type='SETHARES', normalize=True)
    overlap_8 = overlap_curve(ref_8, test_8, transpose_domain=T, function_type='SETHARES_BELL', normalize=True)
    overlap_9 = overlap_curve(ref_9, test_9, transpose_domain=T, function_type='SETHARES_BELL', normalize=True)
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
    ax[0].legend(['8 partials', '9 partials'], edgecolor='k')
    ax[0].set_ylim(0, 1.1)
    ax[1].set_ylim(0, 1.1)
    ax[1].plot(T.domain, ratio_8, 'k')
    ax[1].plot(T.domain, ratio_9, 'k--')
    ax[1].legend(['8 partials', '9 partials'], edgecolor='k')
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

    save_show(name, action)

# Idealized overlap function using a flat-saw timbre
def idealized_overlap(action):
    name = 'idealized_overlap'

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
    ref_tone = FlatSawTone(11)
    test_tone = FlatSawTone(11)
    T = TransposeDomain(1.0, 2.0, 1000, 'SCALE_FACTOR')

    overlap = overlap_curve(
        ref_tone,
        test_tone,
        transpose_domain=T,
        function_type='SETHARES_BELL',
        normalize=True,
        options={
            'crossterms_only': False,
            'show_partials': False,
            'amp_type': 'MIN',
            'cutoff': False,
            'K': -23.74
        }
    )

    # Plot
    fig, ax = plt.subplots()
    ax.plot(T.domain, overlap, 'k-', linewidth=2)
    markers, stemlines, _ = ax.stem(interval, overlap_ideal, linefmt='k--', markerfmt='o', basefmt=' ')
    plt.setp(stemlines, linewidth=1)
    plt.setp(markers, markersize=5, markeredgecolor='k', markerfacecolor='w')
    ax.legend(['S-like overlap (steep slope)', 'C function'], edgecolor='k')
    ax.set_ylim(0)
    plt.xlabel('interval (ratio)')
    plt.ylabel('overlap (arbitrary units)')
    ax.xaxis.set_major_formatter('{x:.1f}')
    ax.yaxis.set_label_coords(-0.1, 0.5)

    save_show(name, action)

##########################
#### APPENDIX FIGURES ####
##########################

# My attempt to implement Helmholtz’s composite function.
def complex_roughness_helmholtz(action):
    name = 'complex_roughness_helmholtz'

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

    save_show(name, action)


def __main__(argv):
    action = ''
    if len(argv) > 1:
        action = argv[1].lower()

    # helmholtz_pair(action)
    # timbre_plots(action)
    # pair_roughness(action)
    # complex_roughness(action)
    # fratres_roughness(action)
    # cardinality_proximity(action)
    # octave_drift_sethares(action)
    # octave_drift_parncutt(action)
    # pair_overlap_sethares(action)
    # pair_overlap_parncutt(action)
    # complex_overlap_sethares(action)
    # complex_overlap_parncutt(action)
    # vary_k_overlap(action)
    # rel_roughness_8ve_h11_sethares(action)
    # rel_roughness_8ve_h11_parncutt(action)
    # rel_roughness_8ve_e11_sethares(action)
    # rel_roughness_8ve_e11_parncutt(action)
    # different_operations_roughness_overlap(action)
    # maj7_chord(action)
    # add_to_triad(action)
    # m18m_chorale(action)
    # m18m_i(action)
    # m18m_ix(action)
    # high_partials_sensitivity(action)
    # idealized_overlap(action)
    # complex_roughness_helmholtz(action)

    plt.close('all')

if __name__ == '__main__':
    __main__(sys.argv)
