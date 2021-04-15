import numpy as np
import chordkit.chord_utils as cu

default_timbre = cu.default_timbre
default_fund = cu.default_fund
default_chord_struct = [0]
default_chord = cu.ChordSpectrum(default_chord_struct)
default_chord_struct_type = 'ST-DIFF'
default_function_type = 'SETHARES'
default_transpose_domain = cu.TransposeDomain(0, 12, 100, 'ST_DIFF')
