import numpy as np
import matplotlib.pyplot as plt
import chordkit.defaults as de
from chordkit.roughness_models import roughness_complex
from chordkit.overlap_models import overlap_complex
from chordkit.chord_utils import MergedSpectrum, ChordSpectrum, TransposeDomain, Timbre

def overlap_curve(
    ref_chord: ChordSpectrum,
    test_chord: ChordSpectrum,
    *,
    transpose_domain: TransposeDomain = de.default_transpose_domain,
    function_type: str = de.default_overlap_function_type,
    normalize: bool = False,
    options = {
        'crossterms_only': False,
        'amp_type': 'MIN',
        'cutoff': False,
        'original': False,
        'show_partials': False
    }
):

    overlap_vals = np.zeros(np.shape(transpose_domain.domain))

    if options['crossterms_only']:
        if options['show_partials']:
            ref_self_overlap = (overlap_complex(ref_chord, function_type, options=options))['overlap']
        else:
            ref_self_overlap = (overlap_complex(ref_chord, function_type, options=options))

    for (idx, position) in enumerate(transpose_domain.domain):
        # new_test_timbre['fund_multiple'] = cu.slide_timbre(position, test_timbre, chord_struct_type=chord_struct_type)
        # test_chord = cu.make_chord(test_chord_struct, chord_struct_type, timbre=new_test_timbre, fund_hz=fund_hz)
        test_chord.transpose(position, transpose_domain.transpose_type)
        # union = ref_chord.append(test_chord, ignore_index=True)

        union = MergedSpectrum(ref_chord, test_chord)

        if options['show_partials']:
            curr_overlap_val = (overlap_complex(union, function_type, options=options))['overlap']
        else:
            curr_overlap_val = (overlap_complex(union, function_type, options=options))

        if options['crossterms_only']:
            if options['show_partials']:
                test_self_overlap = (overlap_complex(ref_chord, function_type, options=options))['overlap']
            else:
                test_self_overlap = (overlap_complex(ref_chord, function_type, options=options))
            curr_overlap_val -= (ref_self_overlap + test_self_overlap)

        overlap_vals[idx] = curr_overlap_val


    # test_chord has been mutated by .transpose(); need to reset
    test_chord.reset_partials()

    if normalize:
        plotMax = max(overlap_vals)
        overlap_vals /= float(plotMax)

    return overlap_vals

def roughness_curve(
    ref_chord: ChordSpectrum,
    test_chord: ChordSpectrum,
    # ref_chord_struct: list = de.default_chord_struct,
    # chord_struct_type: str = de.default_chord_struct_type,
    *,
    # fund_hz: float = de.default_fund,
    # ref_timbre: pd.DataFrame = de.default_timbre,
    # test_chord_struct: list = de.default_chord_struct,
    # test_timbre: pd.DataFrame = de.default_timbre,
    transpose_domain: TransposeDomain = de.default_transpose_domain,
    function_type: str = de.default_roughness_function_type,
    normalize: bool = False,
    plot: bool = False,
    options = {
        'crossterms_only': False,
        'amp_type': 'MIN',
        'cutoff': False,
        'original': False,
        'show_partials': False
    }
):

    # Using Sethares' original function. Note that incorporating crossterms only
    # (i.e. interactions between the two chords, not roughness relations of
    # partials within chord) removes register-dependent effects due to
    # self-roughness alone.
    #if options['original']:
        # options['crossterms_only'] = False

    # ref_chord = cu.make_chord(ref_chord_struct, chord_struct_type, timbre=ref_timbre, fund_hz=fund_hz)
    # new_test_timbre = test_timbre.copy()

    if (ref_chord == test_chord):
        copy_tim = Timbre(ref_chord.partials['hz_orig'], ref_chord.partials['amp'])
        test_chord = ChordSpectrum([0], 'ST_DIFF', timbre=copy_tim, fund_hz=1)
        min_hz = np.min(test_chord.partials['hz_orig'])
        test_chord.partials['fund_multiple'] /= min_hz

    roughness_vals = np.zeros(np.shape(transpose_domain.domain))

    # if chord_struct_type.upper() == 'HZ_SHIFT':
        # fund_hz = 0

    if options['crossterms_only']:
        if options['show_partials']:
            ref_self_diss = (roughness_complex(ref_chord, function_type, options=options))['roughness']
        else:
            ref_self_diss = (roughness_complex(ref_chord, function_type, options=options))

    for (idx, position) in enumerate(transpose_domain.domain):
        # new_test_timbre['fund_multiple'] = cu.slide_timbre(position, test_timbre, chord_struct_type=chord_struct_type)
        # test_chord = cu.make_chord(test_chord_struct, chord_struct_type, timbre=new_test_timbre, fund_hz=fund_hz)
        test_chord.transpose(position, transpose_domain.transpose_type)
        # union = ref_chord.append(test_chord, ignore_index=True)

        if function_type.upper() == 'HELMHOLTZ':
            union = MergedSpectrum(test_chord)
        else:
            union = MergedSpectrum(ref_chord, test_chord)

        if options['show_partials']:
            curr_roughness_val = (roughness_complex(union, function_type, options=options))['roughness']
        else:
            curr_roughness_val = (roughness_complex(union, function_type, options=options))

        if options['crossterms_only']:
            if options['show_partials']:
                test_self_diss = (roughness_complex(ref_chord, function_type, options=options))['roughness']
            else:
                test_self_diss = (roughness_complex(ref_chord, function_type, options=options))
            curr_roughness_val -= (ref_self_diss + test_self_diss)

        roughness_vals[idx] = curr_roughness_val

    # test_chord has been mutated by .transpose(); need to reset
    test_chord.reset_partials()

    if normalize:
        plotMax = max(roughness_vals)
        roughness_vals /= float(plotMax)

    if plot:
        plt.plot(transpose_domain.domain, roughness_vals)
        plt.show()

    return roughness_vals
