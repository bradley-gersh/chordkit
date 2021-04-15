import pandas as pd
import numpy as np
import chordkit.chord_utils as cu
import chordkit.defaults as de
from chordkit.roughness_models import roughness_complex
from chordkit.chord_utils import Spectrum, ChordSpectrum

def roughness_curve(
    ref_chord: ChordSpectrum,
    test_chord: ChordSpectrum,
    # ref_chord_struct: list = de.default_chord_struct,
    # chord_struct_type: str = de.default_chord_struct_type,
    # *,
    # fund_hz: float = de.default_fund,
    # ref_timbre: pd.DataFrame = de.default_timbre,
    # test_chord_struct: list = de.default_chord_struct,
    # test_timbre: pd.DataFrame = de.default_timbre,
    transpose_range: list = de.default_chord_domain,
    transpose_type: str = 'ST_DIFF',
    function_type: str = de.default_function_type,
    options = {
        'normalize': True,
        #'crossterms_only': False, # Need to implement
        'original': False
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

    roughness_vals = np.zeros(np.shape(slide_range))

    # if chord_struct_type.upper() == 'HZ_SHIFT':
        # fund_hz = 0

    for (idx, position) in enumerate(transpose_range):
        # new_test_timbre['fund_multiple'] = cu.slide_timbre(position, test_timbre, chord_struct_type=chord_struct_type)
        # test_chord = cu.make_chord(test_chord_struct, chord_struct_type, timbre=new_test_timbre, fund_hz=fund_hz)
        test_chord.transpose(position, transpose_type)
        # union = ref_chord.append(test_chord, ignore_index=True)
        union = Spectrum(ref_chord, test_chord)
        curr_roughness_val = (roughness_complex(union, function_type, options))['roughness']
        roughness_vals[idx] = curr_roughness_val

    return roughness_vals
